import tempfile
import unittest
from pathlib import Path

import ctfr


class NormalizeDomainTests(unittest.TestCase):
    def test_accepts_domains_and_urls(self):
        cases = {
            "example.com": "example.com",
            "www.example.com": "example.com",
            "https://example.com/path?q=1": "example.com",
            "https://www.example.com:443/path": "example.com",
            " EXAMPLE.COM. ": "example.com",
            "https://münich.example/path": "xn--mnich-kva.example",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(ctfr.normalize_domain(value), expected)

    def test_rejects_invalid_targets(self):
        for value in ("", "localhost", "https://", "bad_domain.example", "-bad.com"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    ctfr.normalize_domain(value)


class ExtractSubdomainsTests(unittest.TestCase):
    def test_splits_normalizes_filters_and_deduplicates(self):
        records = [
            {"name_value": "api.example.com\n*.dev.example.com"},
            {"name_value": "API.EXAMPLE.COM\nother.example.net"},
            {"name_value": "example.com."},
            {"irrelevant": "ignored"},
            "ignored",
        ]
        self.assertEqual(
            ctfr.extract_subdomains(records, "example.com"),
            ["api.example.com", "dev.example.com", "example.com"],
        )

    def test_rejects_unexpected_json(self):
        with self.assertRaises(ValueError):
            ctfr.extract_subdomains({"error": "busy"}, "example.com")


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return [{"name_value": "api.example.com"}]


class FakeClient:
    def __init__(self):
        self.call = None

    def get(self, url, **kwargs):
        self.call = (url, kwargs)
        return FakeResponse()


class FetchSubdomainsTests(unittest.TestCase):
    def test_uses_query_parameters_headers_and_timeout(self):
        client = FakeClient()
        result = ctfr.fetch_subdomains("example.com", timeout=4.5, client=client)

        self.assertEqual(result, ["api.example.com"])
        self.assertEqual(client.call[0], ctfr.CRT_SH_URL)
        self.assertEqual(
            client.call[1]["params"], {"q": "%.example.com", "output": "json"}
        )
        self.assertEqual(client.call[1]["timeout"], 4.5)
        self.assertIn("User-Agent", client.call[1]["headers"])


class SaveSubdomainsTests(unittest.TestCase):
    def test_overwrites_with_sorted_unique_results(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results.txt"
            output.write_text("old.example.com\n", encoding="utf-8")

            count = ctfr.save_subdomains(
                ["b.example.com", "a.example.com", "b.example.com"], output
            )

            self.assertEqual(count, 2)
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                "a.example.com\nb.example.com\n",
            )

    def test_append_writes_only_new_results(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results.txt"
            output.write_text("a.example.com", encoding="utf-8")

            count = ctfr.save_subdomains(
                ["a.example.com", "b.example.com"], output, append=True
            )

            self.assertEqual(count, 1)
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                "a.example.com\nb.example.com\n",
            )


if __name__ == "__main__":
    unittest.main()
