from elasticsearch import Elasticsearch
from elastic_transport import ApiResponse

es = Elasticsearch('http://localhost:9200')


def pretty_print_product_search(response: ApiResponse, comment):
    print("\n-----------------------------------------")
    print(comment)
    print("-----------------------------------------")
    for item in response["hits"]["hits"]:
        print(
            f"Partei: {item['_source']['Sprecher']}, " +
            f"Sprecher: {item['_source']['Text']}"
        )

#Get Speeches from person
# @app.get("/get_speeches_from_person/{mp_name}")
search_result = es.search(index="f3_test_protokolle",
                          size=50,
                          query={"match": {
                              "Sprecher": {
                                  "query": mp_name
                              }
                          }
                          })

pretty_print_product_search(search_result, "Alle Einträge")
#print(search_result)