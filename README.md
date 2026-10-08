# Simple RAG

A small retrieval-augmented generation (RAG) application. It extracts text from PDF, TXT, and Markdown files, cleans and chunks it, stores embeddings in Chroma, retrieves relevant passages with hybrid BM25/vector search, and generates answers with Groq.

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)

## Setup

From the repository root, install the project dependencies and create the local settings file:

```sh
uv sync
cp .env.example .env
```

Run setup and project commands consistently in either WSL or Windows. Virtual environments are platform-specific, so switching environments can make `uv` recreate `.venv` and reinstall packages.

Set `GROQ_API_KEY` in `.env` to enable answer generation. The default source is `docs/document.txt`; set `PDF_PATH` to another PDF, TXT, or Markdown file to use a different document. `PREFERRED_MODELS` must be a JSON array in `.env`, for example:

```dotenv
PREFERRED_MODELS=["openai/gpt-oss-120b","openai/gpt-oss-20b"]
```

The application tries models in order and moves to the next one if Groq reports that a model is unavailable. Configure model IDs that are enabled for your Groq account.

## Run end to end

Run the pipeline to index the configured document and then start an interactive question-and-answer session:

```sh
uv run python -m simple_rag.pipeline
```

Or index a document explicitly, then ask one question or start a chat:

```sh
uv run python -m simple_rag.pipeline ingest docs/document.txt
uv run python -m simple_rag.pipeline ask "What is this document about?"
uv run python -m simple_rag.pipeline chat
```

Run commands from the repository root. Re-ingesting a source replaces its old chunks without deleting other sources in the collection.

The `simple-rag` command runs the same pipeline:

```sh
uv run simple-rag
```

On the first run, `uv` installs the dependencies and the embedding model is downloaded. In WSL, a `Failed to hardlink files` warning is harmless; to silence it, run `export UV_LINK_MODE=copy` before `uv sync`. A PyTorch CUDA driver warning means embeddings will use CPU instead. An unauthenticated Hugging Face warning only indicates lower download rate limits.

## Configuration

| Setting            | Purpose                                       | Example                                                  |
| ------------------ | --------------------------------------------- | -------------------------------------------------------- |
| `PDF_PATH`         | Default PDF, TXT, or Markdown source          | `docs/document.txt`                                      |
| `GROQ_API_KEY`     | Groq API key for answer generation            | `your-key`                                               |
| `GROQ_BASE_URL`    | OpenAI-compatible Groq API endpoint           | `https://api.groq.com/openai/v1`                         |
| `PREFERRED_MODELS` | JSON array of model IDs, tried in order       | `["openai/gpt-oss-120b","openai/gpt-oss-20b"]`         |
| `TOP_K`            | Number of context chunks retrieved            | `10`                                                     |
| `CHUNK_SIZE`       | Maximum chunk size in characters              | `1000`                                                   |
| `CHUNK_OVERLAP`    | Overlap between adjacent chunks in characters | `200`                                                    |
| `EMBEDDING_MODEL`  | Sentence Transformers model used for vectors  | `sentence-transformers/all-MiniLM-L6-v2`                 |
| `COLLECTION_NAME`  | Chroma collection for indexed chunks          | `harness_data`                                           |
| `CHROMA_DB_PATH`   | Persistent Chroma database directory          | `chromadb`                                               |
