import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Crawler:

    def __init__(self, base_url, depth):

        self.base_url = base_url
        self.depth = depth

        self.visited = set()
        self.urls = []

    def crawl(self):

        print("[Crawler] Start crawling")

        self._crawl_page(self.base_url, 0)

        return self.urls

    def _crawl_page(self, url, current_depth):

        if current_depth > self.depth:
            return

        if url in self.visited:
            return

        print(f"[Crawler] Visiting: {url}")

        self.visited.add(url)

        try:

            response = requests.get(url, timeout=5)

        except Exception:

            return

        if response.status_code != 200:
            return

        self.urls.append(url)

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a")

        for link in links:

            href = link.get("href")

            if not href:
                continue

            full_url = urljoin(url, href)

            if full_url.startswith(self.base_url):

                self._crawl_page(full_url, current_depth + 1)