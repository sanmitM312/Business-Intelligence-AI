## ENV SETUP
- create virtual env using -> uv venv
- initialize a project using uv -> uv venv
- define the requirements.txt file -> uv pip install -r requirements.txt

## INGESTION STEP
- Convert the annual reports to markdown - to preserve the structure of the tables for ingestion, kept under markdown/ folder
- the company pdf should be in appropirate defined formats
- pdf_to_markdown.py file added under ingestion --> DONE
- Chunking steps
- {'error': {'code': 'RateLimitReached', 'message': 'Your requests to text-embedding-3-small for text-embedding-3-small in East US have exceeded the call rate limit for your current AIServices S0 pricing tier. This request was for Embeddings_Create under Azure OpenAI API version 2023-05-15. Please retry after 60 seconds. To increase your default rate limit, visit: https://aka.ms/oai/quotaincrease.'}}

Approach :
    - Pre-split large documents using RecursiveCharacterTextSplitter into smaller pieces
    - Then apply semantic chunking on those pieces one by one.
    - Reduces the number of api calls --> cost
    - To remove the rate limiting issue, apply the chunking_size for batch api calls
    - Issue tabular data

### PLAN TO INTEGRATE AZURE AI SEARCH
    - unresolved modules
        - vectorstore -> first create the index in azure -> create_index.py -> DONE
        - vectorstore -> azure_ai_search -> AzureAISearchVectorStore -> DONE
            - Implement the above class
            - upload_chunks is the part of it
        - integrate both under ingest_documents

### PLAN TO RETRIEVE THE KPIS FROM VECTORSTORE
        - rag.kpi_extractor_rag -> extract_financial_metrics (DO IT AFTER INGESTION IN AZURE)

        - database.save_metrics -> save_metrics (DO IT AFTER INGESTION IN AZURE)
        - vectorstore -> azure_ai_search -> Retriever(DO IT AFTER INGESTION IN AZURE)


## AZURE SETUP
- From Microsoft Foundary, create a new resource to deploy the target embedding model
- From overview, get the azure api endpoint (Azure OpenAI) 
- Azure AI Search Service setup under the ai investing resource group