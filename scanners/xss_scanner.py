import requests


class XSSScanner:

    def __init__(self, urls):

        self.urls = urls

        self.payloads = [
            "<script>alert(1)</script>",
            "\"'><script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
        ]

    def scan(self):

        print("[XSSScanner] Starting XSS scan")

        vulnerable_urls = []

        for url in self.urls:

            if "?" not in url:
                continue

            for payload in self.payloads:

                test_url = url + payload

                try:

                    response = requests.get(test_url, timeout=5)

                except Exception:

                    continue

                if payload.lower() in response.text.lower():

                    print(f"[!] XSS vulnerability detected: {url}")

                    vulnerable_urls.append(url)

                    break

        return vulnerable_urls