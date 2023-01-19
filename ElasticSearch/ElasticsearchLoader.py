from elasticsearch import Elasticsearch
import requests
import re
import re
import spacy


nlp = spacy.load("de_core_news_sm")

#define index names for import into elasticsearch

index_protokolle = "f3_test_protokolle"
missing_index = "f3_test_missing"
index_remarks = "f3_test_remarks"

# Function which returns last words

def lastWords(string):

    lis = list(string.split(" "))
    concat = " ".join(lis[-3:])

    return concat


# This Function expects a meeting document and returns the Names of the missing MPs. 
# The Names are stored in lists that are sorted by party. The function also returns the Number
# of missing MPs per Party 

def get_missing_mps(document):

    #create helper arrays

    DIELINKE = []
    CDUCSU= []
    FDP= []
    SPD= []
    GRUENE= []
    FRAKTIONSLOS= []
    AFD= []

     
    document = document.replace(" .",".")                   #This split is done to seperate the Anlagen from the rest of the text, it is the only consistently working string we know of
    split = document.split("Stenografischen Bericht")
    

    #This split is done to cut the rest of the file from the missing MPs part of the anlagen. 
    #If there is no Anlage 2, we have found that splitting on "satzweiss.com" yields good results too
    
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

        #Assign MP to Die Linke

        if "DIE LINKE" in element:
            element = element.split("DIE LINKE")
            try:
                #Names are giving last name first and first name second, therefore they are switched here

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)
            except:
                name = element[0]
            DIELINKE.append(name)

        #Assign MP to CDU/CSU
            
        if "CDU/CSU" in element:
            element = element.split("CDU/CSU")
            try:
                #Names are giving last name first and first name second, therefore they are switched here

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)
            except:
                name = element[0]
            CDUCSU.append(name)

        #Assign MP to FDP

        if "FDP" in element:
            element = element.split("FDP")
            try:
                #Names are giving last name first and first name second, therefore they are switched here

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)
            except:
                name = element[0]
            FDP.append(name)
           
        #Assign MP to SPD

        if "SPD" in element:
            element = element.split("SPD")
            try:
                #Names are giving last name first and first name second, therefore they are switched here

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)
            except:
                name = element[0]
            SPD.append(name)
        
        #Assign MP to Bündnis 90/ Die Grünen

        if "BÜNDNIS 90/" in element:
            element = element.split("BÜNDNIS 90/")
            try:    
                #Names are giving last name first and first name second, therefore they are switched here

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)
            except:
                name = element[0]
            GRUENE.append(name)

        #Assign MP to Bündnis 90/ Die Grünen
        
        if "fraktionslos" in element:
            element = element.split("fraktionslos")
            try:    
                #Names are giving last name first and first name second, therefore they are switched here

                switchnames = element[0].split(",")
                name = switchnames[1]+" "+switchnames[0]
                print(name)
            except:
                name = element[0]
            FRAKTIONSLOS.append(name)

        #Assign MP to AfD

        if "AfD" in element:
            element = element.split("AfD")
            try:
                #Names are giving last name first and first name second, therefore they are switched here

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


# This is a helper Function, that returns a list with the parties, that are in a piece of text

def get_party(element):

    remarking_party = []
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

    return remarking_party


# This Function is used to get the Remarks from a specific speech. It expects the text of the speech as well as some data about the speaker and the party etc. 
# The function extracts reactions like "Beifall" or "Heiterkeit" as well as thematic reactions by specific MPs and adds them to a seperate elastic search index. 
# It also adds information about the reacting MP like Name or Party which enables us to link the reaction to a specific speech

