from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential

from ..config import get_settings
from ..azure.openai_client import create_embeddings

_settings = get_settings()

_search_client = SearchClient(
    endpoint=_settings.AZURE_SEARCH_ENDPOINT,
    index_name=_settings.AZURE_SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(_settings.AZURE_SEARCH_API_KEY),
)


def get_search_client() -> SearchClient:
    return _search_client


def search_hr_documents(query: str, top_k: int = 5, filters: str | None = None):
    client = get_search_client()

    # Generate embedding for the query for vector search
    query_embedding = create_embeddings([query])[0]

    # Create vector query using the proper SDK model
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="embedding"
    )

    # Perform hybrid search (both text and vector)
    results = client.search(
        search_text=query,
        top=top_k,
        filter=filters,
        vector_queries=[vector_query],
    )

    docs = []
    for r in results:
        docs.append({
            "id": r.get("id"),
            "content": r.get("content"),
            "source": r.get("source") or r.get("file_name"),
            "page": r.get("page"),
        })

    return docs
