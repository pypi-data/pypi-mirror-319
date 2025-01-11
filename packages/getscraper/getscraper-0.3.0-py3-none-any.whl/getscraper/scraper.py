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

    def google_maps_search(self, queries, language=None, region=None, dropduplicates=None, enrichment=None, fields=None):
        """
        Search Google Maps for places.

        :param queries: The search query (e.g., "restaurants, Manhattan, NY").
        :param language: Language code for the search.
        :param region: Region code for the search.
        :param dropduplicates: Whether to drop duplicate results.
        :param enrichment: Enrichment level for the results.
        :param fields: Specific fields to include in the response.
        :return: The search results as a dictionary.
        """
        if not queries:
            raise ValueError("Queries is required")

        try:
            response = requests.get(
                f"{self.base_url}api/v1/task/map",
                params={
                    "key": self.api_key,
                    "queries": queries,
                    "language": language,
                    "region": region,
                    "dropduplicates": dropduplicates,
                    "enrichment": enrichment,
                    "fields": fields,
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Failed to fetch data: {error.response.json().get('message', str(error))}") from error

    def google_review_search(self, queries, language=None, region=None, dropduplicates=None, enrichment=None, fields=None):
        """
        Search Google for reviews.

        :param queries: The search query (e.g., "restaurants reviews, Manhattan, NY").
        :param language: Language code for the search.
        :param region: Region code for the search.
        :param dropduplicates: Whether to drop duplicate results.
        :param enrichment: Enrichment level for the results.
        :param fields: Specific fields to include in the response.
        :return: The search results as a dictionary.
        """
        if not queries:
            raise ValueError("Queries is required")

        try:
            response = requests.get(
                f"{self.base_url}api/v1/task/review",
                params={
                    "key": self.api_key,
                    "queries": queries,
                    "language": language,
                    "region": region,
                    "dropduplicates": dropduplicates,
                    "enrichment": enrichment,
                    "fields": fields,
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Failed to fetch data: {error.response.json().get('message', str(error))}") from error

    def google_email_search(self, queries, language=None, region=None, dropduplicates=None, enrichment=None, fields=None):
        """
        Search Google for emails.

        :param queries: The search query (e.g., "contact emails for restaurants").
        :param language: Language code for the search.
        :param region: Region code for the search.
        :param dropduplicates: Whether to drop duplicate results.
        :param enrichment: Enrichment level for the results.
        :param fields: Specific fields to include in the response.
        :return: The search results as a dictionary.
        """
        if not queries:
            raise ValueError("Queries is required")

        try:
            response = requests.get(
                f"{self.base_url}api/v1/task/email",
                params={
                    "key": self.api_key,
                    "queries": queries,
                    "language": language,
                    "region": region,
                    "dropduplicates": dropduplicates,
                    "enrichment": enrichment,
                    "fields": fields,
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Failed to fetch data: {error.response.json().get('message', str(error))}") from error
