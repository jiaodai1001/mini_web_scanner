import requests
import os


class DirectoryScanner:

    def __init__(self, base_url):

        self.base_url = base_url

        self.wordlist_path = "payloads/directories.txt"

    def load_wordlist(self):

        directories = []

        if not os.path.exists(self.wordlist_path):

            print("[DirectoryScanner] Wordlist not found")

            return directories

        with open(self.wordlist_path, "r") as f:

            for line in f:

                directory = line.strip()

                if directory:

                    directories.append(directory)

        return directories

    def scan(self):

        print("[DirectoryScanner] Starting directory scan")

        found_directories = []

        directories = self.load_wordlist()

        for directory in directories:

            url = f"{self.base_url}/{directory}"

            try:

                response = requests.get(url, timeout=5)

            except Exception:

                continue

            if response.status_code == 200:

                print(f"[+] Found directory: {url}")

                found_directories.append(url)

            elif response.status_code == 403:

                print(f"[!] Forbidden directory: {url}")

                found_directories.append(url)

        return found_directories