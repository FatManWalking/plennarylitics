from elasticsearch import Elasticsearch
from elastic_transport import ApiResponse

es = Elasticsearch('http://localhost:9200')


def pretty_print_product_search(response: ApiResponse, comment):
    print("\n-----------------------------------------")
    print(comment)
    print("-----------------------------------------")
    for item in response["aggregations"]["remarkclass_agg"]["buckets"]:
        print(
            f"RemarkClass: {item['key']}, " +
            f"Count: {item['doc_count']}"
        )

#Amount of remark classes
# @app.get("/get_amount_remarkclasses")
search_result = es.search(index="f3_test_remarks",
                          size=0,
                          aggs={"remarkclass_agg": {
                              "terms": {
                                  "field": "Remark Class.keyword",
                                  "exclude": ["", "None"]
                              }
                          }
                          })

pretty_print_product_search(search_result, "Alle Einträge")
