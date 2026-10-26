"""Fiyat metinlerinden sayısal değer ve para birimi ayrıştırıcı modülü."""
import re
from typing import Optional, Tuple

CURRENCY_SYMBOLS = {
    "₺": "TRY",
    "TL": "TRY",
    "$": "USD",
    "€": "EUR",
    "£": "GBP",
}


def clean_price_text(text: Optional[str]) -> str:
    """Metindeki fazla boşlukları ve özel karakterleri temizler."""
    if not text:
        return ""
    # Kesintisiz boşluk (non-breaking space) ve fazla boşlukları teke indir
    return " ".join(text.replace("\xa0", " ").strip().split())


def extract_currency(text: Optional[str]) -> str:
    """Metin içerisindeki para birimi kodunu veya sembolünü döndürür (Varsayılan: TRY)."""
    cleaned = clean_price_text(text).upper()
    for symbol, code in CURRENCY_SYMBOLS.items():
        if symbol.upper() in cleaned:
            return code
    for code in ("TRY", "USD", "EUR", "GBP"):
        if code in cleaned:
            return code
    return "TRY"


def parse_price(text: Optional[str]) -> Optional[float]:
    """
    Farklı e-ticaret sitelerinden gelen fiyat dizgilerini ondalıklı float sayıya dönüştürür.
    
    Örnekler:
      - '1.499,99 TL' -> 1499.99
      - '₺ 2.350,50'  -> 2350.50
      - '1,299.99 USD' -> 1299.99
      - '750 TL'      -> 750.0
      - '12.500 TL'   -> 12500.0
    """
    cleaned = clean_price_text(text)
    if not cleaned:
        return None

    match = re.search(r"\d+(?:[.,]\d+)*", cleaned)
    if not match:
        return None

    num_str = match.group(0)

    # Hem nokta hem virgül varsa (örn: 1.250,50 veya 1,250.50)
    if "." in num_str and "," in num_str:
        if num_str.rfind(",") > num_str.rfind("."):
            # Türk/Avrupa formatı (binlik '.', ondalık ',')
            num_str = num_str.replace(".", "").replace(",", ".")
        else:
            # Amerikan/İngiliz formatı (binlik ',', ondalık '.')
            num_str = num_str.replace(",", "")
    elif "," in num_str:
        parts = num_str.split(",")
        if len(parts[-1]) <= 2:
            num_str = num_str.replace(",", ".")
        else:
            num_str = num_str.replace(",", "")
    elif "." in num_str:
        parts = num_str.split(".")
        if len(parts[-1]) == 3 and len(parts) > 1:
            num_str = num_str.replace(".", "")

    try:
        val = float(num_str)
        return val
    except ValueError:
        return None


def parse_price_and_currency(text: Optional[str]) -> Tuple[Optional[float], str]:
    """Fiyat değerini ve para birimini tuple olarak döndürür."""
    return parse_price(text), extract_currency(text)
