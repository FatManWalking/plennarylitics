from typing import Union, Dict, List
from enum import Enum
import json
from fastapi import FastAPI
from elasticsearch import Elasticsearch

from .routers import speech, missing, remark

app = FastAPI()


class Party(Enum):
    SPD = "SPD"
    CDUCSU = "CDU"
    GRUENE = "GRÜNE"
    FDP = "FDP"
    DIELINKE = "DIE LINKE"
    AFD = "AfD"
    FRAKTIONSLOS = "Fraktionslos"


@app.get("/")
def read_root():
    return {
        "Plennarylitics Backend": "Available",
        "Docs at": "localhost:8000/docs",
        "Health at": "localhost:8000/health",
        "Connection test to Elasticsearch at": "localhost:8000/health/es",
        "Sample search at": "localhost:8000/health/test",
    }


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
        return {"Error": "Elasticsearch is not available"}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res


@app.get("/get_missing/{mp_name}")
def missing_mp(mp_name: str):
    """
    :param index_name: name of the index to be queried
    :return: response from Elasticsearch
    """

    es = get_es_client()
    if es is not None:
        # Query to find all documents where the selected MP is missing
        search_object = {
            "query": {
                "multi_match": {
                    "query": mp_name,
                    "type": "phrase_prefix",
                    "fields": [
                        "missing_AFD",
                        "missing_CDUCSU",
                        "missing_DIELINKE",
                        "missing_FDP",
                        "missing_SPD",
                        "missing_GRUENE",
                        "missing_FRAKTIONSLOS",
                    ],
                }
            },
            "highlight": {
                "fields": {
                    "missing_AFD": {},
                    "missing_CDUCSU": {},
                    "missing_DIELINKE": {},
                    "missing_FDP": {},
                    "missing_SPD": {},
                    "missing_GRUENE": {},
                    "missing_FRAKTIONSLOS": {},
                }
            },
            "size": 10000,
        }

        res = es.search(index="bjoerns_test_missing", body=search_object)
    else:
        return {"Error": "Elasticsearch is not available"}

    # Number of hits we got back
    print(f"res: {res}")

    return res


@app.get("/get_remarks_by_mp/{mp_name}")
def remarks_mp(mp_name: str):
    """
    :param index_name: name of the index to be queried
    #TODO: add query as a parameter
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    """

    # Test query
    es = get_es_client()
    if es is not None:
        search_object = {
            "query": {
                "multi_match": {
                    "query": mp_name,
                    "type": "phrase_prefix",
                    "fields": ["Remarking Persons"],
                }
            },
            "size": 10000,
        }

        res = es.search(index="bjoerns_test_remarks", body=search_object)
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
