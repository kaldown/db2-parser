"""Stand-ins for urllib responses so tests never touch the network."""

import io
import urllib.error
from email.message import Message


class FakeResponse:
    def __init__(self, body: bytes, headers: dict | None = None):
        self._body = body
        self.headers = Message()
        for key, value in (headers or {}).items():
            self.headers[key] = value

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(code: int, url: str = "https://example.invalid") -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url, code, f"HTTP {code}", Message(), io.BytesIO(b""))


class FakeOpener:
    """Returns or raises each scripted outcome in turn and records requests."""

    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.requests = []

    def __call__(self, request, timeout=None):
        self.requests.append(request)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome
