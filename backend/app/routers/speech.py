# Router to get all speeches from a specific MP or party (with optional date range or other filters)
#
from typing import Union

from fastapi import APIRouter

router = APIRouter()

# TODO: add more filters
# Using the optional query parameters allows us to filter by date, MP, party, etc. without having to create a new endpoint for each combination
# And dynamically create the query based on the parameters passed while keeping the URL clean, e.g. /get_speeches?mp_name=Max%20Mustermann&date_from=2020-01-01&date_to=2020-12-31
@router.get("/get_speeches", tags=["speeches"])
async def get_speeches(
    mp_name: Union[str, None] = None,
    date_from: Union[str, None] = None,
    date_to: Union[str, None] = None,
):
    """
    :param index_name: name of the index to be queried

    :param mp_name: name of the MP to be queried
    :param date_from: date from which to query
    :param date_to: date to which to query

    :return: response from Elasticsearch
    """
    pass


@router.get("/get_speeches/{party}", tags=["speeches"])
async def get_speeches_party(
    party: str, date_from: Union[str, None] = None, date_to: Union[str, None] = None
):
    """
    :param index_name: name of the index to be queried

    :param party: party to be queried

    :return: response from Elasticsearch
    """
    pass


@router.get("/get_speeches/{topic}", tags=["speeches"])
async def get_speeches_topic(
    topic: str, date_from: Union[str, None] = None, date_to: Union[str, None] = None
):
    """
    :param index_name: name of the index to be queried

    :param topic: topic to be queried

    :return: response from Elasticsearch
    """
    pass


# Path: backend/app/routers/missing.py
