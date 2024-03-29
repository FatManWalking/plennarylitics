from elasticsearch import Elasticsearch
from elasticsearch import __version__ as es_version
import requests
import re
from typing import List, Dict, Tuple, Any, Generator

# define index names
index_protokolle = "final_speeches"
missing_index = "final_missing"
index_remarks = "final_remarks"

# define helper variables
counter = 0
last_counter = 0
last_idDokumentennummer = ""


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

    # This split is done to cut the rest of the file from the missing MPs part of the anlagen.
    split = document.split("Entschuldigte ")

    try:
        missing_mps = split[2].split("Anlage 2")
        missing_mps = missing_mps[0]
    except:
        try:
            missing_mps = split[2]

        except:
            missing_mps = ""

    # split into seperate rows to get MP names
    missing = re.split("\d+\.\d+\.\d+", missing_mps)
    missing_mps = missing[0].splitlines()

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

                    switchnames = element[0].split(
                        ","
                    )  # Switches First Names and Last Names of MPs arounf
                    name = switchnames[1] + " " + switchnames[0]

                except IndexError as e:
                    name = element[0]

                if name == "":
                    break

                party_dict[party].append(name)

                break

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
        party_dict["DIE LINKE"],
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
    es: Elasticsearch,
    meeting_id: int,
    date: tuple,
    text: str,
    name_speaker: str,
    party_speaker: str,
) -> None:
    """
    Fills the remarks index with remarks made by MPs
    parameter: meeting_id (int), date (datetime), text (string), name_speaker (string), party (string)
    return: None
    """

    parties = ["LINKE", "BÜNDNIS 90", "CDU/CSU", "SPD", "FDP", "AfD", "fraktionslos"]
    remark_class = []
    remarks = []

    potentialremarks = re.findall("\((\n*?|[^)]*)\)", text)  # Find potential remarks

    for element in potentialremarks:
        if len(element) > 9:
            if any(party in element for party in parties):
                remarks.append(element)

    for element in remarks:
        remark_class = []
        remarking_parties = []  # Contains values of entire fractions reacting
        remarking_persons = []  # Contains values of specific persons reacting
        party_remarking_person = []

        for type in [
            "Beifall",
            "Lachen",
            "Heiterkeit",
            "Zuruf",
        ]:  # Classifies reactions that are not thematic
            if type in element:
                remark_class.append(type)
                remarking_parties.append(get_party(element))

        for party in [
            "[SPD]:",
            "[CDU/CSU]:",
            "[AfD]:",
            "[FDP]:",
            "[DIELINKE]:",
            "[FRAKTIONSLOS]:",
        ]:
            if (
                party in element
            ):  # Classifies reactions that are thematic (done by a person)

                party_remarking_person.append(party[1:-2])
                list = element.split()
                try:
                    index = list.index(party)
                except ValueError as e:
                    print(e, list, party)
                remark_class.append("Thematischer Zwischenruf")
                try:
                    pers = str(list[index - 2] + " " + list[index - 1])
                    if "von" in pers:
                        remarking_persons.append(
                            str(
                                list[index - 3]
                                + " "
                                + list[index - 2]
                                + " "
                                + list[index - 1]
                            )
                        )
                    else:
                        remarking_persons.append(pers)

                except ValueError as e:

                    remarking_persons = "None"
                except UnboundLocalError as e:
                    print(f"UnboundLocalError: {e} in {element}")

            try:
                cleaned_list = element.split(party)
                cleaned_text = cleaned_list.pop()
            except UnboundLocalError as e:
                print(f"UnboundLocalError: {e} in {element}")

        # The Following is done to catch different variations of Party names that are used in the plenary protocols

        if "[BÜNDNIS 90/DIE GRÜNEN]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person.append("Bündnis 90/Die Grünen")

            remarking_parties = []
            list = element.split()

            index = list.index("[BÜNDNIS")
            try:
                pers = str(list[index - 2] + " " + list[index - 1])
                if "von" in pers:
                    remarking_persons.append(
                        str(
                            list[index - 3]
                            + " "
                            + list[index - 2]
                            + " "
                            + list[index - 1]
                        )
                    )
                else:
                    remarking_persons.append(pers)
            except:
                remarking_persons = "None"

            cleaned_list = element.split("[BÜNDNIS 90/DIE GRÜNEN]:")
            cleaned_text = cleaned_list.pop()

        if "[DIE LINKE]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            element = element.replace("[DIE LINKE]:", "[DIELINKE]:")
            party_remarking_person.append("Die Linke")

            list = element.split()
            index = list.index("[DIELINKE]:")
            try:
                pers = str(list[index - 2] + " " + list[index - 1])
                if "von" in pers:
                    remarking_persons.append(
                        str(
                            list[index - 3]
                            + " "
                            + list[index - 2]
                            + " "
                            + list[index - 1]
                        )
                    )
                else:
                    remarking_persons.append(pers)
            except:
                remarking_persons = "None"

            cleaned_list = element.split("[DIELINKE]:")
            cleaned_text = cleaned_list.pop()

        if remarking_persons == []:
            remarking_person = "None"
            party_remarking_person = "None"
            cleaned_text = element

        fill_elastic_remarks(
            es,
            meeting_id,
            date,
            element,
            name_speaker,
            party_speaker,
            remark_class,
            remarking_parties,
            remarking_persons,
            party_remarking_person,
            cleaned_text,
        )
        es.indices.refresh(index=index_remarks)


