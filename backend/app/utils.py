# Here we define some helper functions that are used in the app
# Since we did not get the count query to work as we wanted, we decided to use the search query and count the results in the backend
# This is not the most efficient way to do it and we should change it in the future

from collections import defaultdict
from typing import Dict


def count_remarked_party(query_result: dict):
    """
    For the active filters count if and how a speech got interrupted
    """

    hits = query_result["hits"]["hits"]
    remarked = defaultdict(lambda: defaultdict(int))

    for hit in hits:
        remarked[hit["_source"]["Partei des Sprechers der Rede"]]["total"] += 1
        if hit["_source"]["Remarking Parties"]:
            for party in hit["_source"]["Remarking Parties"][0]:

                remarked[hit["_source"]["Partei des Sprechers der Rede"]][party] += 1
        if hit["_source"]["Remark Class"]:
            for remarking_class in hit["_source"]["Remark Class"]:
                remarked[hit["_source"]["Partei des Sprechers der Rede"]][
                    remarking_class
                ] += 1

    return remarked
