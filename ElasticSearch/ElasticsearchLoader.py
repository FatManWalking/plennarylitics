from elasticsearch import Elasticsearch
import requests
import re
import xml.etree.ElementTree as ET
import re
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import os

#define index names

index_protokolle = "protocols_loop2"
missing_index = "missing_loop2"

# Function which returns last words

def lastWords(string):

# split by space and converting
# string to list and
    lis = list(string.split(" "))
    concat = " ".join(lis[-3:])

# returning last 3 elements in list
    return concat

def get_missing_mps(document):

    missing_mps_DIE_LINKE = {}
    missing_mps_CDUCSU = {}
    missing_mps_FDP = {}
    missing_mps_SPD = {}
    missing_mps_GRUENE = {}
    missing_mps_FRAKTIONSLOS = {}
    missing_mps_AFD = {}

    #create helper arrays

    DIELINKE = []
    CDUCSU= []
    FDP= []
    SPD= []
    GRUENE= []
    FRAKTIONSLOS= []
    AFD= []

     #This split is done to seperate the Anlagen from the rest of the text, it is the only consistently working string we know of
    document = document.replace(" .",".")
    split = document.split("Stenografischen Bericht")
    

    #This split is done to cut the rest of the file from the missing MPs part of the anlagen. If there is no Anlage 2, we have found that splitting on "satzweiss.com" yields good results too
    
    try:
        split = split[1].split("Anlage 2")

        missing_mps = split[0].split("Satzweiss.com")
    except:

        try:
            missing_mps = split[1].split("Satzweiss.com")
        except:
            missing_mps = split[0]

    
    
    
    
    #split into seperate rows to get MP names

    missing = re.split("\d+\.\d+\.\d+",missing_mps[0])


    missing_mps = missing[0].splitlines( )
    print(missing_mps)

    #assign mps to parties

    for element in missing_mps:

        if "DIE LINKE" in element:
            element = element.split("DIE LINKE")

            try:

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)

            except:

                name = element[0]
           
            DIELINKE.append(name)
            #np.append(missing_mps_DIE_LINKE, [[filename],[element[0]]])
            
        if "CDU/CSU" in element:
            element = element.split("CDU/CSU")

            try:

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)

            except:

                name = element[0]
   
            CDUCSU.append(name)

        if "FDP" in element:
            element = element.split("FDP")
            
            try:

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)

            except:

                name = element[0]
      
            
            FDP.append(name)
           

        if "SPD" in element:
            element = element.split("SPD")
            try:
                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)

            except:

                name = element[0]
          
            SPD.append(name)
        
        if "BÜNDNIS 90/" in element:
            element = element.split("BÜNDNIS 90/")

            try:    
                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)

            except:

                name = element[0]
           
            GRUENE.append(name)
        
        if "fraktionslos" in element:
            element = element.split("fraktionslos")

            try:    
                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)

            except:

                name = element[0]

            FRAKTIONSLOS.append(name)

        if "AfD" in element:
            element = element.split("AfD")

            try:

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)

            except:

                name = element[0]
 
            AFD.append(name)

    
    #Here the complete names of missing mps per meeting are added to a dictionary with the meeting id in format "19XXX" as a key

    missing_mp_stats = {
        "Linke": len(DIELINKE),
        "CDU": len(CDUCSU),
        "SPD": len(SPD),
        "AfD": len(AFD),
        "Fraktionslos": len(FRAKTIONSLOS),
        "Gruene": len(GRUENE),
        "FDP": len(FDP),
    }



    return DIELINKE, CDUCSU, FDP, SPD, GRUENE, FRAKTIONSLOS, AFD, missing_mp_stats


def Preprocessing(document):

#Read xml Files
#filename = '../Data/19026.xml'

    #tree = ET.parse(document)

    #root = tree.getroot()


    #for content in root.iter('TEXT'):
    #    meeting_content = content.text

    meeting_content = str(document)

   
    meeting_content = " ".join(line.strip() for line in meeting_content.splitlines())
    meeting_content = meeting_content.replace("- ","")
    meeting_content = re.sub('\n', ' ', meeting_content) 

    party_split = re.split("(\(DIE LINKE\):|\(AfD\):|\(BÜNDNIS 90/DIE GRÜNEN\):|\(CDU/CSU\):|\(FDP\):|\(FRAKTIONSLOS\):|\(SPD\):)", meeting_content)

    #Splitting text into talking points

  

    Reden_Linke = []
    Reden_AfD = []
    Reden_Gruene = []
    Reden_CDU = []
    Reden_FDP = []
    Reden_Fraktionslos = []
    Reden_SPD = []

    for idx, element in enumerate(party_split):

        #Check if text was split on party name

        if element == "(DIE LINKE):":

            #concat last words of previous split element (contains the referees name), actual split element (contains party name) and next split element (contains text of speech)

            Reden_Linke.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])

            #Split on name of the moderator to mark the end of the speech and delete none speech text parts

            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_Linke[-1])
            Reden_Linke[-1] = moderation_split[0]
        if element == "(AfD):":
            Reden_AfD.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_AfD[-1])
            Reden_AfD[-1] = moderation_split[0]
        if element == "(BÜNDNIS 90/DIE GRÜNEN):":
            Reden_Gruene.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_Gruene[-1])
            Reden_Gruene[-1] = moderation_split[0]
        if element == "(CDU/CSU):":
            Reden_CDU.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_CDU[-1])
            Reden_CDU[-1] = moderation_split[0]
        if element == "(FDP):":
            Reden_FDP.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_FDP[-1])
            Reden_FDP[-1] = moderation_split[0]
        if element == "(FRAKTIONSLOS):":
            Reden_Fraktionslos.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_Fraktionslos[-1])
            Reden_Fraktionslos[-1] = moderation_split[0]
        if element == "(SPD):":
            Reden_SPD.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_SPD[-1])
            Reden_SPD[-1] = moderation_split[0]

    return Reden_AfD, Reden_CDU, Reden_FDP, Reden_Fraktionslos, Reden_Gruene, Reden_Linke, Reden_SPD


