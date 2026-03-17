from plugins.base_plugin import BasePlugin
from scanners.header_scanner import HeaderScanner


class HeaderPlugin(BasePlugin):

    name = "Header Scanner"

    def run(self, target, urls):

        print("[Plugin] Running Header Plugin")

        scanner = HeaderScanner(target)

        results = scanner.scan()

        return {
            "type": "headers",
            "results": results
        }