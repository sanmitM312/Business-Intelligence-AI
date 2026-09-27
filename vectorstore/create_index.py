from dotenv import load_dotenv
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchProfile
)

load_dotenv()

# do the embedding dimensions have to be compatible 
# with the embedding model that I am currently using?
def create_index(
    endpoint: str,
    api_key: str,
    index_name: str,
    embedding_dimensions: int = 1536
) -> None:
    """
        Create Azure AI Search index

        Args:
            endpoint: Azure AI Search endpoint
            api-key: Azure AI Search API key.
            index_name: Index name
            embedding_dimensions: embedding dimensions
    """
    # initialize the vector search index client to create the necessary fields in the index
    client = SearchIndexClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )

    # add the fields in the index of the vector store
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True), # the primary key
        SimpleField(name="company", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="year", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source_file",type=SearchFieldDataType.String, filterable=True),
        SearchField(name="content", type=SearchFieldDataType.String, searchable=True), # important, to search the content we cannot use SimpleField, we need to use SearchField
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=embedding_dimensions,
            vector_search_profile_name="vector-profile"
        )
    ]

    # attach the type of search that will be done on the vector store during retrieval
    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(name="hnsw-config")
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config"
            )
        ]
    )

    # intialize the index 
    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search
    )

    # perform the transaction 
    client.create_or_update_index(index)
    
    print(f"Index '{index_name}' created successfully.")


if __name__ == '__main__':
    create_index(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        api_key=os.getenv("AZURE_SEARCH_API_KEY"),
        index_name=os.getenv("AZURE_SEARCH_INDEX_NAME")
    )