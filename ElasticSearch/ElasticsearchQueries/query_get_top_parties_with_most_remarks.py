from elasticsearch import Elasticsearch
from elastic_transport import ApiResponse

es = Elasticsearch('http://localhost:9200')


def pretty_print_product_search(response: ApiResponse, comment):
    print("\n-----------------------------------------")
    print(comment)
    print("-----------------------------------------")
    for item in response["aggregations"]["party_most_remarks_agg"]["buckets"]:
        print(
            f"Partei: {item['key']}, " +
            f"Count: {item['doc_count']}"
        )

#Amount of remarks by party
# @app.get("/get_amount_remarks_from_party")
search_result = es.search(index="f3_test_remarks",
                          size=0,
                          aggs={"party_most_remarks_agg": {
                              "terms": {
                                  "field": "Remarking Parties.keyword"
                              }
                          }
                          })

pretty_print_product_search(search_result, "Alle Einträge")
