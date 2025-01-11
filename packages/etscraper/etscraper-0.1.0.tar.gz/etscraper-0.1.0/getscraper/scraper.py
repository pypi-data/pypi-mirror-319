import requests

class GetScraper:
    """
    A scraper class to interact with a scraping service API.
    """

    def __init__(self, api_key):
        """
        Initialize the scraper with an API key.

        :param api_key: Your API key for the scraping service.
        """
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.base_url = 'https://api.livescraper.com/'  # Replace with your own endpoint if needed.

    def google_maps_search(self, queries, options=None):
        """
        Search Google Maps for places.

        :param queries: The search query (e.g., "restaurants, Manhattan, NY").
        :param options: Additional options for the search as a dictionary.
        :return: The search results as a dictionary.
        """
        if not queries:
            raise ValueError("Queries is required")

        # Extract options explicitly
        options = options or {}
        language = options.get("language")
        region = options.get("region")
        dropduplicates = options.get("dropduplicates")
        enrichment = options.get("enrichment")
        fields = options.get("fields")

        # Construct params explicitly
        params = {
            "key": self.api_key,
            "queries": queries,
            "language": language,
            "region": region,
            "dropduplicates": dropduplicates,
            "enrichment": enrichment,
            "fields": fields,
        }

        try:
            response = requests.get(f"{self.base_url}api/v1/task/map", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Failed to fetch data: {error.response.json().get('message', str(error))}") from error

    def google_review_search(self, queries, options=None):
        """
        Search Google for reviews.

        :param queries: The search query (e.g., "restaurants reviews, Manhattan, NY").
        :param options: Additional options for the search as a dictionary.
        :return: The search results as a dictionary.
        """
        if not queries:
            raise ValueError("Queries is required")

        # Extract options explicitly
        options = options or {}
        language = options.get("language")
        region = options.get("region")
        dropduplicates = options.get("dropduplicates")
        enrichment = options.get("enrichment")
        fields = options.get("fields")

        # Construct params explicitly
        params = {
            "key": self.api_key,
            "queries": queries,
            "language": language,
            "region": region,
            "dropduplicates": dropduplicates,
            "enrichment": enrichment,
            "fields": fields,
        }

        try:
            response = requests.get(f"{self.base_url}api/v1/task/email", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Failed to fetch data: {error.response.json().get('message', str(error))}") from error

    def google_email_search(self, queries, options=None):
        """
        Search Google for emails.

        :param queries: The search query (e.g., "contact emails for restaurants").
        :param options: Additional options for the search as a dictionary.
        :return: The search results as a dictionary.
        """
        if not queries:
            raise ValueError("Queries is required")

        # Extract options explicitly
        options = options or {}
        language = options.get("language")
        region = options.get("region")
        dropduplicates = options.get("dropduplicates")
        enrichment = options.get("enrichment")
        fields = options.get("fields")

        # Construct params explicitly
        params = {
            "key": self.api_key,
            "queries": queries,
            "language": language,
            "region": region,
            "dropduplicates": dropduplicates,
            "enrichment": enrichment,
            "fields": fields,
        }

        try:
            response = requests.get(f"{self.base_url}api/v1/task/email", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Failed to fetch data: {error.response.json().get('message', str(error))}") from error
