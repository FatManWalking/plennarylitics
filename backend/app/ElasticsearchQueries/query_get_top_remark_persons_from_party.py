from elasticsearch import Elasticsearch
from elastic_transport import ApiResponse

es = Elasticsearch('http://localhost:9200')


def pretty_print_product_search(response: ApiResponse, comment):
    print("\n-----------------------------------------")
    print(comment)
    print("-----------------------------------------")
    #["person_most_remarks_agg"]["buckets"]
    for item in response["aggregations"]["party_most_remarks_agg"]["buckets"]:
        print(
            f"Party: {item['key']}, " +
            f"Personlist: {item['person_most_remarks_agg']['buckets']}"
        )

#Get parties with most remarks + their list of top remark persons
# @app.get("/get_top_remark_persons_from_party")
search_result = es.search(index="f3_test_remarks",
                          size=0,
                          aggs={"party_most_remarks_agg": {
                              "terms": {
                                  "field": "Party Remarking Person.keyword",
                                  "exclude": ""
                              },
                              "aggs": {
                                  "person_most_remarks_agg": {
                                      "terms": {
                                          "field": "Remarking Persons.keyword"
                                      }
                                  }
                              }
                          }
                          })

pretty_print_product_search(search_result, "Alle Einträge")

#Get parties with most remarks + their list of top remark persons
