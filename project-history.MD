## ENV SETUP
- create virtual env using -> uv venv
- initialize a project using uv -> uv venv
- define the requirements.txt file -> uv pip install -r requirements.txt

## INGESTION STEP
- Convert the annual reports to markdown - to preserve the structure of the tables for ingestion, kept under markdown/ folder
- pdf_to_markdown.py file added under ingestion --> DONE

## AZURE SETUP
- From Microsoft Foundary, create a new resource to deploy the target embedding model
- From overview, get the azure api endpoint (Azure OpenAI) 
- First error : openai.RateLimitError: Error code: 429 - {'error': {'code': 'RateLimitReached', 'message': 'Your requests to text-embedding-3-small for text-embedding-3-small in East US have exceeded the call rate limit for your current AIServices S0 pricing tier. This request was for Embeddings_Create under Azure OpenAI API version 2023-05-15. Please retry after 60 seconds. To increase your default rate limit, visit: https://aka.ms/oai/quotaincrease.'}}

Approach :
    - Pre-split large documents using RecursiveCharacterTextSplitter into smaller pieces
    - Then apply semantic chunking on those pieces one by one.
    - Reduces the number of api calls --> cost
    - To remove the rate limiting issue, apply the chunking_size for batch api calls
    - Issue tabular data