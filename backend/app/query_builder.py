# The Queries of all endpoints are defined here to keep the endpoints clean and readable
# Also here we can define a template to spot mistakes in the queries and to keep them consistent (like interfaces in Typescript)

from typing import List, Optional, Tuple, Union, Dict, Any, Mapping
from datetime import datetime

# Query for get_missing_mp
class Query:
    def __init__(
        self, extras: Optional[List[Tuple[str, Union[str, List]]]] = None
    ) -> None:
        """
        A completly generic query we can use to build our queries

        :param extras: A list of tuples with the name of the function and the parameter to pass to the function

        E.g. [("add_mp_name", "Max Mustermann"), ("add_date", "2020-01-01")]
             Calls the function add_mp_name("Max Mustermann") and add_date("2020-01-01")
        """
        self.query = {
            "query": {
                "bool": {
                    "must": [
                        # {"match": {"title": "Search term"}}, # The document is scored based on how well the search term matches the title
                        # {"match": {"body": "Search term"}}, # The document is scored based on how well the search term matches the body
                        # {"multi_match": {"query": "Search term", "fields": ["title", "*_body"]}}, # The document is scored based on how well the search term matches the title and body
                    ],
                    "filter": [
                        # {"range": {"Datum": {"gte": "now-10000d/d", "lte": "now/d"}}} # Only show the last 10000 days
                        # { "term": {"missing_AFD": "1"} } # Exact match where there must be a 1 in the field missing_AFD
                    ],
                },
            }
            # "aggs": { "types_count": ...   # Aggregations are used to group the results by a specific field and e.g. count the number of results per group
        }

        # alternative way to add the extras to the query
        # if extras:
        #     for extra in extras:
        #         extra_function = getattr(self, f"{extra[0]}")
        #         extra_function(extra[1])

    def get_query(self) -> Mapping[str, Any]:
        """
        Returns the query
        """
        return self.query

    # First more generic, then more specific (e.g. add_date before add_missing_mp_name)

    def add_date(
        self,
        from_date: str = datetime.utcfromtimestamp(0).strftime("%Y-%m-%d"),
        to_date: str = datetime.now().strftime("%Y-%m-%d"),
    ):
        """
        Adds the date to the query
        """
        self.query["query"]["bool"]["filter"].append(
            {"range": {"Datum": {"gte": from_date, "lte": to_date}}}
        )

    def add_topic(self, topic: str):
        """
        Adds the topic to the query
        """
        self.query["query"]["bool"]["must"].append({"match": {"Text": topic}})

    # All MP related functions

    def add_missing_mp_name(self, mp_name: str):
        """
        Adds the MP name to the query
        """
        self.query["query"]["bool"]["must"].append(
            {"multi_match": {"query": mp_name, "fields": ["missing_*"]}}
        )

    def add_remarking_mp_name(self, mp_name: str):
        """
        Adds the MP name to the query
        """
        self.query["query"]["bool"]["must"].append(
            {"match": {"query": mp_name, "fields": ["Remarking_Persons"]}}
        )

    def add_speaking_mp_name(self, mp_name: str):
        """
        Adds the MP name to the query
        """
        self.query["query"]["bool"]["must"].append(
            {"multi_match": {"query": mp_name, "fields": ["Sprecher der Rede"]}}
        )

    # All party related functions

    def count_missing_party(self, party: str):
        """
        For the active filters count how many MPs are missing for a specific party
        """
        self.query["aggs"] = {
            "types_count": {"value_count": {"field": f"missing_{party}"}}
        }

    def add_missing_party(self, party: str):
        """
        Adds the party to the query
        """
        # TODO: Not done yet
        self.query["query"]["bool"]["filter"].append(
            {"term": {f"missing_{party}": "1"}}
        )
