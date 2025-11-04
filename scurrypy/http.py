import aiohttp
import aiofiles
import asyncio
import json

from typing import Any, Optional

from .logger import Logger
from .error import DiscordError

class HTTPException(Exception):
    """Represents an HTTP error response from Discord."""
    def __init__(self, response: aiohttp.ClientResponse, message: str):
        self.response = response
        self.status = response.status
        self.text = message
        super().__init__(f"{response.status}: {message}")

class HTTPClient:
    BASE = "https://discord.com/api/v10"
    MAX_RETRIES = 3

    def __init__(self, token: str, logger: Logger):
        self.token = token
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logger
        self.global_reset = 0.0
        self.global_lock = asyncio.Lock()
        self.endpoint_to_bucket: dict[str, str] = {}
        self.queues: dict[str, asyncio.Queue] = {}
        self.workers: dict[str, asyncio.Task] = {}

    async def start(self):
        """Start the HTTP session."""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={"Authorization": f"Bot {self.token}"}
            )

    async def close(self):
        """Close the HTTP session."""
        for task in self.workers.values():
            task.cancel()
        if self.session and not self.session.closed:
            await self.session.close()

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        data: Any | None = None,
        params: dict | None = None,
        files: Any | None = None,
    ):
        """Enqueues request WRT rate-limit buckets.

        Args:
            method (str): HTTP method (e.g., POST, GET, DELETE, PATCH, etc.)
            endpoint (str): Discord endpoint (e.g., /channels/123/messages)
            data (dict, optional): relevant data
            params (dict, optional): relevant query params
            files (list[str], optional): relevant files

        Returns:
            (Future): future with response
        """
        if not self.session:
            await self.start()

        bucket = self.endpoint_to_bucket.get(endpoint, endpoint)
        queue = self.queues.setdefault(bucket, asyncio.Queue())
        future = asyncio.get_event_loop().create_future()

        await queue.put((method, endpoint, data, params, files, future))
        if bucket not in self.workers:
            self.workers[bucket] = asyncio.create_task(self._worker(bucket))

        return await future

    async def _worker(self, bucket: str):
        """Processes request from specific rate-limit bucket."""

        q = self.queues[bucket]
        while self.session:
            method, endpoint, data, params, files, future = await q.get()
            try:
                result = await self._send(method, endpoint, data, params, files)
                if not future.done():
                    future.set_result(result)
            except Exception as e:
                if not future.done():
                    future.set_exception(e)
            finally:
                q.task_done()

    async def _send(
        self,
        method: str,
        endpoint: str,
        data: Any | None,
        params: dict | None,
        files: Any | None,
    ):
        """Core HTTP request executor.

        Sends a request to Discord, handling JSON payloads, files, query parameters,
        rate limits, and retries.

        Args:
            method (str): HTTP method (e.g., 'POST', 'GET', 'DELETE', 'PATCH').
            endpoint (str): Discord API endpoint (e.g., '/channels/123/messages').
            data (dict | None, optional): JSON payload to include in the request body.
            params (dict | None, optional): Query parameters to append to the URL.
            files (list[str] | None, optional): Files to send with the request.

        Raises:
            (HTTPException): If the request fails after the maximum number of retries
                        or receives an error response.

        Returns:
            (dict | str | None): Parsed JSON response if available, raw text if the
                            response is not JSON, or None for HTTP 204 responses.
        """

        url = f"{self.BASE.rstrip('/')}/{endpoint.lstrip('/')}"

        def sanitize_query_params(params: dict | None) -> dict | None:
            if not params:
                return None
            return {k: ('true' if v is True else 'false' if v is False else v)
                    for k, v in params.items() if v is not None}

        for attempt in range(self.MAX_RETRIES):
            await self._check_global_limit()

            kwargs = {}

            if files and any(files):
                payload, headers = await self._make_payload(data, files)
                kwargs = {"data": payload, "headers": headers}
            else:
                kwargs = {"json": data}

            try:
                async with self.session.request(
                    method, url, params=sanitize_query_params(params), timeout=15, **kwargs
                ) as resp:
                    if resp.status == 429:
                        data = await resp.json()
                        retry = float(data.get("retry_after", 1))
                        if data.get("global"):
                            self.global_reset = asyncio.get_event_loop().time() + retry
                        self.logger.log_warn(
                            f"Rate limited {retry}s ({endpoint})"
                        )
                        await asyncio.sleep(retry + 0.5)
                        continue

                    if 200 <= resp.status < 300:
                        if resp.status == 204:
                            return None
                        try:
                            return await resp.json()
                        except aiohttp.ContentTypeError:
                            return await resp.text()
                        
                    if resp.status == 400:
                        raise DiscordError(resp.status, await resp.json())

                    text = await resp.text()
                    raise HTTPException(resp, text)

            except asyncio.TimeoutError:
                self.logger.log_warn(f"Timeout on {method} {endpoint}, retrying...")
                continue

        raise HTTPException(resp, f"Failed after {self.MAX_RETRIES} retries")

    async def _check_global_limit(self):
        """Waits if the global rate-limit is in effect."""

        now = asyncio.get_event_loop().time()
        if now < self.global_reset:
            delay = self.global_reset - now
            self.logger.log_warn(f"Global rate limit active, sleeping {delay:.2f}s")
            await asyncio.sleep(delay)

    async def _make_payload(self, data: dict, files: list):
        """Return (data, headers) for aiohttp request — supports multipart.

        Args:
            data (dict): request data
            files (list): relevant files

        Returns:
            (tuple[aiohttp.FormData, dict]): form data and headers
        """
        headers = {}
        if not files:
            return data, headers

        form = aiohttp.FormData()
        if data:
            form.add_field("payload_json", json.dumps(data))

        for idx, file_path in enumerate(files):
            async with aiofiles.open(file_path, 'rb') as f:
                data = await f.read()
            form.add_field(
                f'files[{idx}]',
                data,
                filename=file_path.split('/')[-1],
                content_type='application/octet-stream'
            )

        return form, headers
