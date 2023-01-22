from elasticsearch import Elasticsearch
import requests
import re
from typing import List, Dict, Tuple, Any, TypeVar, Generator

Document = TypeVar("Document")

# define elasticsearch connection
try:
    es = Elasticsearch(
        "http://localhost:9200",
        verify_certs=False,
        timeout=60,
        retry_on_timeout=True,
        max_retries=5,
    )  # Security not enabled
except Exception as e:
    AssertionError(
        f"Elasticsearch connection failed. Please check your connection and that Host and Port in the config file are correct. Error: {e}"
    )

# define api url to get all plenary protocols
api_url = "https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.datum.start=2021-09-26&apikey=ECrwIai.ErBmVaihLIzqiqu9DqNoVFVvUysTzDwuOo"


# define index names
index_protokolle = "f2_test_protokolle"
missing_index = "f2_test_missing"
index_remarks = "f2_test_remarks"


def lastWords(string: str) -> str:
    """
    This function returns last 3 words of a string
    parameter: string
    return: string
    """

    lis = list(string.split(" "))
    concat = " ".join(lis[-3:])

    return concat


def get_missing_mps(document: str) -> tuple:
    """
    This function returns a dictionary with the number of missing MPs per party
    parameter: document (string)
    return: tuple of lists
    """

    # create helper arrays
    party_dict = {
        "DIE LINKE": [],
        "CDU/CSU": [],
        "FDP": [],
        "SPD": [],
        "BÜNDNIS 90/": [],
        "fraktionslos": [],
        "AfD": [],
    }

    # This split is done to seperate the Anlagen from the rest of the text, it is the only consistently working string we know of
    document = document.replace(" .", ".")
    split = document.split("Stenografischen Bericht")

    # This split is done to cut the rest of the file from the missing MPs part of the anlagen.
    # If there is no Anlage 2, we have found that splitting on "satzweiss.com" yields good results too
    try:
        split = split[1].split("Anlage 2")

        missing_mps = split[0].split("Satzweiss.com")
    except:

        try:
            missing_mps = split[1].split("Satzweiss.com")
        except:
            missing_mps = split[0]

    # split into seperate rows to get MP names
    missing = re.split("\d+\.\d+\.\d+", missing_mps[0])

    missing_mps = missing[0].splitlines()
    # print(missing_mps)

    # assign mps to parties
    for element in missing_mps:

        for party in [
            "DIE LINKE",
            "CDU/CSU",
            "FDP",
            "SPD",
            "BÜNDNIS 90/",
            "fraktionslos",
            "AfD",
        ]:
            if party in element:
                element = element.split(party)

                try:

                    switchnames = element[0].split(",")
                    name = switchnames[1] + " " + switchnames[0]

                except IndexError:
                    print("Index out of bounds for switchnames. Unordered name is used instead")
                    name = element[0]

                party_dict[party].append(name)

                continue

    # Here the complete names of missing mps per meeting are added to a dictionary with the meeting id in format "19XXX" as a key

    missing_mp_stats = {
        "Linke": len(party_dict["DIE LINKE"]),
        "CDU": len(party_dict["CDU/CSU"]),
        "SPD": len(party_dict["SPD"]),
        "AfD": len(party_dict["AfD"]),
        "Fraktionslos": len(party_dict["fraktionslos"]),
        "Gruene": len(party_dict["BÜNDNIS 90/"]),
        "FDP": len(party_dict["FDP"]),
    }

    return (
        party_dict["Die Linke"],
        party_dict["CDU/CSU"],
        party_dict["SPD"],
        party_dict["AfD"],
        party_dict["fraktionslos"],
        party_dict["BÜNDNIS 90/"],
        party_dict["FDP"],
        missing_mp_stats,
    )


