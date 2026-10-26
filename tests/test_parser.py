"""Fiyat ayrıştırma (parser) modülü birim testleri."""
import unittest
from src.parser import parse_price, extract_currency, parse_price_and_currency, clean_price_text


class TestPriceParser(unittest.TestCase):
    def test_clean_price_text(self):
        self.assertEqual(clean_price_text("  1.299,00 TL \xa0"), "1.299,00 TL")
        self.assertEqual(clean_price_text(""), "")
        self.assertEqual(clean_price_text(None), "")

    def test_parse_turkish_currency_formats(self):
        self.assertEqual(parse_price("1.499,90 TL"), 1499.90)
        self.assertEqual(parse_price("₺ 2.350,50"), 2350.50)
        self.assertEqual(parse_price("750 TL"), 750.0)
        self.assertEqual(parse_price("49,99 TL"), 49.99)
        self.assertEqual(parse_price("12.500 TL"), 12500.0)

    def test_parse_us_and_other_formats(self):
        self.assertEqual(parse_price("$1,299.99"), 1299.99)
        self.assertEqual(parse_price("1,299.99 USD"), 1299.99)
        self.assertEqual(parse_price("19.99 €"), 19.99)

    def test_parse_invalid_or_empty_inputs(self):
        self.assertIsNone(parse_price(""))
        self.assertIsNone(parse_price(None))
        self.assertIsNone(parse_price("Tükendi"))
        self.assertIsNone(parse_price("Fiyat Sorunuz"))

    def test_extract_currency(self):
        self.assertEqual(extract_currency("1.250 TL"), "TRY")
        self.assertEqual(extract_currency("₺ 500"), "TRY")
        self.assertEqual(extract_currency("$99.90"), "USD")
        self.assertEqual(extract_currency("45,00 €"), "EUR")
        self.assertEqual(extract_currency("£120"), "GBP")
        self.assertEqual(extract_currency("150"), "TRY")  # Varsayılan fallback

    def test_parse_price_and_currency(self):
        price, cur = parse_price_and_currency("  ₺ 1.899,00 ")
        self.assertEqual(price, 1899.00)
        self.assertEqual(cur, "TRY")


if __name__ == "__main__":
    unittest.main()
