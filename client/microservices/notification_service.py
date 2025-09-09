from base_service import BaseService
import random
import time
from datetime import datetime
from uuid import uuid4
from fluent import sender


class NotificationService(BaseService):
    def __init__(self):
        super().__init__("NotificationService")
        self.logger = sender.FluentSender(
            "notification_service", host="localhost", port=24224
        )

    def send_notification(self, recipient: str, message: str):
        start_time = time.time()
        processing_time = random.uniform(0.2, 3.0)
        time.sleep(processing_time)
        response_time = int((time.time() - start_time) * 1000)

        if processing_time > 2.5:
            self.logger.emit(
                "warn",
                {
                    "log_id": str(uuid4()),
                    "node_id": self.node_id,
                    "log_level": "WARN",
                    "message_type": "LOG",
                    "message": f"Notification to {recipient} delayed",
                    "service_name": self.service_name,
                    "response_time_ms": response_time,
                    "threshold_limit_ms": 2500,
                    "timestamp": datetime.utcnow().isoformat(),
                },
            )
        elif random.random() < 0.1:
            try:
                raise Exception("Notification gateway error")
            except Exception as e:
                self.logger.emit(
                    "error",
                    {
                        "log_id": str(uuid4()),
                        "node_id": self.node_id,
                        "log_level": "ERROR",
                        "message_type": "LOG",
                        "message": f"Failed to send notification to {recipient}",
                        "service_name": self.service_name,
                        "error_details": {
                            "error_code": "NOTIFICATION_ERROR",
                            "error_message": str(e),
                        },
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                )
        else:
            self.logger.emit(
                "info",
                {
                    "log_id": str(uuid4()),
                    "node_id": self.node_id,
                    "log_level": "INFO",
                    "message_type": "LOG",
                    "message": f"Notification sent to {recipient}",
                    "service_name": self.service_name,
                    "timestamp": datetime.utcnow().isoformat(),
                },
            )

    def start(self):
        log_id = 1
        while True:
            recipient = f"user{random.randint(100, 999)}@example.com"
            message = f"Hello, this is your notification {random.randint(1, 100)}"
            self.send_notification(recipient, message)
            if log_id % 5 == 0:
                self.logger.emit(
                    "heartbeat",
                    {
                        "node_id": self.node_id,
                        "message_type": "HEARTBEAT",
                        "status": "UP",
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                )
            log_id += 1
            time.sleep(random.uniform(2.0, 6.0))


if __name__ == "__main__":
    service = NotificationService()
    service.start()
