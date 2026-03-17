from plugins.base_plugin import BasePlugin
from scanners.xss_scanner import XSSScanner


class XSSPlugin(BasePlugin):

    name = "XSS Scanner"

    def run(self, target, urls):

        print("[Plugin] Running XSS Plugin")

        scanner = XSSScanner(urls)

        results = scanner.scan()

        return {
            "type": "xss",
            "results": results
        }