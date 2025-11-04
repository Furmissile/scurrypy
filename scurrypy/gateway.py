import asyncio
import json
import websockets

from .logger import Logger
from .events.hello_event import HelloEvent

DISCORD_OP_CODES = {
    0: "Dispatch",
    1: "Heartbeat",
    2: "Identify",
    3: "Presence Update",
    6: "Resume",
    7: "Reconnect",
    8: "Request Guild Members",
    9: "Invalid Session",
    10: "Hello",
    11: "Heartbeat ACK",
    None: "Unknown"
}

class GatewayClient:
    """Handles real-time Websocket (WS) connection to Discord's Gateway.
        Connects to Discord's WS, handles identify/resume logic, and maintains heartbeat.
    """
    def __init__(self, token: str, intents: int, logger: Logger):
        self.token = token
        """The bot's token."""

        self._logger = logger
        """Logger instance to log events."""

        self.ws = None
        """Websocket instance."""

        self.heartbeat = None
        """Heartbeat task instance."""

        self.sequence = None
        """Discord-generated sequence number for this websocket connection."""

        self.session_id = None
        """Discord-generated session ID for this websocket connection."""

        self.intents = intents
        """User-defined bot intents (for identify)."""

        self.url_params = "?v=10&encoding=json"
        """Discord WS query params."""

        self.connect_url = f"wss://gateway.discord.gg/"
        """URL to connect to Discord's gateway."""

    async def connect(self):
        """Established websocket connection to Discord."""
        self.ws = await websockets.connect(self.connect_url + self.url_params)
        self._logger.log_high_priority("Connected to Discord.")

    async def receive(self):
        """Receives and logs messages from the gateway.

        Returns:
            (dict): parsed JSON data
        """

        message = await asyncio.wait_for(self.ws.recv(), timeout=60)

        if message:
            data: dict = json.loads(message)
            self._logger.log_info(f"Received: {DISCORD_OP_CODES.get(data.get('op'))}")
            return data

        return None

    async def send(self, message: dict):
        """Sends a JSON-encoded message to the gateway.

        Args:
            message (dict): the message to send
        """
        await self.ws.send(json.dumps(message))

    async def send_heartbeat_loop(self):
        """Background task that sends heartbeat payloads in regular intervals.
            Retries until cancelled.
        """
        while self.ws:
            await asyncio.sleep(self.heartbeat_interval / 1000)
            hb_data = {"op": 1, "d": self.sequence}
            await self.send(hb_data)
            self._logger.log_debug(f"Sent HEARTBEAT: {hb_data}")

    async def identify(self):
        """Sends the IDENIFY payload (token, intents, connection properties).
            Must be sent after connecting to the WS.
        """
        i = {
            "op": 2,
            "d": {
                "token": f"Bot {self.token}",
                "intents": self.intents,
                "properties": {
                    "$os": "my_os",
                    "$browser": "my_bot",
                    "$device": "my_bot"
                }
            }
        }
        await self.send(i)
        log_i = self._logger.redact(i)
        self._logger.log_debug(f"Sent IDENTIFY: {log_i}")
        self._logger.log_high_priority("Identify sent.")
    
    async def start_heartbeat(self):
        """Waits for initial HELLO event, hydrates the HelloEvent class, and begins the heartbeat."""
        data = await self.receive()
        hello = HelloEvent.from_dict(data.get('d'))
        self.heartbeat_interval = hello.heartbeat_interval
        self.heartbeat = asyncio.create_task(self.send_heartbeat_loop())
        self._logger.log_high_priority("Heartbeat started.")

    async def reconnect(self):
        """Sends RESUME payload to reconnect with the same session ID and sequence number
            as provided by Discord.
        """
        await self.send({
            "op": 6,
            "d": {
                "token": f"Bot {self.token}",
                "session_id": self.session_id,
                "seq": self.sequence
            }
        })
        self._logger.log_high_priority("RESUME sent")
        
    async def close(self):
        """Cancels heart beat and cleanly closes WS with error handling."""
        # Cancel heartbeat task if it's still running
        if self.heartbeat:
            self._logger.log_high_priority(f"Cancelling heartbeat...")
            self.heartbeat.cancel()
            await asyncio.wait_for(self.heartbeat, timeout=3)  # Add timeout to avoid hanging
            self.heartbeat = None

        if self.ws:
            await self.ws.close()
            self._logger.log_high_priority("WebSocket closed.")
            self.ws = None

    def is_connected(self):
        """Helper function to tell whether the websocket is still active."""
        return self.ws is not None
