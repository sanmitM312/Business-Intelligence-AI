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


## AZURE SETUP
- From Microsoft Foundary, create a new resource to deploy the target embedding model
- From overview, get the azure api endpoint (Azure OpenAI) 
- Azure AI Search Service setup under the ai investing resource group

## RETRIEVAL PIPELINE

### PLAN TO RETRIEVE THE KPIS FROM VECTORSTORE
        - vectorstore -> azure_ai_search -> Retriever (Check the Namespace stuff also)
            - Defines the retriever to retrieve the relevant chunks for the KPIs (DONE)

        - rag.kpi_extractor_rag -> extract_financial_metrics 
            - Defines the context extraction and structured output generation methods (DONE)

        - llms.azure_openai -> structured_completion -> to tie up with OpenAI's chat api (DONE)
        
        - database.save_metrics -> save_metrics (DO IT AFTER INGESTION IN AZURE)
        
        - Question : Difference between KPI-EXTRACTOR-RAG's Retriever and Azure AI Search's Retriever

## POSTGRES DB SETUP
    - Firewall rule, had to allow my local machine's IP to make the connection via the portal
    - I think this is only server settings, need to check whether end users will be affected or not

## BACKLOG
    - Complete end to end deployment
    - Add better logs on the backend
    - Improve the UI of the financials - it should mention - billion units
    - Improve chat formatting and responsiveness for the UI
    - Split into frontend and backend microservices
    - Add authentication to this project
    - Azure AI Search index schema changes are not applied on startup
        - create_index.py now skips creation if the index already exists (guardrail added so startup doesn't recreate it every run)
        - Side effect: changes to the index fields (e.g. embedding_dimensions, new filterable fields) won't reach Azure automatically
        - Current workaround: delete the index and restart the app, or run create_or_update_index manually
        - TODO: add a schema check / migration step that compares the existing index fields with the expected ones and updates or warns on mismatch

## PERFORMANCE LOG
    - Tesla took 4 minutes to process with 150 chunks


## DEPLOYMENT LOGS
    - Dockerfile created
    - Docker image built and deployed in local container, running on localhost:8000
    - changed my wifi also public ip , had to go to azure postgres db networking firewall and allow this ip 
    - Failure in retrieving the chunks for kpi-extraction (isolate the failure modes)
    