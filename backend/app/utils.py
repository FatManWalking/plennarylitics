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