def Preprocessing(document: Any) -> Generator[list, None, None]:
    """
    General preprocessing of the text
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

    # Splitting text into talking points (speeches)
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
                )  # This split is done to seperate ends of speeches that contain moderation by the President or Vice President of the Bundestag
                party_dict[party][-1] = moderation_split[0]
                break

    for element in party_dict.values():  # This catches noise in the Data
        element = re.sub(
            "Deutscher Bundestag[^>]+\(A\) \(B\) \(C\) \(D\)", "", str(element)
        )
    return (speech for speech in party_dict.values())


def delete_elastic_index(es: Elasticsearch, index_protokolle: str):
    """
    Deletes the elastic index"""
    es.options(ignore_status=[400, 404]).indices.delete(index=index_protokolle)


def counter_function(idDokumentennummer: str):
    """
    Counter for the id of the elastic index
    While the idDokumentennummer is the same, the counter is increased
    Yields the counter
    """

    global counter
    global last_counter
    global last_idDokumentennummer
    if idDokumentennummer == last_idDokumentennummer:
        counter += 1
    else:
        last_counter = counter
        counter = 1
    last_idDokumentennummer = idDokumentennummer
    return counter, last_counter


def fill_elastic(
    es: Elasticsearch,
    element: str,
    name_speaker: str,
    meeting_id: int,
    party: str,
    date: tuple,
    title: str,
    publisher: str,
):
    """
    Fills the elastic index with the data from the document. Fills data about speeches made by different MPs
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
    counter, last_counter = counter_function(idDokumentennummer)
    if counter == 1:
        print(
            f"Indexing {idDokumentennummer} - complete with {last_counter} entries",
            end="\n",
        )
    else:
        print(f"Indexing {idDokumentennummer} - {counter}", end="\r")
    es.index(index=index_protokolle, document=doc)


