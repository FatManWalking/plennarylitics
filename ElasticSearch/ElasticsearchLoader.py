from elasticsearch import Elasticsearch
import requests
import re

def  convert_text(text):
    return text

def  delete_elastic_index():
    es.options(ignore_status=[400,404]).indices.delete(index=index_protokolle)

def fill_elastic(document):
    print("Verarbeite Dokument: ", document['dokumentnummer'])
    doc = {
        'Dokumentnummer': document['dokumentnummer'],
        'Datum': document['datum'],
        'Titel': document['titel'],
        'Organ': document['herausgeber'],
        #'Text': convert_text(document['text']),
        'Text': document['text']
    }

    idDokumentennummer = re.sub("/", "", document['dokumentnummer'])
    print("idDokumentennummer: " + idDokumentennummer)
    resp = es.index(index=index_protokolle, id=idDokumentennummer, document=doc)

es = Elasticsearch('http://localhost:9200') # Security not enabled
api_url = "https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.datum.start=2021-09-26&apikey=ECrwIai.ErBmVaihLIzqiqu9DqNoVFVvUysTzDwuOo"
index_protokolle = "protokolle"

delete_elastic_index() # ggf. vorhandener Index löschen
response = requests.get(api_url)
dictionary = response.json()
vorhandeneDokumente = dictionary['numFound']
print("Gesamtanzahl vorhandener Dokumente: ", vorhandeneDokumente)

for document in dictionary['documents']:
    fill_elastic(document)

oldCursor = ""
cursor = dictionary['cursor']

while len(cursor) > 0 and cursor != oldCursor: # wenn neu = alt dann ende
    cursor = re.sub("\/", "%2F", cursor)
    cursor = re.sub("\+", "%2B", cursor)
    weiterlesen_url = api_url + "&cursor=" + cursor
    response = requests.get(weiterlesen_url)
    dictionary = response.json()

    for document in dictionary['documents']:
        fill_elastic(document)

    oldCursor = cursor
    cursor = dictionary['cursor']

es.indices.refresh(index="protokolle")
result = es.count(index=index_protokolle)
geladeneProtkolle = result['count']
print("Anzahl Protokolle", geladeneProtkolle)

if vorhandeneDokumente == geladeneProtkolle:
    print("Alle Dokumente erfolgreich geladen")
else:
    print("Da ist was schiefgelaufen !!!")