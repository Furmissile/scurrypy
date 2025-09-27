import aiohttp
import aiofiles
import asyncio
import time
import json
import ssl
from dataclasses import dataclass
from urllib.parse import urlencode

from .logger import Logger
from .error import DiscordError

ssl_ctx = ssl.create_default_context()
ssl_ctx.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3  # Disable old SSL

DISCORD_HTTP_CODES = {
    200: "Successful Request",
    201: "Successful Creation",
    204: "No Content",
    304: "Not Modified",
    400: "Bad Request",
    401: "Missing Authorization",
    403: "Missing Permission",
    404: "Resource Not Found",
    405: "Invalid Method",
    429: "Rate Limited",
    502: "Gateway Unavailable"
}

@dataclass
class RequestItem:
    """Data container representing an HTTP request to Discord's API.
        Used internally by HTTPClient for queuing and processing requests.
    """
    method: str
    """HTTP method (e.g., GET, POST, DELETE, PUT, PATCH)"""

    url: str
    """Fully qualifying URL for this request."""

    endpoint: str
    """Endpoint of the URL for this request."""

    data: dict | None
    """Relevant data for this request."""

    files: list | None
    """Relevant files for this request."""

    future: asyncio.Future
    """Track the result of this request."""

class RouteQueue:
    """Represents a queue of requests for a single rate-limit bucket.
        Manages task worker that processes requests for that bucket.
    """
    def __init__(self):
        self.queue = asyncio.Queue()
        """Queue holding RequestItem for this bucket."""

        self.worker = None
        """Process for executing request for this bucket."""