def get_remarks(meeting_id,date,text, name_speaker, party):

    parties = ['LINKE', 'BÜNDNIS 90', 'CDU/CSU', 'SPD', 'FDP', 'AfD', 'fraktionslos']
    remark_class = []
    remarks = []

   # This should find all sentences in the text that contain square brackets with letters in them. 
   # They indicated, that a party has been assigned to a speaker (example: Robert Habeck [BÜNDNIS90/DIEGRUENEN])
    potentialremarks = re.findall( '\((\n*?|[^)]*)\)', text)        

    for element in potentialremarks:
        if len(element) > 9:
            if any(party in element for party in parties):
                remarks.append(element)
    
    for element in remarks:
        remark_class = []
        remarking_parties = []
        remarking_persons =""
        party_remarking_person = ""
        cleaned_text = ""

        # This assigns the "non thematic reactions" in the speech to parties
        if "Beifall" in element:
            remark_class.append("Beifall")
            remarking_parties.append(get_party(element))

        if "Lachen" in element:
            remark_class.append("Lachen")
            remarking_parties.append(get_party(element))

        if "Heiterkeit" in element:
            remark_class.append("Heiterkeit")
            remarking_parties.append(get_party(element))

        if "Zuruf" in element:
            remark_class.append("Zuruf")
            remarking_parties.append(get_party(element))
        
        # ******************************************************
        # Here the part concerning thematic reactions starts
        # ******************************************************

        if "[SPD]:" in element:
            remark_class.append("Thematischer Zwischenruf")
            party_remarking_person = "SPD"

            list = element.split()
            index = list.index('[SPD]:')
            try:
                remarking_persons = str(list[index - 2] +" "+ list[index - 1])      #Names of remarking persons are switched because they are stated last name first
            except:
                remarking_persons = "None"

            # This extracts only the text of the speech without the name and ther party of the MP giving it
            cleaned_list = element.split('[SPD]:')                          
            cleaned_text = cleaned_list.pop()


        if "[CDU/CSU]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "CDU/CSU"

            list = element.split()
            index = list.index('[CDU/CSU]:')
            try:
                remarking_persons = str(list[index - 2] +" "+ list[index - 1])      #Names of remarking persons are switched because they are stated last name first
            except:
                remarking_persons = "None"

            # This extracts only the text of the speech without the name and ther party of the MP giving it
            cleaned_list = element.split('[CDU/CSU]:')
            cleaned_text = cleaned_list.pop()


        if "[AfD]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "AfD"

            list = element.split()
            index = list.index('[AfD]:')
            try:
                remarking_persons = str(list[index - 2] +" "+ list[index - 1])       #Names of remarking persons are switched because they are stated last name first
            except:
                remarking_persons = "None"
            
            # This extracts only the text of the speech without the name and ther party of the MP giving it
            cleaned_list = element.split('[AfD]:')
            cleaned_text = cleaned_list.pop()
           

        if "[FDP]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "FDP"

            list = element.split()
            index = list.index('[FDP]:')
            try:
                remarking_persons = str(list[index - 2] +" "+ list[index - 1])      #Names of remarking persons are switched because they are stated last name first
            except:
                remarking_persons = "None"

            # This extracts only the text of the speech without the name and ther party of the MP giving it
            cleaned_list = element.split('[FDP]:')
            cleaned_text = cleaned_list.pop()


        if "[BÜNDNIS 90/DIE GRÜNEN]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "Bündnis 90/Die Grünen"

            remarking_parties = []
            list = element.split()
            print(list)
            index = list.index('[BÜNDNIS')
            try:
                remarking_persons = str(list[index - 2] +" "+ list[index - 1])      #Names of remarking persons are switched because they are stated last name first
            except:
                remarking_persons = "None"

            # This extracts only the text of the speech without the name and ther party of the MP giving it
            cleaned_list = element.split('[BÜNDNIS 90/DIE GRÜNEN]:')
            cleaned_text = cleaned_list.pop()
           

        if "[DIELINKE]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "Die Linke"

            list = element.split()
            index = list.index('[DIELINKE]:')
            try:
                remarking_persons = str(list[index - 2] +" "+ list[index - 1])      #Names of remarking persons are switched because they are stated last name first
            except:
                remarking_persons = "None"

            # This extracts only the text of the speech without the name and ther party of the MP giving it
            cleaned_list = element.split('[DIELINKE]:')
            cleaned_text = cleaned_list.pop()
        

        if "[DIE LINKE]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "Die Linke"

            list = element.split()
            
            try:
                index = list.index('[DIE LINKE]:')
                remarking_persons = str(list[index - 2] +" "+ list[index - 1])      #Names of remarking persons are switched because they are stated last name first
            except:
                remarking_persons = "None"

            # This extracts only the text of the speech without the name and ther party of the MP giving it
            cleaned_list = element.split('[DIE LINKE]:')
            cleaned_text = cleaned_list.pop()
            

        if "[FRAKTIONSLOS]:" in element:
            remark_class.append("Thematischer Zwischenruf")

            party_remarking_person = "Fraktionslos"

            list = element.split()
            index = list.index('[FRAKTIONSLOS]:')
            try:
                remarking_persons = str(list[index - 2] +" "+ list[index - 1])      #Names of remarking persons are switched because they are stated last name first
            except:
                remarking_persons = "None"
            
            # This extracts only the text of the speech without the name and ther party of the MP giving it
            cleaned_list = element.split('[FRAKTIONSLOS]:')
            cleaned_text = cleaned_list.pop()


        fill_elastic_remarks(meeting_id,date,element,name_speaker,party, remark_class,remarking_parties, remarking_persons,party_remarking_person, cleaned_text)
        es.indices.refresh(index=index_remarks)


