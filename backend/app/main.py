from typing import Union, Dict, List, Tuple, Optional, Any, Mapping
from enum import Enum
import json
from fastapi import FastAPI
from fastapi import Query as FastAPIQuery
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

from .routers import speech, missing, remark

from .query_builder import Query as Query
from .utils import count_remarked_party

# TODO: get indices as environment variables
missing_index = "final_missing"
speech_index = "final_speeches"
remark_index = "final_remarks"

app = FastAPI()

origins = [
    "http://localhost:*",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Simple header we can put in front of the API
headers = {"Access-Control-Allow-Origin": "*"}


class Party(Enum):
    """
    Enum for parties
    When we query by party we could use the following enum to make sure we only query for valid parties
    """

    SPD = "SPD"
    CDUCSU = "CDU"
    GRUENE = "GRÜNE"
    FDP = "FDP"
    DIELINKE = "DIE LINKE"
    AFD = "AfD"
    FRAKTIONSLOS = "Fraktionslos"


def get_es_client():
    """
    Establish connection to Elasticsearch
    :return: Elasticsearch client
    """
    return Elasticsearch(
        "http://elasticsearch:9200",
        verify_certs=False,
        timeout=60,
        retry_on_timeout=True,
        max_retries=5,
    )


# Tested
@app.get("/")
def read_root():
    """
    :return: Simple message to check if the API is up and running
    Show available endpoints
    """
    return {
        "Plennarylitics Backend": "Available",
        "Docs at": "localhost:8000/docs",
        "Health at": "localhost:8000/health",
        "Connection test to Elasticsearch at": "localhost:8000/health/es",
        "Sample search at": "localhost:8000/health/test",
    }


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
        search_object = {"match_all": {}}
        index_name = "f2*"
        res = es.search(index=index_name, query=search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    return res


# Tested [speeches_v2]
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


# TESTED
@app.get("/test/{topic}")
def test(topic: str):
    """
    :param topic: topic to be queried
    :return: response from Elasticsearch
    """

    # Test query
    es = get_es_client()
    if es is not None:
        query = Query()
        query.add_topic(topic=topic)

        # Log the query
        print(f"query: {query.get_query()}")
        # Searches for all speeches between the given dates in the speech index
        res = es.search(index=speech_index, query=query.get_query()["query"])
    else:
        return {"Error": "Elasticsearch is not available"}

    return res


# TESTED
@app.get("/speeches")
def get_speeches(
    keyword: Optional[str] = None,
    party: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    speaker: Optional[str] = None,
):
    """
    :param q: search query parameters
    :return: response from Elasticsearch
    """
    parameters = {
        "topic": keyword,
        "party": party,
        "date": [from_date, to_date],
        "speaker": speaker,
    }

    # Test query
    es = get_es_client()
    if es is not None:
        query = Query()

        # Add parameters to query
        for key, value in parameters.items():
            if value is not None:
                if key == "date":
                    query.add_date(from_date=value[0], to_date=value[1])
                else:
                    # dynamic method call
                    getattr(query, f"add_{key}")(value)

        # Log the query
        print(f"query: {query.get_query()}")
        # Searches for all speeches between the given dates in the speech index
        res = es.search(index=speech_index, query=query.get_query()["query"])
    else:
        return {"Error": "Elasticsearch is not available"}

    return res


# Tested [speeches_v2]
@app.get("/test_querybuilder/{from_date}/{to_date}")
def test_querybuilder(from_date: str, to_date: str):
    """
    :param date: date range to be queried
    :return: response from Elasticsearch
    """

    # Test query
    es = get_es_client()
    if es is not None:
        query = Query()
        query.add_date(from_date=from_date, to_date=to_date)

        # Log the query
        print(f"query: {query.get_query()}")
        # Searches for all speeches between the given dates in the speech index
        res = es.search(index=speech_index, query=query.get_query()["query"])
    else:
        return {"Error": "Elasticsearch is not available"}

    return res


@app.get("/remarks")
def get_remarks():
    """
    :return: response from Elasticsearch
    """

    # Test query
    es = get_es_client()
    if es is not None:

        query = {
            "aggs": {
                "0": {
                    "terms": {
                        "field": "Party Remarking Person.keyword",
                        "order": {"_count": "desc"},
                        "size": 8,
                    },
                    "aggs": {
                        "1": {
                            "terms": {
                                "field": "Partei des Sprechers der Rede.keyword",
                                "order": {"_count": "desc"},
                                "size": 8,
                            }
                        }
                    },
                }
            },
            "size": 0,
            "script_fields": {},
            "stored_fields": ["*"],
            "runtime_mappings": {},
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                            "range": {
                                "Datum": {
                                    "format": "strict_date_optional_time",
                                    "gte": "2008-03-03T13:14:06.395Z",
                                    "lte": "2023-03-03T13:14:06.395Z",
                                }
                            }
                        }
                    ],
                    "should": [],
                    "must_not": [
                        {"match_phrase": {"Party Remarking Person.keyword": "None"}}
                    ],
                }
            },
        }

        # Log the query
        print(f"query: {query}")
        # Searches for all speeches between the given dates in the speech index
        res = es.search(index=remark_index, query=query)

        # get the results
        # res = count_remarked_party(res)

    else:
        return {"Error": "Elasticsearch is not available"}

    return res


