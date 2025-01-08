from .client import APIClient
from .queries import PAGINATED_SEARCH_QUERY

class PaginatedSearchService:
    def __init__(self, api_key):
        self.client = APIClient(api_key)

    def paginated_search(self, paper_list, keywords=None):
        variable_values = {
            "paper_list": paper_list,
            "keywords": keywords or [],
        }
        result = self.client.execute_query(PAGINATED_SEARCH_QUERY, variable_values)
        return result