def fill_elastic_remarks(
    es: Elasticsearch,
    meeting_id: int,
    date: tuple,
    element: str,
    name_speaker: str,
    party: str,
    remark_class: list,
    remarking_parties: list,
    remarking_persons: str,
    party_remarking_person: str,
    cleaned_text: str,
):
    """
    Fills the elastic index with the data from the document. Only fills remarks.
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
    counter, last_counter = counter_function(idDokumentennummer)
    if counter == 1:
        print(
            f"Indexing {idDokumentennummer} - complete with {last_counter} Remarks",
            end="\n",
        )
    else:
        print(f"Indexing {idDokumentennummer} - {counter}", end="\r")
    es.index(index=index_remarks, document=doc)


def fill_elastic_missing(
    es: Elasticsearch,
    meeting_id: int,
    date: tuple,
    title: tuple,
    missing_DIELINKE: list,
    missing_CDUCSU: list,
    missing_FDP: list,
    missing_SPD: list,
    missing_GRUENE: list,
    missing_FRAKTIONSLOS: list,
    missing_AFD: list,
):
    """
    Fills the elastic index with the data from the document. Only fills data about missing MPs
    """
    if (
        len(missing_DIELINKE) == 0
        and len(missing_CDUCSU) == 0
        and len(missing_FDP) == 0
        and len(missing_SPD) == 0
        and len(missing_GRUENE) == 0
        and len(missing_FRAKTIONSLOS) == 0
        and len(missing_AFD) == 0
    ):
        return

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
    counter, last_counter = counter_function(idDokumentennummer)
    if counter == 1:
        print(
            f"Indexing {idDokumentennummer} - complete with {last_counter} Entries about Missing",
            end="\n",
        )
    else:
        print(f"Indexing {idDokumentennummer} - {counter}", end="\r")
    es.index(index=missing_index, document=doc)


def fill_loop(es: Elasticsearch, dictionary: dict):
    """
    Fills the elastic index with the data from the document. This is the Main loop calling all other fill functions
    """
    for document in dictionary["documents"]:
        if "text" not in document:
            break
        meeting_id = document["dokumentnummer"]
        date = (document["datum"],)
        title = (document["titel"],)
        publisher = document["herausgeber"]

        (
            missing_DIELINKE,
            missing_CDUCSU,
            missing_SPD,
            missing_AFD,
            missing_FRAKTIONSLOS,
            missing_GRUENE,
            missing_FDP,
            missing_mp_stats,
        ) = get_missing_mps(document["text"])

        fill_elastic_missing(
            es,
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

        (
            Reden_Linke,
            Reden_AfD,
            Reden_Gruene,
            Reden_CDU,
            Reden_FDP,
            Reden_Fraktionslos,
            Reden_SPD,
        ) = Preprocessing(str(document["text"]))

        for element in Reden_AfD:
            name_speaker = element.split()[:2]
            party = "AfD"
            get_remarks(es, meeting_id, date, element, name_speaker, party)
            fill_elastic(
                es, element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_CDU:
            name_speaker = element.split()[:2]
            party = "CDU"
            get_remarks(es, meeting_id, date, element, name_speaker, party)
            fill_elastic(
                es, element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_FDP:
            name_speaker = element.split()[:2]
            party = "FDP"
            get_remarks(es, meeting_id, date, element, name_speaker, party)
            fill_elastic(
                es, element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_Fraktionslos:
            name_speaker = element.split()[:2]
            party = "Fraktionslos"
            get_remarks(es, meeting_id, date, element, name_speaker, party)
            fill_elastic(
                es, element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_Gruene:
            name_speaker = element.split()[:2]
            party = "Bündnis 90/Die Grünen"
            get_remarks(es, meeting_id, date, element, name_speaker, party)
            fill_elastic(
                es, element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_Linke:
            name_speaker = element.split()[:2]
            party = "Die Linke"
            get_remarks(es, meeting_id, date, element, name_speaker, party)
            fill_elastic(
                es, element, name_speaker, meeting_id, party, date, title, publisher
            )

        for element in Reden_SPD:
            name_speaker = element.split()[:2]
            party = "SPD"
            get_remarks(es, meeting_id, date, element, name_speaker, party)
            fill_elastic(
                es, element, name_speaker, meeting_id, party, date, title, publisher
            )

    # Refresh Indeces to update Elasticsearch Information
    es.indices.refresh(index=index_protokolle)
    es.indices.refresh(index=missing_index)
    es.indices.refresh(index=index_remarks)
    result = es.count(index=index_protokolle)
    geladeneProtkolle = result["count"]
    print("Anzahl Protokolle", geladeneProtkolle)


def establish_elastic_connection():
    """
    Establishes a connection to the elastic search instance

    Returns: Elasticsearch object
    """
    # define elasticsearch connection

    es = Elasticsearch(
        "http://elasticsearch:9200",
        verify_certs=False,
        request_timeout=60,
        retry_on_timeout=True,
        max_retries=5,
    )  # Security not enabled

    # check if connection is established
    if es.ping():
        print("Elasticsearch connection established.")
        return es
    else:
        print("Elasticsearch connection failed.")
        return None


if __name__ == "__main__":
    # Elasticsearch connection
    print(f"Elasticsearch Version: {es_version}")
    es = establish_elastic_connection()
    if es is None:
        raise AssertionError("Elasticsearch connection failed.")

    # define api url to get all plenary protocols
    api_url = "https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.datum.start=2021-09-26&apikey=ECrwIai.ErBmVaihLIzqiqu9DqNoVFVvUysTzDwuOo"

    response = requests.get(api_url)

    dictionary = response.json()

    vorhandeneDokumente = dictionary["numFound"]
    print("Gesamtanzahl vorhandener Dokumente: ", vorhandeneDokumente)

    fill_loop(es, dictionary)

    oldCursor = ""
    cursor = dictionary["cursor"]

    # Pulls Files in Batches from the Bundestag API

    while len(cursor) > 0 and cursor != oldCursor:  # wenn neu = alt dann ende
        cursor = re.sub("\/", "%2F", cursor)
        cursor = re.sub("\+", "%2B", cursor)
        weiterlesen_url = api_url + "&cursor=" + cursor
        response = requests.get(weiterlesen_url)
        dictionary = response.json()
        fill_loop(es, dictionary)

        oldCursor = cursor
        cursor = dictionary["cursor"]
