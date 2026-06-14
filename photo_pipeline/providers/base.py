"""Base class for photo providers with common utilities."""

import urllib.request
import json
import time
from typing import Optional
from abc import ABC


class BaseProvider(ABC):
    RETRY_COUNT = 3
    RETRY_DELAY = 2.0
    USER_AGENT = "TravelHubPhotoPipeline/2.0"

    def _fetch_json(self, url: str, headers: Optional[dict] = None) -> Optional[dict]:
        hdrs = {"User-Agent": self.USER_AGENT}
        if headers:
            hdrs.update(headers)
        for attempt in range(1, self.RETRY_COUNT + 1):
            try:
                req = urllib.request.Request(url, headers=hdrs)
                resp = urllib.request.urlopen(req, timeout=20)
                return json.loads(resp.read().decode())
            except Exception:
                if attempt < self.RETRY_COUNT:
                    time.sleep(self.RETRY_DELAY)
        return None

    def _fetch_bytes(self, url: str) -> Optional[bytes]:
        hdrs = {"User-Agent": self.USER_AGENT}
        for attempt in range(1, self.RETRY_COUNT + 1):
            try:
                req = urllib.request.Request(url, headers=hdrs)
                resp = urllib.request.urlopen(req, timeout=30)
                return resp.read()
            except Exception:
                if attempt < self.RETRY_COUNT:
                    time.sleep(self.RETRY_DELAY)
        return None
