from .client import APIClient
from .queries import DOCUMENT_SEARCH_QUERY

class DocumentSearchService:
    def __init__(self, api_key):
        self.client = APIClient(api_key)

    def search_documents(
            self,
            ranking_variable,
            keywords=None
    ):
        variable_values = {
            "ranking_variable": ranking_variable,
            "keywords": keywords or []
        }
        result = self.client.execute_query(DOCUMENT_SEARCH_QUERY, variable_values)
        return result
