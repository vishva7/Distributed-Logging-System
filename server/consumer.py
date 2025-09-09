from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import json

consumer = KafkaConsumer(
    "logs",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

es = Elasticsearch(["http://localhost:9200"])

last_heartbeats = {}

for message in consumer:
    msg = message.value
    # print("\nReceived Message:")
    # print(json.dumps(msg, indent=4))
    message_type = msg.get("message_type")
    service_name = msg.get("service_name", "")
    print(f"\nReceived Message: {message_type} {service_name}")

    es.index(index="logs", document=msg)

    node_id = msg.get("node_id")

    if message_type == "REGISTRATION":
        registry_doc = {
            "node_id": node_id,
            "service_name": msg.get("service_name"),
            "status": "UP",
            "timestamp": datetime.utcnow().isoformat(),
        }
        es.index(index="service_registry", id=node_id, document=registry_doc)
        print(f"Registered service {msg.get('service_name')} with node_id {node_id}")

    elif message_type == "HEARTBEAT":
        last_heartbeats[node_id] = datetime.utcnow()
        es.update(
            index="service_registry",
            id=node_id,
            body={"doc": {"status": "UP", "timestamp": datetime.utcnow().isoformat()}},
        )

    elif message_type == "LOG":
        if msg.get("log_level") in ["ERROR", "WARN"]:
            print(f"ALERT: {msg.get('log_level')} - {msg.get('message')}")

    current_time = datetime.utcnow()
    for node, last_hb in list(last_heartbeats.items()):
        if current_time - last_hb > timedelta(seconds=15):
            es.update(
                index="service_registry",
                id=node,
                body={"doc": {"status": "DOWN", "timestamp": current_time.isoformat()}},
            )
            print(f"ALERT: Node {node} is DOWN")
            del last_heartbeats[node]
