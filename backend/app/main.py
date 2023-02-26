from typing import Union, Dict, List
import json
from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/search/{index_name}")
def search(index_name: str):
    """
    :param index_name: name of the index to be queried
    #TODO: add query as a parameter
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    """

    # Test query
    es = get_es_client()
    if es is not None:
        search_object = {"match_all": {}}
        res = es.search(index=index_name, query=search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

@app.get("/get_missing/{mp_name}")
def search(mp_name: str):
    """
    :param index_name: name of the index to be queried
    #TODO: add query as a parameter
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    """


    es = get_es_client()
    if es is not None:
        search_object =  {"query" : {
                                    "multi_match" : {
                                    "query":    mp_name, 
                                    "type":       "phrase_prefix",
                                    "fields": [ "missing_AFD", "missing_CDUCSU", "missing_DIELINKE", "missing_FDP", "missing_SPD", "missing_GRUENE", "missing_FRAKTIONSLOS" ] 
    }},
                                    "highlight": {
                                        "fields": {
                                            "missing_AFD": {},
                                            "missing_CDUCSU": {},
                                            "missing_DIELINKE" : {},
                                            "missing_FDP" : {},
                                            "missing_SPD" : {},
                                            "missing_GRUENE" : {},
                                            "missing_FRAKTIONSLOS" : {}
                                        }
                                    },
                                    "size": 10000      
        }

        res = es.search(index="bjoerns_test_missing", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

@app.get("/get_missing_by_date/{date}")
def search(date: str):
    """
    :param index_name: name of the index to be queried
    #TODO: add query as a parameter
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    returns list of missing mps for every party on a specific date
    """


    es = get_es_client()
    if es is not None:
        search_object =  {
          "query": {
            "range": {
              "Datum": {
                "gte": date
              }
            }
          }
        }

        res = es.search(index="bjoerns_test_missing", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res


@app.get("/get_remarks_by_mp/{mp_name}")
def search(mp_name: str):
    """
    :param index_name: name of the index to be queried
    #TODO: add query as a parameter
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    """

    # Test query
    es = get_es_client()
    if es is not None:
        search_object =  {"query" : {
                                    "multi_match" : {
                                    "query":    mp_name, 
                                    "type":       "phrase_prefix",
                                    "fields": ["Remarking Persons"] 
    }},
                        
                                    "size": 10000      
        }
                                
        

        res = es.search(index="bjoerns_test_remarks", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

@app.get("/get_remarks_by_speaker_of_speech/{mp_name}")
def search(mp_name: str):
    """
    :param index_name: name of the index to be queried
    #TODO: add query as a parameter
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    """

    es = get_es_client()
    if es is not None:
        search_object =  {"query" : {
                                    "multi_match" : {
                                    "query":    mp_name, 
                                    "type":       "phrase_prefix",
                                    "fields": ["Sprecher der Rede"] 
    }},
                        
                                    "size": 10000      
        }
                                
        

        res = es.search(index="bjoerns_test_remarks", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

@app.get("/get_remarks_by_party_of_speaker/{party_name}")
def search(party_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns remarks to speeches that were given by member of specific party (the speech not the remark)
    """

    es = get_es_client()
    if es is not None:
        search_object =  {"query" : {
                                    "multi_match" : {
                                    "query":    party_name, 
                                    "type":       "phrase_prefix",
                                    "fields": ["Partei des Sprechers der Rede"] 
    }},
                        
                                    "size": 10000      
        }
                                
        

        res = es.search(index="bjoerns_test_remarks", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

@app.get("/get_remarks_by_party_of_remarker/{party_name}")
def search(party_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns remarks to speeches that were made by member of specific party (the remark, not the speech)
    """

    es = get_es_client()
    if es is not None:
        search_object =  {"query" : {
                                    "multi_match" : {
                                    "query":    party_name, 
                                    "type":       "phrase_prefix",
                                    "fields": ["Party Remarking Person"] 
    }},
                        
                                    "size": 10000      
        }
                                
        

        res = es.search(index="bjoerns_test_remarks", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res


@app.get("/get_missing_mps_by_party/{party_name}")

def search(party_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns list of all missing MPs for all meetings in the database
    """

    # Test query
    es = get_es_client()
    if es is not None:
      if party_name == "CDU/CSU":
        search_object =  {"query" : {
                                    "multi_match" : { 
                                    "fields": ["missing_CDUCSU"],
                                    "size": 10000
    }},
                        
                                    "size": 0   
        }
      if party_name == "SPD":
        search_object =  {"query" : {
                                    "multi_match" : { 
                                    "fields": ["missing_SPD"],
                                    "size": 10000
    }},
                        
                                    "size": 0   
        }
      if party_name == "AfD":
        search_object =  {"query" : {
                                    "multi_match" : { 
                                    "fields": ["missing_AfD"],
                                    "size": 10000
    }},
                        
                                    "size": 0   
        }
      if party_name == "DIE LINKE":
        search_object =  {"query" : {
                                    "multi_match" : { 
                                    "fields": ["missing_DIELINKE"],
                                    "size": 10000
    }},
                        
                                    "size": 0   
        }
      if party_name == "FRAKTIONSLOS":
        search_object =  {"query" : {
                                    "multi_match" : { 
                                    "fields": ["missing_FRAKTIONSLOS"],
                                    "size": 10000
    }},
                        
                                    "size": 0   
        }
      if "GRUENEN" in party_name:
        search_object =  {"query" : {
                                    "multi_match" : { 
                                    "fields": ["missing_GRUENE"],
                                    "size": 10000
    }},
                        
                                    "size": 0   
        }
      if "FDP" in party_name:
        search_object =  {"query" : {
                                    "multi_match" : { 
                                    "fields": ["missing_FDP"],
                                    "size": 10000
    }},
                        
                                    "size": 0   
        }
                                
        

        res = es.search(index="bjoerns_test_missing", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

@app.get("/get_speech_by_speaker/{mp_name}")
def search(mp_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns speeches, that were given by a specific person
    """

    es = get_es_client()
    if es is not None:
        search_object =  {"query" : {
                                    "multi_match" : {
                                    "query":    mp_name, 
                                    "type":       "phrase_prefix",
                                    "fields": ["Sprecher"] 
    }},
                        
                                    "size": 10000      
        }
                                
        

        res = es.search(index="bjoerns_test_speeches", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

@app.get("/get_speech_by_party/{party_name}")
def search(party_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns speeches, that were given by members of a specific party
    """

    es = get_es_client()
    if es is not None:
        search_object =  {"query" : {
                                    "multi_match" : {
                                    "query":    party_name, 
                                    "type":       "phrase_prefix",
                                    "fields": ["Partei des Sprechers der Rede"] 
    }},
                        
                                    "size": 10000      
        }
                                
        

        res = es.search(index="bjoerns_test_speeches", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

@app.get("/get_speech_by_date/{date}")
def search(date: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns speeches, that were given on a specific date
    """

    es = get_es_client()
    if es is not None:
        search_object =  {
          "query": {
            "range": {
              "Datum": {
                "gte": date
              }
            }
          }
        }
                                
        

        res = es.search(index="bjoerns_test_speeches", body =search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res

def get_es_client():
    return Elasticsearch(
        "http://elasticsearch:9200",
        verify_certs=False,
        timeout=60,
        retry_on_timeout=True,
        max_retries=5,
    )


@app.get("/health/es")
def health_es():
    """
    Check if Elasticsearch is available
    :return: Elasticsearch version
    """
    es = get_es_client()
    if es is not None:
        return es.info()
    else:
        return {"Elasticsearch": "is not available"}


@app.get("/health/test")
def query_es():
    """
    We can use the elasticsearch_dsl library to build the query
    Establish connection to Elasticsearch and then pass the query
    Here we simply pass a match_all query to test if all is well

    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"query": {"match_all": {}}} or {"query": {"match": {"title": "test"}}}
    :param index_name: name of the index to be queried
    :return: response from Elasticsearch
    """

    es = get_es_client()
    if es is not None:
        search_object = {"query": {"match_all": {}}}
        index_name = "f2*"
        res = es.search(index=index_name, body=json.dumps(search_object))
    else:
        print("Elasticsearch is not available")
        return {}

    return res
