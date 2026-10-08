from langchain_text_splitters import RecursiveCharacterTextSplitter
from simple_rag.config import get_settings

settings = get_settings()


def chunk_text(text: str) -> list[str]:
    """Split text into chunks based on the specified chunk size and overlap."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_text(text)