def get_party(element: str) -> list:
    """
    This function returns a list of parties that are mentioned in a string
    parameter: element (string)
    return: list
    """
    remarking_party = []

    for party in [
        "FRAKTIONSLOS",
        "CDU/CSU",
        "SPD",
        "AfD",
        "FDP",
        "DIE GRÜNEN",
        "LINKE",
    ]:
        if party in element:
            remarking_party.append(party)

    return remarking_party

def get_remarks(
    meeting_id: int, date: str, text: str, name_speaker: str, party: str
) -> None:
    """
    Fills the remarks index with remarks made by MPs
    parameter: meeting_id (int), date (datetime), text (string), name_speaker (string), party (string)
    return: None
    """

    parties = ["LINKE", "BÜNDNIS 90", "CDU/CSU", "SPD", "FDP", "AfD", "fraktionslos"]
    remark_class = []
    remarks = []

    potentialremarks = re.findall("\((\n*?|[^)]*)\)", text)

    for element in potentialremarks:
        if len(element) > 9:
            if any(party in element for party in parties):
                remarks.append(element)

    for element in remarks:
        remark_class = []
        remarking_parties = []

        # TODO: None of these variables are needed, you dont have to initialize them
        # Got referenced before assignment error when not initializing
        remarking_persons = ""
        party_remarking_person = ""
        cleaned_list = []
        cleaned_text = ""

        for type in ["Beifall", "Lachen", "Heiterkeit", "Zuruf"]:
            if type in element:
                remark_class.append(type)
                remarking_parties.append(get_party(element))

                continue

        # TODO: Are the [] really necessary? If no we could directly use the party name
        # Yes they are necessary
        for party in [
            "[SPD]:",
            "[CDU/CSU]:",
            "[AfD]:",
            "[FDP]:",
            "[DIE LINKE]:",
            "[DIELINKE]:",
            "[BÜNDNIS 90/DIE GRÜNEN]:",
            "[fraktionslos]:",
        ]:
            if party in element:
                party_remarking_person = party[1:-2]
                list = element.split()
                index = list.index(party)
                try:
                    remarking_persons = str(list[index - 2] + " " + list[index - 1])

                except ValueError:
                    print("No remarkign Person found")
                    remarking_persons = "None"

                cleaned_list = element.split(party)
                cleaned_text = cleaned_list.pop()

                continue

        if "[BÜNDNIS 90/DIE GRÜNEN]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "Bündnis 90/Die Grünen"

            remarking_parties = []
            list = element.split()
            print(list)
            # TODO: Isnt a ]: missing here?
            # No, the split splits the party name in half
            # TODO: Is it ok to handle it like above? If yes we could use the same code for all parties
            # Yes should be okay
            index = list.index("[BÜNDNIS")
            try:
                remarking_persons = str(list[index - 2] + " " + list[index - 1])
            except:
                remarking_persons = "None"

            cleaned_list = element.split("[BÜNDNIS 90/DIE GRÜNEN]:")
            cleaned_text = cleaned_list.pop()

        # TODO: Why are there two different ways to handle die linke regarding the index?
        # Die Linke is not spelled consistently in the docs
        if "[DIELINKE]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "Die Linke"

            list = element.split()
            index = list.index("[DIELINKE]:")
            try:
                remarking_persons = str(list[index - 2] + " " + list[index - 1])
            except:
                remarking_persons = "None"

            cleaned_list = element.split("[DIELINKE]:")
            cleaned_text = cleaned_list.pop()

        if "[DIE LINKE]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "Die Linke"

            list = element.split()

            try:
                index = list.index("[DIE LINKE]:")
                remarking_persons = str(list[index - 2] + " " + list[index - 1])
            except:
                remarking_persons = "None"

            cleaned_list = element.split("[DIE LINKE]:")
            cleaned_text = cleaned_list.pop()

        fill_elastic_remarks(
            meeting_id,
            date,
            element,
            name_speaker,
            party,
            remark_class,
            remarking_parties,
            remarking_persons,
            party_remarking_person,
            cleaned_text,
        )
        es.indices.refresh(index=index_remarks)


