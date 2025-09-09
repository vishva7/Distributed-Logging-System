from elasticsearch import Elasticsearch
import json

es = Elasticsearch(["http://localhost:9200"])

response = es.search(
    index="logs",
    body={
        "query": {"match_all": {}},
        "sort": [{"timestamp": {"order": "desc"}}],
        "size": 10,
    },
)

print("\nLast 10 indexed messages:")
print(json.dumps(response["hits"]["hits"], indent=4))
print("-" * 50)
