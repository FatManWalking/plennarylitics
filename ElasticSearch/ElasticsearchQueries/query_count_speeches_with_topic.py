from elasticsearch import Elasticsearch
from elastic_transport import ApiResponse

es = Elasticsearch('http://localhost:9200')

#How many Speeches about a specific topic
# @app.get("/amount_speeches_with_topic/{topic}")
search_result = es.count(index="f3_test_protokolle",
                          query={"match": {
                              "Text": {
                                  "query": topic
                              }
                          }
                          })
print(search_result)
