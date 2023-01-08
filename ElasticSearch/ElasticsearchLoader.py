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
import pandas as pd

#define index names

index_protokolle = "ghjkghjk"
missing_index = "gjhkgjkghjk"

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

def get_remarks(text):

    parties = ['LINKE', 'BÜNDNIS 90', 'CDU/CSU', 'SPD', 'FDP', 'AfD', 'fraktionslos']
    remark_class = []
    remarks = []
    remarking_party = []

    potentialremarks = re.findall( '\((\n*?|[^)]*)\)', text)

    for element in potentialremarks:
        if len(element) > 9:
            if any(party in element for party in parties):
                remarks.append(element)
    
    for element in remarks:
        if "Beifall" in element:
            remark_class.append("Beifall")
            #einwürfe.remove(element)
        if "Lachen" in element:
            remark_class.append("Lachen")
            #einwürfe.remove(element)
        if "Heiterkeit" in element:
            remark_class.append("Heiterkeit")
            #einwürfe.remove(element)
        if "Zuruf" in element:
            remark_class.append("Zuruf")
            #einwürfe.remove(element)
        if "[SPD]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            #einwürfe.remove(element)
        if "[CDU/CSU]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            #einwürfe.remove(element)
        if "[AfD]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            #einwürfe.remove(element)
        if "[FDP]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            #einwürfe.remove(element)
        if "[BÜNDNIS 90/DIE GRÜNEN]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            #einwürfe.remove(element)
        if "[DIELINKE]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            #einwürfe.remove(element)
        if "[FRAKTIONSLOS]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            #einwürfe.remove(element)
        if "SPD" in element:
            remarking_party.append("SPD")
        
        if "CDU/CSU" in element:
            remarking_party.append("CDU/CSU")
        
        if "AfD" in element:
            remarking_party.append("AfD")

        if "FDP" in element:
            remarking_party.append("FDP")
    
        if "DIE GRÜNEN" in element:
            remarking_party.append("DIE GRÜNEN")

        if "LINKE" in element:
            remarking_party.append("LINKE")

        if "FRAKTIONSLOS" in element:
            remarking_party.append("FRAKTIONSLOS")
        if len(remarking_party) > len(remark_class):
            remark_class.extend(['X'] * (len(remarking_party)-len(remark_class)))
        if len(remarking_party) < len(remark_class):
            remarking_party.extend(['X'] * (len(remark_class)-len(remarking_party)))
        if len(remarks) < len(remark_class):
            remarks.extend(['X'] * (len(remark_class)-len(remarks)))
        if len(remarks) < len(remarking_party):
            remarks.extend(['X'] * (len(remarking_party)-len(remarks)))

        

    print(len(remarks), len(remark_class),len(remarking_party))

    d = {'remark_text': remarks, 'remark_class': remark_class, 'remark_party': remarking_party}

    df_remarks = pd.DataFrame(data=d)

    return df_remarks

def Preprocessing(document):



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
    Remarks_Linke = []
    Remarks_AfD = []
    Remarks_Gruene = []
    Remarks_CDU = []
    Remarks_FDP = []
    Remarks_Fraktionslos = []
    Remarks_SPD = []


    for idx, element in enumerate(party_split):

        #Check if text was split on party name

        if element == "(DIE LINKE):":

            #concat last words of previous split element (contains the referees name), actual split element (contains party name) and next split element (contains text of speech)

            Reden_Linke.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])

            #Split on name of the moderator to mark the end of the speech and delete none speech text parts

            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_Linke[-1])
            remarks_in_speech = get_remarks(moderation_split[0])
            if remarks_in_speech.empty:
                remarks_in_speech['remark_text'] = "No remarks"
                remarks_in_speech['remark_class'] = "No remarks" 
                remarks_in_speech['remark_party'] = "No remarks"
            Remarks_Linke.append(remarks_in_speech)
            Reden_Linke[-1] = moderation_split[0]
        if element == "(AfD):":
            Reden_AfD.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_AfD[-1])
            remarks_in_speech = get_remarks(moderation_split[0])
            if remarks_in_speech.empty:
                remarks_in_speech['remark_text'] = "No remarks"
                remarks_in_speech['remark_class'] = "No remarks" 
                remarks_in_speech['remark_party'] = "No remarks"
            Remarks_AfD.append(remarks_in_speech)
            Reden_AfD[-1] = moderation_split[0]
        if element == "(BÜNDNIS 90/DIE GRÜNEN):":
            Reden_Gruene.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_Gruene[-1])
            remarks_in_speech = get_remarks(moderation_split[0])
            if remarks_in_speech.empty:
                remarks_in_speech['remark_text'] = "No remarks"
                remarks_in_speech['remark_class'] = "No remarks" 
                remarks_in_speech['remark_party'] = "No remarks"
            Remarks_Gruene.append(remarks_in_speech)
            Reden_Gruene[-1] = moderation_split[0]
        if element == "(CDU/CSU):":
            Reden_CDU.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_CDU[-1])
            remarks_in_speech = get_remarks(moderation_split[0])
            if remarks_in_speech.empty:
                remarks_in_speech['remark_text'] = "No remarks"
                remarks_in_speech['remark_class'] = "No remarks" 
                remarks_in_speech['remark_party'] = "No remarks"
            Remarks_CDU.append(remarks_in_speech)
            Reden_CDU[-1] = moderation_split[0]
        if element == "(FDP):":
            Reden_FDP.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_FDP[-1])
            remarks_in_speech = get_remarks(moderation_split[0])
            if remarks_in_speech.empty:
                remarks_in_speech['remark_text'] = "No remarks"
                remarks_in_speech['remark_class'] = "No remarks" 
                remarks_in_speech['remark_party'] = "No remarks"
            Remarks_FDP.append(remarks_in_speech)
            Reden_FDP[-1] = moderation_split[0]
        if element == "(FRAKTIONSLOS):":
            Reden_Fraktionslos.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_Fraktionslos[-1])
            remarks_in_speech = get_remarks(moderation_split[0])
            if remarks_in_speech.empty:
                remarks_in_speech['remark_text'] = "No remarks"
                remarks_in_speech['remark_class'] = "No remarks" 
                remarks_in_speech['remark_party'] = "No remarks"
            Remarks_Fraktionslos.append(remarks_in_speech)
            Reden_Fraktionslos[-1] = moderation_split[0]
        if element == "(SPD):":
            Reden_SPD.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_SPD[-1])
            remarks_in_speech = get_remarks(moderation_split[0])
            if remarks_in_speech.empty:
                remarks_in_speech['remark_text'] = "No remarks"
                remarks_in_speech['remark_class'] = "No remarks" 
                remarks_in_speech['remark_party'] = "No remarks"
            Remarks_SPD.append(remarks_in_speech)
            Reden_SPD[-1] = moderation_split[0]

    return Reden_AfD, Reden_CDU, Reden_FDP, Reden_Fraktionslos, Reden_Gruene, Reden_Linke, Reden_SPD, Remarks_Linke, Remarks_AfD, Remarks_Gruene, Remarks_CDU, Remarks_FDP, Remarks_Fraktionslos, Remarks_SPD 


