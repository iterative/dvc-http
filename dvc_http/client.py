import re
from typing import Sequence, Tuple, Union

from aiohttp.client import ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient
from yarl import URL

StrOrURL = Union[str, URL]


class Client:
    """A custom HTTP client based on AIOHTTP.

    It supports retries except for PUT/POST requests and URL path rewrites.
    """

    def __init__(
        self, rewrites: Sequence[Tuple[str, str]], *args, **kwargs
    ) -> None:
        self._rewrites = [(re.compile(src), dst) for src, dst in rewrites]
        self._retry_client = RetryClient(*args, **kwargs)
        self._write_opts = ExponentialRetry(
            attempts=1, retry_all_server_errors=False
        )

    async def close(self) -> None:
        return await self._retry_client.close()

    def head(self, url: StrOrURL, **kwargs):
        return self._retry_client.head(self._build_url(url), **kwargs)

    def get(self, url: StrOrURL, **kwargs):
        return self._retry_client.get(self._build_url(url), **kwargs)

    def post(self, url: StrOrURL, **kwargs):
        return self._retry_client.post(
            self._build_url(url), retry_options=self._write_opts, **kwargs
        )

    def put(self, url: StrOrURL, **kwargs):
        return self._retry_client.put(
            self._build_url(url), retry_options=self._write_opts, **kwargs
        )

    @property
    def _client(self) -> ClientSession:
        # HACK: Accessed in `tests/test_config.py`
        return self._retry_client._client  # pylint: disable=protected-access

    def _build_url(self, url: StrOrURL) -> URL:
        if isinstance(url, str):
            url = URL(url)
        for src, dst in self._rewrites:
            url_path, n = src.subn(dst, url.path)
            if n != 0:
                url = url.with_path(url_path)
                break
        return url
