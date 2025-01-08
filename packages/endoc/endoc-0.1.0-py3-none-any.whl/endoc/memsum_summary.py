from .client import APIClient
from .queries import MEMSUM_SUMMARY_QUERY

class SummarizationService:
    def __init__(self, api_key):
        self.client = APIClient(api_key)

    def summarize_paper(
            self,
            collection,
            id_field,
            id_type,
            id_value
    ):
        variable_values = {
            "paper_id" : {
                "collection": collection,
                "id_field": id_field,
                "id_type": id_type,
                "id_value": id_value,
            }
        }
        result = self.client.execute_query(MEMSUM_SUMMARY_QUERY, variable_values)
        return result