def  convert_text(text):
    return text

def  delete_elastic_index():
    es.options(ignore_status=[400,404]).indices.delete(index=index_protokolle)

def fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher,remarks):
    #print("Verarbeite Dokument: ", document['dokumentnummer'])
    doc = {
        'Dokumentnummer': meeting_id,
        'Sprecher': name_speaker,
        'Partei': party,
        'Datum': date,
        'Titel': title,
        'Organ': publisher,
        'Text': element,
        'Remarks': element
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
    es.index(index=missing_index,  body=doc)

def fill_loop(dictionary):

    for document in dictionary['documents']:
        if "text" not in document:
            continue
        meeting_id = document['dokumentnummer']
        date = document['datum'],
        title = document['titel'],
        publisher = document['herausgeber']


        missing_DIELINKE, missing_CDUCSU, missing_FDP, missing_SPD, missing_GRUENE, missing_FRAKTIONSLOS, missing_AFD, missing_mp_stats = get_missing_mps(document['text'])

        #fill_elastic_missing(meeting_id,date,title,missing_DIELINKE, missing_CDUCSU, missing_FDP, missing_SPD, missing_GRUENE, missing_FRAKTIONSLOS, missing_AFD)
        
        Reden_AfD, Reden_CDU, Reden_FDP, Reden_Fraktionslos, Reden_Gruene, Reden_Linke, Reden_SPD, Remarks_Linke, Remarks_AfD, Remarks_Gruene, Remarks_CDU, Remarks_FDP, Remarks_Fraktionslos, Remarks_SPD = Preprocessing(str(document['text']))
        
        for element in Reden_AfD:
            index = Reden_AfD.index(element)
            name_speaker = element.split()[:2]
            party="AfD"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher, Remarks_AfD[index])


        for element in Reden_CDU:
            name_speaker = element.split()[:2]
            party="CDU"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher, Remarks_CDU[index])

        for element in Reden_FDP:
            name_speaker = element.split()[:2]
            party="FDP"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher, Remarks_FDP[index])
    
        for element in Reden_Fraktionslos:
            name_speaker = element.split()[:2]
            party="Fraktionslos"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher, Remarks_Fraktionslos[index])
    
        for element in Reden_Gruene:
            name_speaker = element.split()[:2]
            party="Bündnis 90/Die Grünen"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher, Remarks_Gruene[index])
    
        for element in Reden_Linke:
            name_speaker = element.split()[:2]
            party="Die Linke"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher, Remarks_Linke[index])
        
        for element in Reden_SPD:
            name_speaker = element.split()[:2]
            party="SPD"
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher, Remarks_SPD[index])
       

    es.indices.refresh(index=index_protokolle)
    es.indices.refresh(index=missing_index)
    result = es.count(index=index_protokolle)
    geladeneProtkolle = result['count']
    print("Anzahl Protokolle", geladeneProtkolle)

es = Elasticsearch("http://localhost:9200",
    verify_certs=False, timeout=60,retry_on_timeout =True, max_retries = 5,use_ssl=False) # Security not enabled
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