# TODO: Is document a string or a list? Then please add a type hint
# Any is okay, document is converted to string in the function
def Preprocessing(document: Any) -> Generator[list, None, None]:
    """
    Preprocessing of the text
    parameter: document (string)
    return: tuple of strings
    """
    meeting_content = str(document)

    meeting_content = " ".join(line.strip() for line in meeting_content.splitlines())
    meeting_content = meeting_content.replace("- ", "")
    meeting_content = re.sub("\n", " ", meeting_content)

    party_split = re.split(
        "(\(DIE LINKE\):|\(AfD\):|\(BÜNDNIS 90/DIE GRÜNEN\):|\(CDU/CSU\):|\(FDP\):|\(FRAKTIONSLOS\):|\(SPD\):)",
        meeting_content,
    )

    # Splitting text into talking points
    party_dict = {
        "(DIE LINKE):": [],
        "(AfD):": [],
        "(BÜNDNIS 90/DIE GRÜNEN):": [],
        "(CDU/CSU):": [],
        "(FDP):": [],
        "FRAKTIONSLOS:": [],
        "(SPD):": [],
    }

    for idx, element in enumerate(party_split):

        for party in party_dict.keys():
            if party in element:
                party_dict[party].append(
                    lastWords(party_split[idx - 1])
                    + " "
                    + party_split[idx]
                    + " "
                    + party_split[idx + 1]
                )

                moderation_split = re.split(
                    "Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:",
                    party_dict[party][-1],
                )
                party_dict[party][-1] = moderation_split[0]
                continue

    # TODO: There is always only one none empty element in the list. Correct?
    # No there are the speeches per party in the dictionary
    return (speech for speech in party_dict.values())

def delete_elastic_index():
    """
    Deletes the elastic index"""
    es.options(ignore_status=[400, 404]).indices.delete(index=index_protokolle)

def fill_elastic(
    element: str,
    name_speaker: str,
    meeting_id: int,
    party: str,
    date: str,
    title: str,
    publisher: str,
):
    """
    Fills the elastic index with the data from the document
    """
    doc = {
        "Dokumentnummer": meeting_id,
        "Sprecher": name_speaker,
        "Partei": party,
        "Datum": date,
        "Titel": title,
        "Organ": publisher,
        "Text": element,
    }

    idDokumentennummer = re.sub("/", "", meeting_id)
    print("idDokumentennummer: " + idDokumentennummer)
    resp = es.index(index=index_protokolle, body=doc)



def fill_elastic_remarks(
    meeting_id: int,
    date: str,
    element: str,
    name_speaker: str,
    party: str,
    remark_class: list,
    remarking_parties: list,
    remarking_persons: list,
    party_remarking_person: str,
    cleaned_text: str
):
    """
    Fills the elastic index with the data from the document
    """
    doc = {
        "Dokumentnummer": meeting_id,
        "Sprecher der Rede": name_speaker,
        "Partei des Sprechers der Rede": party,
        "Datum": date,
        "Remark Class": remark_class,
        "Remarking Parties": remarking_parties,
        "Text": element,
        "Remarking Persons": remarking_persons,
        "Party Remarking Person": party_remarking_person,
        "Remark Text": cleaned_text,
    }

    idDokumentennummer = re.sub("/", "", meeting_id)
    print("idDokumentennummer: " + idDokumentennummer)
    resp = es.index(index=index_remarks, body=doc)




