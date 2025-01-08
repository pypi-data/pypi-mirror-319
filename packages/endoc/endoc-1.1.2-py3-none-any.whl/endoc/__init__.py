from .document_search import DocumentSearchService
from .paginated_search import PaginatedSearchService
from .memsum_summary import SummarizationService

def summarize(api_key, collection, id_field, id_type, id_value):
    service = SummarizationService(api_key)
    return service.summarize_paper(collection, id_field, id_type, id_value)

def document_search(api_key, ranking_variable, **kwargs):
    service = DocumentSearchService(api_key)
    return service.search_documents(ranking_variable, **kwargs)

def paginated_search(api_key, paper_list, keywords=None):
    service = PaginatedSearchService(api_key)
    return service.paginated_search(paper_list, keywords)