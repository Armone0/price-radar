"""HTTP istek (fetcher) modülü birim testleri."""
import io
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

from src.fetcher import (
    DEFAULT_USER_AGENT,
    FetchError,
    fetch_html,
    get_default_headers,
)


class TestFetcher(unittest.TestCase):
    def test_default_headers(self):
        headers = get_default_headers()
        self.assertIn("User-Agent", headers)
        self.assertEqual(headers["User-Agent"], DEFAULT_USER_AGENT)
        self.assertIn("tr-TR", headers["Accept-Language"])

    @patch("urllib.request.urlopen")
    def test_fetch_html_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.status = 200
        mock_response.read.return_value = "<html><body><h1>1.499 TL</h1></body></html>".encode("utf-8")
        mock_response.headers.get_content_charset.return_value = "utf-8"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        html = fetch_html("https://example.com/urun-123")
        self.assertIn("1.499 TL", html)
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_fetch_html_custom_headers(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.status = 200
        mock_response.read.return_value = b"<html>OK</html>"
        mock_response.headers.get_content_charset.return_value = "utf-8"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        custom_headers = {"X-Custom-Header": "TestValue"}
        fetch_html("https://example.com", headers=custom_headers)

        call_args, call_kwargs = mock_urlopen.call_args
        req = call_args[0]
        self.assertEqual(req.headers.get("X-custom-header"), "TestValue")

    @patch("urllib.request.urlopen")
    def test_fetch_html_fallback_decoding(self, mock_urlopen):
        # iso-8859-9 içeren Türkçe karakterli içerik (örn: "ş", "ç", "ğ")
        turkish_text = "<html><body>İndirimli Fiyat: 250 TL</body></html>"
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.status = 200
        mock_response.read.return_value = turkish_text.encode("iso-8859-9")
        mock_response.headers.get_content_charset.return_value = "invalid-charset"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        html = fetch_html("https://example.com")
        self.assertIn("İndirimli Fiyat", html)

    @patch("urllib.request.urlopen")
    def test_fetch_html_http_error(self, mock_urlopen):
        fp = io.BytesIO(b"Not Found")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://example.com/yok",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=fp
        )

        with self.assertRaises(FetchError) as ctx:
            fetch_html("https://example.com/yok")

        self.assertEqual(ctx.exception.status_code, 404)
        self.assertIn("Sunucu hatası", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_fetch_html_url_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError(reason="Name resolution failure")

        with self.assertRaises(FetchError) as ctx:
            fetch_html("https://gecersiz-alan-adi.com")

        self.assertIn("Bağlantı hatası", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
