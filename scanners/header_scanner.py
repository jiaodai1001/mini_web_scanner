import requests


class HeaderScanner:

    def __init__(self, url):

        self.url = url

        self.security_headers = [
            "X-Frame-Options",
            "X-XSS-Protection",
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "Referrer-Policy",
        ]

    def scan(self):

        print("[HeaderScanner] Checking HTTP security headers")

        missing_headers = []

        try:

            response = requests.get(self.url, timeout=5)

        except Exception:

            print("[HeaderScanner] Failed to connect to target")

            return missing_headers

        headers = response.headers

        for header in self.security_headers:

            if header not in headers:

                print(f"[!] Missing security header: {header}")

                missing_headers.append(header)

            else:

                print(f"[+] Header present: {header}")

        return missing_headers