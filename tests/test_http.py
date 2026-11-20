import gzip
import unittest
import urllib.error

from tests import _path  # noqa: F401
from tests.fakes import FakeOpener, FakeResponse, http_error

import fetch

URL = "https://wago.tools/db2/Spell/csv?build=1.2.3.4"
BODY = b"ID,Name\n1,a\n"


class HttpGetTests(unittest.TestCase):
    def setUp(self):
        self.sleeps = []

    def get(self, opener):
        return fetch.http_get(URL, opener=opener, sleep=self.sleeps.append)

    def test_sends_browser_headers(self):
        opener = FakeOpener(FakeResponse(BODY))
        self.get(opener)
        request = opener.requests[0]
        self.assertEqual(request.get_header("User-agent"), fetch.BROWSER_HEADERS["User-Agent"])
        self.assertEqual(request.get_header("Accept-encoding"), "gzip")
        self.assertIn("Mozilla/5.0", request.get_header("User-agent"))

    def test_decodes_gzip(self):
        opener = FakeOpener(FakeResponse(gzip.compress(BODY), {"Content-Encoding": "gzip"}))
        self.assertEqual(self.get(opener), BODY)

    def test_plain_body_passthrough(self):
        self.assertEqual(self.get(FakeOpener(FakeResponse(BODY))), BODY)

    def test_retries_5xx_then_succeeds(self):
        opener = FakeOpener(http_error(503), http_error(503), FakeResponse(BODY))
        self.assertEqual(self.get(opener), BODY)
        self.assertEqual(self.sleeps, [2, 4])

    def test_gives_up_after_three_attempts(self):
        opener = FakeOpener(*(urllib.error.URLError("down") for _ in range(3)))
        with self.assertRaises(urllib.error.URLError):
            self.get(opener)
        self.assertEqual(len(opener.requests), 3)
        self.assertEqual(self.sleeps, [2, 4])

    def test_no_retry_on_4xx(self):
        opener = FakeOpener(http_error(403))
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.get(opener)
        self.assertEqual(ctx.exception.code, 403)
        self.assertEqual(len(opener.requests), 1)
        self.assertEqual(self.sleeps, [])


if __name__ == "__main__":
    unittest.main()
