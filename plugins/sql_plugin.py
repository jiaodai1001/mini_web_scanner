from plugins.base_plugin import BasePlugin
from scanners.sql_scanner import SQLScanner


class SQLPlugin(BasePlugin):

    name = "SQL Injection Scanner"

    def run(self, target, urls):

        print("[Plugin] Running SQL Injection Plugin")

        scanner = SQLScanner(urls)

        results = scanner.scan()

        return {
            "type": "sql_injection",
            "results": results
        }