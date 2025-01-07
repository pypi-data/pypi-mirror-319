from enum import Enum


class CaptureConfigTriggerKind(str, Enum):
    EMAIL = "email"
    HTTP = "http"
    KAFKA = "kafka"
    WEBHOOK = "webhook"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