# This Function expects an entire document and preprocesses it. It splits the document into speeches done by different MPs. One speech will be one document in elasticsearch
# It splits moderation from other parts of the speech and assigns a speaker as well as a party to the document

def Preprocessing(document):

    meeting_content = str(document)
    meeting_content = " ".join(line.strip() for line in meeting_content.splitlines())
    meeting_content = meeting_content.replace("- ","")
    meeting_content = re.sub('\n', ' ', meeting_content) 

    # This splits the document on the party names in brackets. This is the best split we could find, as the speeches start with the speakers name followed by his or her party
    # in brackets. Example: "Robert Habeck (BÜNDNIS90/DIEGRÜNEN)"
    party_split = re.split("(\(DIE LINKE\):|\(AfD\):|\(BÜNDNIS 90/DIE GRÜNEN\):|\(CDU/CSU\):|\(FDP\):|\(FRAKTIONSLOS\):|\(SPD\):)", meeting_content)     #Splitting text into talking points

    Reden_Linke = []
    Reden_AfD = []
    Reden_Gruene = []
    Reden_CDU = []
    Reden_FDP = []
    Reden_Fraktionslos = []
    Reden_SPD = []

    # Iterates over the split speeches and cleans them up, speerating moderation etc.
    for idx, element in enumerate(party_split):

        if element == "(DIE LINKE):":

            Reden_Linke.append(lastWords(party_split[idx-1])+" "+party_split[idx]+" "+party_split[idx+1])
            moderation_split = re.split("Präsident Dr. Wolfgang Schäuble:|Vizepräsident Dr. Hans-Peter Friedrich:", Reden_Linke[-1])    # This splits on moderation to find the end of the speech. The split texts have been decided on by experimentation
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


    # This Function imports the protocols into elasticsearch

def fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher):

    doc = {
        'Dokumentnummer': meeting_id,
        'Sprecher': name_speaker,
        'Partei': party,
        'Datum': date,
        'Titel': title,
        'Organ': publisher,
        'Text': element,
    }

    idDokumentennummer = re.sub("/", "", meeting_id)
    print("idDokumentennummer: " + idDokumentennummer)
    resp = es.index(index=index_protokolle,  body=doc)


# This function imports the remarks into the remarks index of elastic search

def fill_elastic_remarks(meeting_id,date,element,name_speaker,party, remark_class,remarking_parties, remarking_persons, party_remarking_person, cleaned_text):
    #print("Verarbeite Dokument: ", document['dokumentnummer'])
    doc = {
        'Dokumentnummer': meeting_id,
        'Sprecher der Rede': name_speaker,
        'Partei des Sprechers der Rede': party,
        'Datum': date,
        'Remark Class': remark_class,
        'Remarking Parties': remarking_parties,
        'Text': element,
        'Remarking Persons' : remarking_persons,
        'Party Remarking Person': party_remarking_person,
        'Remark Text': cleaned_text
    }

    idDokumentennummer = re.sub("/", "", meeting_id)
    print("idDokumentennummer: " + idDokumentennummer)
    resp = es.index(index=index_remarks,  body=doc)