def fill_elastic_missing(
    meeting_id: int,
    date: str,
    title: str,
    missing_DIELINKE: list,
    missing_CDUCSU: list,
    missing_FDP: list,
    missing_SPD: list,
    missing_GRUENE: list,
    missing_FRAKTIONSLOS: list,
    missing_AFD: list
):
    """
    Fills the elastic index with the data from the document
    """
    doc = {
        "Dokumentnummer": meeting_id,
        "missing_DIELINKE": missing_DIELINKE,
        "missing_CDUCSU": missing_CDUCSU,
        "missing_FDP": missing_FDP,
        "missing_SPD": missing_SPD,
        "missing_GRUENE": missing_GRUENE,
        "missing_FRAKTIONSLOS": missing_FRAKTIONSLOS,
        "missing_AFD": missing_AFD,
        "Datum": date,
        "Titel": title,
    }

    idDokumentennummer = re.sub("/", "", meeting_id)
    print("idDokumentennummer: " + idDokumentennummer)
    resp = es.index(index=missing_index, body=doc)


def fill_loop(dictionary: dict):
    """
    Fills the elastic index with the data from the document
    """
    for document in dictionary["documents"]:
        if "text" not in document:
            continue
        meeting_id = document["dokumentnummer"]
        date = (document["datum"],)
        title = (document["titel"],)
        publisher = document["herausgeber"]

        (
            missing_DIELINKE,
            missing_CDUCSU,
            missing_FDP,
            missing_SPD,
            missing_GRUENE,
            missing_FRAKTIONSLOS,
            missing_AFD,
            missing_mp_stats,
        ) = get_missing_mps(document["text"])

        fill_elastic_missing(
            meeting_id,
            date,
            title,
            missing_DIELINKE,
            missing_CDUCSU,
            missing_FDP,
            missing_SPD,
            missing_GRUENE,
            missing_FRAKTIONSLOS,
            missing_AFD,
        )

        # TODO: There is always only one none empty element in the list. Correct?
        # No there should be all speeches from the current doc in them
        (
            Reden_AfD,
            Reden_CDU,
            Reden_FDP,
            Reden_Fraktionslos,
            Reden_Gruene,
            Reden_Linke,
            Reden_SPD,
        ) = Preprocessing(str(document["text"]))

        for element in Reden_AfD:
            name_speaker = element.split()[:2]
            party = "AfD"
            get_remarks(meeting_id, date, element, name_speaker, party)
            fill_elastic(
                element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_CDU:
            name_speaker = element.split()[:2]
            party = "CDU"
            fill_elastic(
                element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_FDP:
            name_speaker = element.split()[:2]
            party = "FDP"
            fill_elastic(
                element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_Fraktionslos:
            name_speaker = element.split()[:2]
            party = "Fraktionslos"
            fill_elastic(
                element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_Gruene:
            name_speaker = element.split()[:2]
            party = "Bündnis 90/Die Grünen"
            fill_elastic(
                element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_Linke:
            name_speaker = element.split()[:2]
            party = "Die Linke"
            fill_elastic(
                element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_SPD:
            name_speaker = element.split()[:2]
            party = "SPD"
            fill_elastic(
                element, name_speaker, meeting_id, party, date, title, publisher
            )

    es.indices.refresh(index=index_protokolle)
    es.indices.refresh(index=missing_index)
    es.indices.refresh(index=index_remarks)
    result = es.count(index=index_protokolle)
    geladeneProtkolle = result["count"]
    print("Anzahl Protokolle", geladeneProtkolle)


# delete_elastic_index() # ggf. vorhandener Index löschen
response = requests.get(api_url)

dictionary = response.json()


vorhandeneDokumente = dictionary["numFound"]
print("Gesamtanzahl vorhandener Dokumente: ", vorhandeneDokumente)

fill_loop(dictionary)

oldCursor = ""
cursor = dictionary["cursor"]

while len(cursor) > 0 and cursor != oldCursor:  # wenn neu = alt dann ende
    cursor = re.sub("\/", "%2F", cursor)
    cursor = re.sub("\+", "%2B", cursor)
    weiterlesen_url = api_url + "&cursor=" + cursor
    response = requests.get(weiterlesen_url)
    dictionary = response.json()
    fill_loop(dictionary)

    oldCursor = cursor
    cursor = dictionary["cursor"]
