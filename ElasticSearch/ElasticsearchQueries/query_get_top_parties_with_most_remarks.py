from elasticsearch import Elasticsearch
from elastic_transport import ApiResponse

es = Elasticsearch('http://localhost:9200')


def pretty_print_product_search(response: ApiResponse, comment):
    print("\n-----------------------------------------")
    print(comment)
    print("-----------------------------------------")
    for item in response["aggregations"]["party_most_remarks_agg"]["buckets"]:
        print(
            f"key: {item['key']}, " +
            f"doc_count: {item['doc_count']}"
        )

#Get parties with most remarks
# @app.get("/get_list_parties_most_remarks")
search_result = es.search(index="f3_test_remarks",
                          size=0,
                          aggs={"party_most_remarks_agg": {
                              "terms": {
                                  "field": "Remarking Parties.keyword"
                              }
                          }
                          })

pretty_print_product_search(search_result, "Alle Einträge")
