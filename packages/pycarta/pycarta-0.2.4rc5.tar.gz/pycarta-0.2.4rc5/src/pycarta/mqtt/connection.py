import os
import logging
import time
from typing import Any
from uuid import uuid4
from paho.mqtt import client as pclient
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("DEBUG_LEVEL", logging.INFO))

class MQTTConnection:
    """
    Base class for managing MQTT connections with connection, disconnection, and reconnection support.
    """
    POLLING_INTERVAL = float(os.getenv("POLLING_INTERVAL", 0.1))
    POLLING_TIMEOUT = float(os.getenv("POLLING_TIMEOUT", 30))
    FIRST_RECONNECT_DELAY = int(os.environ.get("FIRST_RECONNECT_DELAY", 1))
    RECONNECT_RATE = int(os.environ.get("RECONNECT_RATE", 2))
    MAX_RECONNECT_COUNT = int(os.environ.get("MAX_RECONNECT_COUNT", 12))
    MAX_RECONNECT_DELAY = int(os.environ.get("MAX_RECONNECT_DELAY", 60))

    class ConnectInfo(BaseModel):
        """Connection information model."""
        userdata: Any
        flags: Any
        return_code: Any
        properties: Any

    def __init__(self, topic: str, *, host: str = "localhost", port: int = 1883):
        """
        Initialize MQTTConnection.

        Args:
            topic (str): MQTT topic.
            host (str): Broker host. Default is 'localhost'.
            port (int): Broker port. Default is 1883.
        """
        self.topic = topic
        self.host = host
        self.port = port
        self.client = pclient.Client(
            callback_api_version=pclient.CallbackAPIVersion.VERSION2,
            client_id=str(uuid4())
        )
        self.connect_info = None

    def __del__(self):
        """Ensure disconnection on object deletion."""
        self.disconnect()

    def connect(self):
        """Connect to the MQTT broker."""
        if not self.client.is_connected():
            self.client.connect(self.host, self.port)

    def reconnect(self):
        """Reconnect to the MQTT broker."""
        self.disconnect()
        self.connect()

    def disconnect(self, client=None, userdata=None, rc=None, properties=None) -> None:
        """
        Disconnect from the MQTT broker or handle disconnection callback.
        """
        if rc is not None:
            logger.info(f"Disconnected with return code {rc}.")
            if rc != 0:  # Unexpected disconnection
                logger.warning("[MQTTConnection] Unexpected disconnection. Attempting to reconnect...")
                self._attempt_reconnect(client, userdata, rc, properties)
            else:
                self.connect_info = None
        else:
            if self.client.is_connected():
                logger.info("[MQTTConnection] Explicitly disconnecting from broker.")
                self.client.disconnect()
                self.connect_info = None

    def _on_connect(self, client, userdata, flags, rc, properties) -> None:
        """Handle successful connection."""
        if not rc:
            self.connect_info = self.ConnectInfo(
                userdata=userdata, flags=flags, return_code=rc, properties=properties
            )
            logger.info(f"Connected {userdata} to {self.host}:{self.port}")

    def _attempt_reconnect(self, client, userdata, rc, properties) -> None:
        """Attempt to reconnect to the broker."""
        cls = type(self)
        logger.info(f"Disconnected with return code {rc}.")
        reconnect_count, reconnect_delay = 0, cls.FIRST_RECONNECT_DELAY

        while reconnect_count < cls.MAX_RECONNECT_COUNT:
            logger.info(f"Reconnecting in {reconnect_delay} seconds...")
            time.sleep(reconnect_delay)
            try:
                self.client.reconnect()
                logger.info("Reconnect successful.")
                return
            except Exception as err:
                logger.error(f"Reconnect failed: {err}")

            reconnect_delay = min(reconnect_delay * cls.RECONNECT_RATE, cls.MAX_RECONNECT_DELAY)
            reconnect_count += 1

        logger.info(f"Reconnect failed after {reconnect_count} attempts.")

class PubSubStopIteration(StopIteration, StopAsyncIteration):
    """
    Raised to signal the termination of synchronous or asynchronous loops.

    This exception is a specialized form of `StopIteration` and `StopAsyncIteration`, designed for use in MQTT publish/subscribe workflows. It is raised when an MQTT subscription loop needs to terminate gracefully, either due to the completion of a task or a controlled shutdown of the process.

    Attributes:
        message (str): An optional description of the reason for loop termination.
    """

    def __init__(self, message="The publish/subscribe loop has been stopped."):
        super().__init__(message)


class SerializationError(Exception):
    """
    Raised when message serialization fails during MQTT operations.

    This exception indicates that an attempt to serialize a message (e.g., to JSON or another format) has failed. It commonly occurs when the message contains unsupported data types, invalid structures, or other issues incompatible with the serialization format.

    Attributes:
        message (str): A detailed description of the serialization error.
    """

    def __init__(self, message="Message serialization failed."):
        super().__init__(message)


class PublishError(Exception):
    """
    Raised when publishing to the MQTT broker fails.

    This exception indicates that an attempt to publish a message to an MQTT broker was unsuccessful. Common reasons include network issues, broker unavailability, authentication failures, or payload-related problems.

    Attributes:
        message (str): A detailed description of the publishing error.
        topic (str): The topic to which the message was being published.
    """

    def __init__(self, message="Publishing to the MQTT broker failed.", topic=None):
        self.topic = topic
        if topic:
            message += f" (Topic: {topic})"
        super().__init__(message)


class SubscribeError(Exception):
    """
    Raised when subscribing to an MQTT topic fails.

    This exception signals that an attempt to subscribe to an MQTT topic was unsuccessful. Causes can include invalid topic names, lack of permissions, network issues, or broker errors.

    Attributes:
        message (str): A detailed description of the subscription error.
        topic (str): The topic to which the subscription was attempted.
    """

    def __init__(self, message="Subscribing to the MQTT topic failed.", topic=None):
        self.topic = topic
        if topic:
            message += f" (Topic: {topic})"
        super().__init__(message)


class TimeoutException(Exception):
    """
    Raised when an MQTT operation exceeds the allowed time limit.

    This exception is triggered when an operation, such as connecting to the broker, subscribing to a topic, or waiting for a message, does not complete within the specified timeout period. It ensures that long-running or stalled processes can be gracefully handled.

    Attributes:
        message (str): A detailed description of the timeout error.
        timeout (float): The duration (in seconds) after which the timeout occurred.
    """

    def __init__(self, message="Operation timed out.", timeout=None):
        self.timeout = timeout
        if timeout:
            message += f" (Timeout: {timeout} seconds)"
        super().__init__(message)
