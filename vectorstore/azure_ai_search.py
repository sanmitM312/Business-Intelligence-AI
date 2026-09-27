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