import requests


class SQLScanner:

    def __init__(self, urls):

        self.urls = urls

        self.payloads = [
            "'",
            "' OR '1'='1",
            "' OR 1=1 --",
            "\" OR \"1\"=\"1",
        ]

        self.errors = [
            "sql syntax",
            "mysql",
            "syntax error",
            "warning",
            "pdo",
            "odbc",
        ]

    def scan(self):

        print("[SQLScanner] Starting SQL injection scan")

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

                for error in self.errors:

                    if error.lower() in response.text.lower():

                        print(f"[!] SQL Injection detected: {url}")

                        vulnerable_urls.append(url)

                        break

        return vulnerable_urls