def  convert_text(text):
    return text

def  delete_elastic_index():
    es.options(ignore_status=[400,404]).indices.delete(index=index_protokolle)

def fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher):
    #print("Verarbeite Dokument: ", document['dokumentnummer'])
    doc = {
        'Dokumentnummer': meeting_id,
        'Sprecher': name_speaker,
        'Partei': party,
        'Datum': date,
        'Titel': title,
        'Organ': publisher,
        'Text': element
    }

    idDokumentennummer = re.sub("/", "", meeting_id)
    print("idDokumentennummer: " + idDokumentennummer)
    resp = es.index(index=index_protokolle,  body=doc)

def fill_elastic_missing( meeting_id,date,title,missing_DIELINKE, missing_CDUCSU, missing_FDP, missing_SPD, missing_GRUENE, missing_FRAKTIONSLOS, missing_AFD):
    #print("Verarbeite Dokument: ", document['dokumentnummer'])
    doc = {
        'Dokumentnummer': meeting_id,
        'missing_DIELINKE': missing_DIELINKE, 
        'missing_CDUCSU': missing_CDUCSU,
        'missing_FDP': missing_FDP,
        'missing_SPD': missing_SPD,
        'missing_GRUENE': missing_GRUENE,
        'missing_FRAKTIONSLOS': missing_FRAKTIONSLOS,
        'missing_AFD': missing_AFD,
        'Datum': date,
        'Titel': title,
    }

    idDokumentennummer = re.sub("/", "", meeting_id)
    print("idDokumentennummer: " + idDokumentennummer)
    resp = es.index(index=missing_index,  body=doc)

def fill_loop(dictionary):

    for document in dictionary['documents']:
        meeting_id = document['dokumentnummer']
        date = document['datum'],
        title = document['titel'],
        publisher = document['herausgeber']

        missing_DIELINKE, missing_CDUCSU, missing_FDP, missing_SPD, missing_GRUENE, missing_FRAKTIONSLOS, missing_AFD, missing_mp_stats = get_missing_mps(document['text'])

        fill_elastic_missing(meeting_id,date,title,missing_DIELINKE, missing_CDUCSU, missing_FDP, missing_SPD, missing_GRUENE, missing_FRAKTIONSLOS, missing_AFD)
        
        Reden_AfD, Reden_CDU, Reden_FDP, Reden_Fraktionslos, Reden_Gruene, Reden_Linke, Reden_SPD = Preprocessing(str(document['text']))
        
        for element in Reden_AfD:
            name_speaker = element.split()[:2]
            party="AfD"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)


        for element in Reden_CDU:
            name_speaker = element.split()[:2]
            party="CDU"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)

        for element in Reden_FDP:
            name_speaker = element.split()[:2]
            party="FDP"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
    
        for element in Reden_Fraktionslos:
            name_speaker = element.split()[:2]
            party="Fraktionslos"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
    
        for element in Reden_Gruene:
            name_speaker = element.split()[:2]
            party="Bündnis 90/Die Grünen"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
    
        for element in Reden_Linke:
            name_speaker = element.split()[:2]
            party="Die Linke"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
        
        for element in Reden_SPD:
            name_speaker = element.split()[:2]
            party="SPD"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
       

    es.indices.refresh(index=index_protokolle)
    es.indices.refresh(index=missing_index)
    result = es.count(index=index_protokolle)
    geladeneProtkolle = result['count']
    print("Anzahl Protokolle", geladeneProtkolle)

es = Elasticsearch('http://127.0.0.1:9200') # Security not enabled
api_url = "https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.datum.start=2021-09-26&apikey=ECrwIai.ErBmVaihLIzqiqu9DqNoVFVvUysTzDwuOo"


#delete_elastic_index() # ggf. vorhandener Index löschen
response = requests.get(api_url)

dictionary = response.json()

vorhandeneDokumente = dictionary['numFound']
print("Gesamtanzahl vorhandener Dokumente: ", vorhandeneDokumente)

fill_loop(dictionary)

oldCursor = ""
cursor = dictionary['cursor']

while len(cursor) > 0 and cursor != oldCursor: # wenn neu = alt dann ende
    cursor = re.sub("\/", "%2F", cursor)
    cursor = re.sub("\+", "%2B", cursor)
    weiterlesen_url = api_url + "&cursor=" + cursor
    response = requests.get(weiterlesen_url)
    dictionary = response.json()
    fill_loop(dictionary)
    
    oldCursor = cursor
    cursor = dictionary['cursor']
