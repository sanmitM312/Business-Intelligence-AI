from pathlib import Path

from langchain_core.documents  import Document
from langchain_experimental.text_splitter import SemanticChunker

# apply pre-split logic
from langchain_text_splitters import RecursiveCharacterTextSplitter


from dotenv import load_dotenv

load_dotenv()


def read_markdown(markdown_file: str) -> str:
    """
    Read markdown content.

    Args:
        markdown_file: Markdown file path.

    Returns:
        Markdown content.
    """
    return Path(markdown_file).read_text(encoding="utf-8")


def chunk_markdown(
    markdown_file: str,
    embeddings,
    pre_split_size: int = 20_000,
) -> list[Document]:
    """
    Generate semantic chunks from markdown.

    Coarse-splits with a character splitter first so SemanticChunker
    runs on smaller pieces — cuts embedding calls dramatically.

    Args:
        markdown_file: Markdown file path.
        embeddings: Azure OpenAI embedding model.
        pre_split_size: Coarse chunk size in characters before semantic split.

    Returns:
        List of semantic chunks.
    """
    markdown_content = read_markdown(markdown_file)

    pre_splitter = RecursiveCharacterTextSplitter(
        chunk_size=pre_split_size,
        chunk_overlap=0,
    )
    coarse_sections = pre_splitter.split_text(markdown_content)

    splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type="percentile",
    )

    chunks: list[Document] = []
    for section in coarse_sections:
        chunks.extend(splitter.create_documents([section]))
    return chunks


if __name__ == '__main__':
    import os
    from langchain_openai import AzureOpenAIEmbeddings

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_EMBEDDING_VERSION","2023-05-12")
    embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")


    if not endpoint or not api_key:
        raise RuntimeError(
            "Missing Azure creds, set up AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY in .env file"
        )

    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-small",
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        max_retries=6,
        request_timeout=60,
        chunk_size=16,
    )

    repo_root = Path(__file__).resolve().parents[1]
    markdown_file = repo_root / "data" / "markdown" / "goog014907-ars.md"

    chunks = chunk_markdown(
        markdown_file=markdown_file,
        embeddings=embeddings
    )

    print(f"Generated {len(chunks)} chunks\n")

    for index,chunk in enumerate(chunks[:3]):
        print("="*80)
        print(f'Chunk {index + 1}')
        print("="*80)
        print(chunk.page_content[:100])
        print()