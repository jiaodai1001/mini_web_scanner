from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class ParameterParser:

    def __init__(self, urls):

        self.urls = urls

    def extract_parameters(self):

        """
        Extract parameters from URLs
        """

        param_urls = []

        for url in self.urls:

            parsed = urlparse(url)

            query = parsed.query

            if query:

                param_urls.append(url)

        return param_urls

    def generate_test_urls(self):

        """
        Generate parameter mutation URLs
        """

        test_urls = []

        for url in self.urls:

            parsed = urlparse(url)

            params = parse_qs(parsed.query)

            if not params:

                continue

            for key in params:

                new_params = params.copy()

                new_params[key] = ["TEST"]

                new_query = urlencode(new_params, doseq=True)

                new_url = urlunparse(
                    (
                        parsed.scheme,
                        parsed.netloc,
                        parsed.path,
                        parsed.params,
                        new_query,
                        parsed.fragment,
                    )
                )

                test_urls.append(new_url)

        return test_urls

    def discover_common_parameters(self):

        """
        Generate common parameter URLs
        """

        common_params = [
            "id",
            "page",
            "search",
            "q",
            "user",
            "uid",
            "file",
            "path",
        ]

        generated_urls = []

        for url in self.urls:

            parsed = urlparse(url)

            for param in common_params:

                new_query = urlencode({param: "1"})

                new_url = urlunparse(
                    (
                        parsed.scheme,
                        parsed.netloc,
                        parsed.path,
                        parsed.params,
                        new_query,
                        parsed.fragment,
                    )
                )

                generated_urls.append(new_url)

        return generated_urls