class HTTPClient:
    """Handles all HTTP communication with Discord's API
        including rate-limiting by bucket and globally, async request handling,
        multipart/form-data file uploads, and error handling/retries.
    """
    def __init__(self, token: str, logger: Logger):
        self.token = token
        """The bot's token."""

        self._logger = logger
        """Logger instance to log events."""

        self.session: aiohttp.ClientSession = None
        """Client session instance."""

        self.global_reset = 0
        """Global rete limit cooldown if a global rate limit is active."""

        self.global_lock: asyncio.Lock = None
        """Lock on queues to avoid race conditions."""

        self.pending_queue: asyncio.Queue = None
        """Queue for requests not yet assigned to bucket."""

        self.pending_worker: asyncio.Task = None
        """Task processing for the pending queue."""

        self.endpoint_to_bucket: dict[str, str] = {}
        """Maps endpoints to rate-limit buckets"""

        self.bucket_queues: dict[str, RouteQueue] = {}
        """Maps endpoints to RouteQueue objects."""

        self._sentinel = object()
        """Sentinel to terminate session."""

        self.base_url = "https://discord.com/api/v10"
        """Base URL for discord's API requests."""

    async def start_session(self):
        """Initializes aiohttp session, queues, locks, and starting pending worker."""
        self.session = aiohttp.ClientSession()
        self.pending_queue = asyncio.Queue()
        self.global_lock = asyncio.Lock()
        self.pending_worker = asyncio.create_task(self._pending_worker())
        self._logger.log_debug("Session started.")

    async def request(self, method: str, endpoint: str, data=None, params=None, files=None):
        """Enqueues request WRT rate-limit buckets.

        Args:
            method (str): HTTP method (e.g., POST, GET, DELETE, PATCH, etc.)
            endpoint (str): Discord endpoint (e.g., /channels/123/messages)
            data (dict, optional): relevant data
            files (list[str], optional): relevant files

        Returns:
            (Future): future with response
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}" # normalize for single slashes
        if params:
            url += f"?{urlencode(params)}"

        future = asyncio.get_event_loop().create_future()

        if endpoint in self.endpoint_to_bucket:
            bucket = self.endpoint_to_bucket[endpoint]
            if bucket not in self.bucket_queues:
                self.bucket_queues[bucket] = RouteQueue()
                self.bucket_queues[bucket].worker = asyncio.create_task(
                    self._route_worker(bucket)
                )
            await self.bucket_queues[bucket].queue.put(RequestItem(method, url, endpoint, data, files, future))
        else:
            await self.pending_queue.put(RequestItem(method, url, endpoint, data, files, future))

        return await future

    async def _pending_worker(self):
        """Processes requests from global pending queue."""
        while True:
            item = await self.pending_queue.get()
            if item is self._sentinel:
                self.pending_queue.task_done()
                break
            await self._process_request(item)
            self.pending_queue.task_done()

    async def _route_worker(self, bucket: str):
        """Processes request from specific rate-limit bucket.

        Args:
            bucket (str): endpoint
        """
        queue = self.bucket_queues[bucket].queue
        while True:
            item = await queue.get()
            if item is self._sentinel:
                queue.task_done()
                break
            await self._process_request(item)
            queue.task_done()

    async def _process_request(self, item: RequestItem):
        """Core request execution. Handles headers, payload, files, retries, and bucket assignment.

        Args:
            item (RequestItem): incoming request

        Raises:
            DiscordError: discord error object
        """
        try:
            await self._check_global_limit()

            headers = {"Authorization": f"Bot {self.token}"}

            # Build multipart if files exist
            request_kwargs = {'headers': headers, 'ssl': ssl_ctx}

            if item.files: # only create FormData if files exist
                form = aiohttp.FormData()
                form.add_field('payload_json', json.dumps(item.data))

                for idx, file_path in enumerate(item.files):
                    try:
                        async with aiofiles.open(file_path, 'rb') as f:
                            data = await f.read()
                        form.add_field(
                            f'files[{idx}]',
                            data,
                            filename=file_path.split('/')[-1],
                            content_type='application/octet-stream'
                        )
                    except FileNotFoundError:
                        self._logger.log_warn(f"File '{file_path}' could not be found.")
                        break

                request_kwargs['data'] = form

            elif item.data is not None:
                request_kwargs['json'] = item.data # aiohttp sets Content-Type automatically

            async with self.session.request(item.method, item.url, **request_kwargs) as resp:
                self._logger.log_debug(f"{item.method} {item.endpoint}: {resp.status} {DISCORD_HTTP_CODES.get(resp.status, 'Unknown Status')}")

                # if triggered rate-limit
                if resp.status == 429:
                    data = await resp.json()
                    retry_after = float(data.get("retry_after", 1))
                    is_global = data.get("global")
                    if is_global:
                        self.global_reset = time.time() + retry_after

                    try:
                        self._logger.log_warn( f"You are being rate limited on {item.endpoint}. Retrying in {retry_after}s (global={is_global})")
                        await asyncio.sleep(retry_after + 0.5)
                    except asyncio.CancelledError:
                        # shutdown is happening
                        raise

                    # retry the request
                    await self._process_request(item)
                    return

                # if response failed (either lethal or recoverable)
                elif resp.status not in [200, 201, 204]:
                    raise DiscordError(resp.status, await resp.json())

                await self._handle_response(item, resp)

                # Handle rate-limit bucket headers
                bucket = resp.headers.get("X-RateLimit-Bucket")
                if bucket and item.endpoint not in self.endpoint_to_bucket:
                    self.endpoint_to_bucket[item.endpoint] = bucket
                    if bucket not in self.bucket_queues:
                        self.bucket_queues[bucket] = RouteQueue()
                        self.bucket_queues[bucket].worker = asyncio.create_task(
                            self._route_worker(bucket)
                        )

        except Exception as e:
            if not item.future.done():
                item.future.set_exception(e)

    async def _handle_response(self, item: RequestItem, resp: aiohttp.ClientResponse):
        """Resolves future with parsed JSON/text response.

        Args:
            item (RequestItem): request data to handle
            resp (aiohttp.ClientResponse): response for item
        """
        if resp.status == 204:
            item.future.set_result((None, 204))
        else:
            try:
                result = await resp.json()
            except aiohttp.ContentTypeError:
                result = await resp.text()
            item.future.set_result(result)

    async def _check_global_limit(self):
        """Waits if the global rate-limit is in effect."""
        async with self.global_lock:
            now = time.time()
            if now < self.global_reset:
                await asyncio.sleep(self.global_reset - now)

    async def close_session(self):  
        """Gracefully shuts down all workes and closes aiohttp session."""      
        # Stop workers
        for q in self.bucket_queues.values():
            await q.queue.put(self._sentinel)
        await self.pending_queue.put(self._sentinel)
        
        if self.session and not self.session.closed:
            await self.session.close()
