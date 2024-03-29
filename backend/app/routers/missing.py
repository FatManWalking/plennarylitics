# Router to get all missing MPs or aggregated by party (with optional date range or other filters)
#
from typing import Union
from fastapi import APIRouter

router = APIRouter()


@router.get("/get_missing", tags=["missing"])
async def get_missing(
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


@router.get("/get_missing/{party}", tags=["missing"])
async def get_missing_party(
    party: str, date_from: Union[str, None] = None, date_to: Union[str, None] = None
):
    """
    :param index_name: name of the index to be queried

    :param party: party to be queried

    :return: response from Elasticsearch
    """
    pass


@router.get("/get_missing/{topic}", tags=["missing"])
async def get_missing_topic(
    topic: str, date_from: Union[str, None] = None, date_to: Union[str, None] = None
):
    """
    :param index_name: name of the index to be queried

    :param topic: topic to be queried

    :return: response from Elasticsearch
    """
    pass


# Path: backend/app/routers/speech.py