# Tested [missing_v2]
@app.get("/missing_mp/{mp_name}")
def test_mp(mp_name: str):
    """
    :param mp_name: name of the MP to be queried
    :return: response from Elasticsearch
    """

    # Test query
    es = get_es_client()
    if es is not None:
        query = Query()
        query.add_missing_mp_name(mp_name=mp_name)

        # Log the query
        print(f"query: {query.get_query()}")
        # Searches for all speeches between the given dates in the speech index
        res = es.search(index=missing_index, query=query.get_query()["query"])
    else:
        return {"Error": "Elasticsearch is not available"}

    return res


@app.get("/get_missing_by_date/{date}")
def missing_date(date: str):
    """
    :param index_name: name of the index to be queried
    #TODO: add query as a parameter
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    returns list of missing mps for every party on a specific date
    """

    es = get_es_client()
    if es is not None:
        search_object = {"query": {"range": {"Datum": {"gte": date}}}}

        res = es.search(index="bjoerns_test_missing", body=search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back

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
            "multi_match": {
                "query": mp_name,
                "type": "phrase_prefix",
                "fields": ["Remarking Persons"],
            },
            "size": 10000,
        }

        res = es.search(index="bjoerns_test_remarks", query=search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res


@app.get("/get_remarks_by_speaker_of_speech/{mp_name}")
def remarks_speaker(mp_name: str):
    """
    :param index_name: name of the index to be queried
    #TODO: add query as a parameter
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    """

    es = get_es_client()
    if es is not None:
        search_object = {
            "query": {
                "multi_match": {
                    "query": mp_name,
                    "type": "phrase_prefix",
                    "fields": ["Sprecher der Rede"],
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


@app.get("/get_remarks_by_party_of_speaker/{party_name}")
def remarks_speaker_party(party_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns remarks to speeches that were given by member of specific party (the speech not the remark)
    """

    es = get_es_client()
    if es is not None:
        search_object = {
            "query": {
                "multi_match": {
                    "query": party_name,
                    "type": "phrase_prefix",
                    "fields": ["Partei des Sprechers der Rede"],
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


@app.get("/get_remarks_by_party_of_remarker/{party_name}")
def remarks_remarker_party(party_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns remarks to speeches that were made by member of specific party (the remark, not the speech)
    """

    es = get_es_client()
    if es is not None:
        search_object = {
            "query": {
                "multi_match": {
                    "query": party_name,
                    "type": "phrase_prefix",
                    "fields": ["Party Remarking Person"],
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


@app.get("/get_missing_mps_by_party/{party_name}")
def missing_party(party_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns list of all missing MPs for all meetings in the database
    """

    # Test query
    es = get_es_client()
    if es is not None:
        if party_name == "CDU":
            search_object = {
                "query": {"multi_match": {"fields": ["missing_CDUCSU"], "size": 10000}},
                "size": 0,
            }
        if party_name == "SPD":
            search_object = {
                "query": {"multi_match": {"fields": ["missing_SPD"], "size": 10000}},
                "size": 0,
            }
        if party_name == "AfD":
            search_object = {
                "query": {"multi_match": {"fields": ["missing_AfD"], "size": 10000}},
                "size": 0,
            }
        if party_name == "DIE LINKE":
            search_object = {
                "query": {
                    "multi_match": {"fields": ["missing_DIELINKE"], "size": 10000}
                },
                "size": 0,
            }
        if party_name == "FRAKTIONSLOS":
            search_object = {
                "query": {
                    "multi_match": {"fields": ["missing_FRAKTIONSLOS"], "size": 10000}
                },
                "size": 0,
            }
        if "GRUENEN" in party_name:
            search_object = {
                "query": {"multi_match": {"fields": ["missing_GRUENE"], "size": 10000}},
                "size": 0,
            }
        if "FDP" in party_name:
            search_object = {
                "query": {"multi_match": {"fields": ["missing_FDP"], "size": 10000}},
                "size": 0,
            }

            res = es.search(index=missing_index, body=search_object)
        else:
            res = {"Error": "Party not found"}

    else:
        print("Elasticsearch is not available")
        res = {"Error": "Elasticsearch is not available"}
        return {}

    # Number of hits we got back

    return res


@app.get("/get_speech_by_speaker/{mp_name}")
def speech_speaker(mp_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns speeches, that were given by a specific person
    """

    es = get_es_client()
    if es is not None:
        search_object = {
            "query": {
                "multi_match": {
                    "query": mp_name,
                    "type": "phrase_prefix",
                    "fields": ["Sprecher"],
                }
            },
            "size": 10000,
        }

        res = es.search(index=speech_index, body=search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res


@app.get("/get_speech_by_party/{party_name}")
def speech_party(party_name: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns speeches, that were given by members of a specific party
    """

    es = get_es_client()
    if es is not None:
        search_object = {
            "query": {
                "multi_match": {
                    "query": party_name,
                    "type": "phrase_prefix",
                    "fields": ["Partei des Sprechers der Rede"],
                }
            },
            "size": 10000,
        }

        res = es.search(index=speech_index, body=search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res


@app.get("/get_speech_by_date/{date}")
def speech_date(date: str):
    """
    :param index_name: name of the index to be queried
    :param query: query to be passed to Elasticsearch in the form of a dictionary e.g. {"match_all": {}} or {"match": {"title": "test"}}
    :return: response from Elasticsearch
    Returns speeches, that were given on a specific date
    """

    es = get_es_client()
    if es is not None:
        search_object = {"query": {"range": {"Datum": {"gte": date}}}}

        res = es.search(index=speech_index, body=search_object)
    else:
        print("Elasticsearch is not available")
        return {}

    # Number of hits we got back
    print(f"res: {res['hits']['total']['value']}")

    return res
