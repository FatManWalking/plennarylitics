from elasticsearch import Elasticsearch
from elastic_transport import ApiResponse

es = Elasticsearch('http://localhost:9200')


def pretty_print_product_search(response: ApiResponse, comment):
    print("\n-----------------------------------------")
    print(comment)
    print("-----------------------------------------")
    for item in response["aggregations"]["party_most_missing_persons_agg"]["buckets"]:
        print(
            f"Person: {item['key']}, " +
            f"Count: {item['doc_count']}"
        )

#get top 10 missing people from party
# @app.get("/get_top_missing_persons_from_party/{party}")
search_result = es.search(index="f3_test_missing",
                          size=0,
                          aggs={"party_most_missing_persons_agg": {
                              "terms": {
                                  "field": "missing_" + party + ".keyword"
                              }
                          }
                          })

pretty_print_product_search(search_result, "Alle Einträge")