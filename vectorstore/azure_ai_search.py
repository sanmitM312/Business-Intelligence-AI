import uuid

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from types import SimpleNamespace


class AzureAISearchVectorStore:
    """Azure AI Search vector store"""

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        index_name: str
    ) -> None:
        self.client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key)
        )

    def upload_chunks(
        self,
        chunks,
        embeddings,
        company:str,
        year: str,
        source_file: str
    ) -> None:
        """
        Upload chunks to Azure AI Search
        """

        documents = []

        # use batched embeddings for the chunks
        texts = [c.page_content for c in chunks]
        vectors = embeddings.embed_documents(texts) # batched under the hood
        
   
        documents = [
                {
                    "id" : str(uuid.uuid4()),
                    "company": company,
                    "year": year,
                    "source_file": source_file,
                    "content": text,
                    "content_vector" : vec
                }
                for text,vec in zip(texts,vectors)
        ]
        result = self.client.upload_documents(documents=documents)

        uploaded = sum(item.succeeded for item in result) # number of successful document uploads 

        print(f"Uploaded {uploaded}/{len(documents)} chunks.") # Exampled Uploaded 24 / 24 chunks


class Retriever:
    """Simple wrapper around Azure Search client for retrieving relevant chunks.
        Mirrors the Retriever used in the RAG extractor
    """

    def __init__(self,client):
        self.client = client

    def invoke(
        self,
        query: str,
        company: str | None = None,
        year: int | None = None,
        top_k: int = 20
    ) -> list:
        """
        Retrieves relevant chunks from Azure AI Search.
        Returns a list of SimpleNamespace objects with `page_content`
        """

        # filter with company and year for the company and year wise storage of stru
        # -ured outputs in the postgres db and also for retrieving context for user queries
        filter_expr = None
        if company and year:
            filter_expr = (
                f"company eq '{company}'"
                f"and year eq '{year}'"
            )

        results = (
            # for postgres
            self.client.search(
                search_text=query,
                top=top_k,
                filter=filter_expr
            )
            if filter_expr
            else self.client.search( # for normal user queries
                search_text=query,
                top=top_k
            )
        )

        documents = []
        for result in results:
            content = result.get("content","")
            documents.append(SimpleNamespace(page_content=content))

        return documents