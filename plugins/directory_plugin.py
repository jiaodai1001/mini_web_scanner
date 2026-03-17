from plugins.base_plugin import BasePlugin
from scanners.directory_scanner import DirectoryScanner


class DirectoryPlugin(BasePlugin):

    name = "Directory Scanner"

    def run(self, target, urls):

        print("[Plugin] Running Directory Plugin")

        scanner = DirectoryScanner(target)

        results = scanner.scan()

        return {
            "type": "directories",
            "results": results
        }