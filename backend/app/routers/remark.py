# Router to get all remarks from a specific MP or party (with optional date range or other filters)
#
from typing import Union
from fastapi import APIRouter

router = APIRouter()


@router.get("/get_remarks", tags=["remarks"])
async def get_remarks(
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


@router.get("/get_remarks/{party}", tags=["remarks"])
async def get_remarks_party(
    party: str, date_from: Union[str, None] = None, date_to: Union[str, None] = None
):
    """
    Find out which party made remarks

    :param index_name: name of the index to be queried

    :param party: party to be queried

    :return: response from Elasticsearch
    """
    pass


@router.get("/get_remarks_to/{party}", tags=["remarks"])
async def get_remarks_to_party(
    party: str, date_from: Union[str, None] = None, date_to: Union[str, None] = None
):
    """
    Find out which party was the target of remarks

    :param index_name: name of the index to be queried

    :param party: party to be queried

    :return: response from Elasticsearch
    """
    pass


@router.get("/get_remarks/{topic}", tags=["remarks"])
async def get_remarks_topic(
    topic: str, date_from: Union[str, None] = None, date_to: Union[str, None] = None
):
    """
    Find out who made remarks on a specific topic

    :param index_name: name of the index to be queried

    :param topic: topic to be queried

    :return: response from Elasticsearch
    """
    pass


# Path: backend/app/routers/remark.py
