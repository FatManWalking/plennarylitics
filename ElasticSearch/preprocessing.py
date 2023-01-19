import xml.etree.ElementTree as ET
import re
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import os

# Function which returns last words

def lastWords(string):

# split by space and converting
# string to list and
    lis = list(string.split(" "))
    concat = " ".join(lis[-3:])

# returning last 3 elements in list
    return concat

def Preprocessing(document):

#Read xml Files
#filename = '../Data/19026.xml'

    tree = ET.parse(document)

    root = tree.getroot()


    for content in root.iter('TEXT'):
        meeting_content = content.text

    meeting_content = " ".join(line.strip() for line in meeting_content.splitlines())
    meeting_content = meeting_content.replace("- ","")

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