# This function imports the missing mps into the missing mps index of elastic search

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


# This function fills elasticsearch with the missing mps and the documents. The remarks are imported in the resprective get_remarks function. It is also the main loop

def fill_loop(dictionary):

    #Iterated over all the documents that were exported from the Bundestag API

    for document in dictionary['documents']:
        if "text" not in document:
            continue
        meeting_id = document['dokumentnummer']
        date = document['datum'],
        title = document['titel'],
        publisher = document['herausgeber']

        missing_DIELINKE, missing_CDUCSU, missing_FDP, missing_SPD, missing_GRUENE, missing_FRAKTIONSLOS, missing_AFD, missing_mp_stats = get_missing_mps(document['text'])
        fill_elastic_missing(meeting_id,date,title,missing_DIELINKE, missing_CDUCSU, missing_FDP, missing_SPD, missing_GRUENE, missing_FRAKTIONSLOS, missing_AFD)
        
        Reden_AfD, Reden_CDU, Reden_FDP, Reden_Fraktionslos, Reden_Gruene, Reden_Linke, Reden_SPD= Preprocessing(str(document['text'])) # Preprocesses documents and splits them
        
        for element in Reden_AfD:
            name_speaker = element.split()[:2]
            party="AfD"
            get_remarks(meeting_id,date,element, name_speaker, party)
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)


        for element in Reden_CDU:
            name_speaker = element.split()[:2]
            party="CDU"
            get_remarks(meeting_id,date,element, name_speaker, party)
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)

        for element in Reden_FDP:
            name_speaker = element.split()[:2]
            party="FDP"
            get_remarks(meeting_id,date,element, name_speaker, party)
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
    
        for element in Reden_Fraktionslos:
            name_speaker = element.split()[:2]
            party="Fraktionslos"
            get_remarks(meeting_id,date,element, name_speaker, party)
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
    
        for element in Reden_Gruene:
            name_speaker = element.split()[:2]
            party="Bündnis 90/Die Grünen"
            get_remarks(meeting_id,date,element, name_speaker, party)
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
    
        for element in Reden_Linke:
            name_speaker = element.split()[:2]
            party="Die Linke"
            get_remarks(meeting_id,date,element, name_speaker, party)
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
        
        for element in Reden_SPD:
            name_speaker = element.split()[:2]
            party="SPD"
            get_remarks(meeting_id,date,element, name_speaker, party)
            fill_elastic(element,name_speaker,meeting_id,party,date,title,publisher)
       

    es.indices.refresh(index=index_protokolle) 
    es.indices.refresh(index=missing_index)
    es.indices.refresh(index=index_remarks)

    result = es.count(index=index_protokolle)
    geladeneProtkolle = result['count']
    print("Anzahl Protokolle", geladeneProtkolle)

es = Elasticsearch("http://localhost:9200",
    verify_certs=False, timeout=60,retry_on_timeout =True, max_retries = 5,use_ssl=False) # Security not enabled
api_url = "https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.datum.start=2021-09-26&apikey=ECrwIai.ErBmVaihLIzqiqu9DqNoVFVvUysTzDwuOo"

response = requests.get(api_url) # Get Documents from the Bundestag API

dictionary = response.json()


vorhandeneDokumente = dictionary['numFound']
print("Gesamtanzahl vorhandener Dokumente: ", vorhandeneDokumente)

fill_loop(dictionary)

oldCursor = ""
cursor = dictionary['cursor']

while len(cursor) > 0 and cursor != oldCursor: # if new = old, end
    cursor = re.sub("\/", "%2F", cursor)
    cursor = re.sub("\+", "%2B", cursor)
    weiterlesen_url = api_url + "&cursor=" + cursor
    response = requests.get(weiterlesen_url)
    dictionary = response.json()
    fill_loop(dictionary)
    
    oldCursor = cursor
    cursor = dictionary['cursor']
