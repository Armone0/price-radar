"""Web sayfalarından HTML içeriği çekmek için hafif urllib istemcisi."""
import ssl
import urllib.error
import urllib.request
from typing import Dict, Optional


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

DEFAULT_TIMEOUT = 10.0


class FetchError(Exception):
    """HTTP isteklerinde meydana gelen genel hata sınıfı."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


def get_default_headers() -> Dict[str, str]:
    """Standart tarayıcı başlıklarını döndürür."""
    return {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }


def fetch_html(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> str:
    """
    Belirtilen URL adresine GET isteği atarak sayfanın HTML içeriğini döndürür.

    Args:
        url: İstek atılacak web adresi.
        headers: İsteğe eklenecek ek HTTP başlıkları (varsayılan headers ile birleştirilir).
        timeout: Saniye cinsinden zaman aşımı süresi.

    Returns:
        str: Web sayfasının çözümlenmiş HTML metni.

    Raises:
        FetchError: Ağ hatası, zaman aşımı veya geçersiz HTTP durum kodunda fırlatılır.
    """
    req_headers = get_default_headers()
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, headers=req_headers)
    ctx = ssl.create_default_context()

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            status = getattr(response, "status", None) or response.getcode()
            if status and status >= 400:
                raise FetchError(f"HTTP Hatası: {status}", status_code=status)

            content_bytes = response.read()

            # Karakter setini belirle ve çözümle
            charset = None
            if hasattr(response, "headers") and response.headers:
                charset = response.headers.get_content_charset()

            charset = charset or "utf-8"

            try:
                return content_bytes.decode(charset)
            except (UnicodeDecodeError, LookupError):
                try:
                    return content_bytes.decode("iso-8859-9")
                except UnicodeDecodeError:
                    return content_bytes.decode("utf-8", errors="replace")

    except urllib.error.HTTPError as e:
        raise FetchError(f"Sunucu hatası ({e.code}): {e.reason}", status_code=e.code) from e
    except urllib.error.URLError as e:
        raise FetchError(f"Bağlantı hatası: {e.reason}") from e
    except TimeoutError as e:
        raise FetchError("İstek zaman aşımına uğradı") from e
    except Exception as e:
        if isinstance(e, FetchError):
            raise
        raise FetchError(f"Beklenmeyen istek hatası: {str(e)}") from e
