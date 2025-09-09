import threading
import time
import random
from uuid import uuid4
from datetime import datetime
from fluent import sender


class BaseService:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.node_id = f"{service_name}-{str(uuid4())}"
        self.logger = sender.FluentSender(
            service_name.lower(), host="localhost", port=24224
        )
        self._register_service()
        self._start_heartbeat()

    def _register_service(self):
        self.registration_message = {
            "node_id": self.node_id,
            "message_type": "REGISTRATION",
            "service_name": self.service_name,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.logger.emit("registration", self.registration_message)

    def _send_heartbeat(self):
        while True:
            if random.random() < 0.15:
                heartbeat = {
                    "node_id": self.node_id,
                    "message_type": "HEARTBEAT",
                    "status": "UP",
                    "timestamp": datetime.utcnow().isoformat(),
                }
                self.logger.emit("heartbeat", heartbeat)
            time.sleep(10)

    def _start_heartbeat(self):
        thread = threading.Thread(target=self._send_heartbeat, daemon=True)
        thread.start()

    def start(self):
        raise NotImplementedError("Service must implement start method")
