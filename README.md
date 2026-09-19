# DocuMind — Intelligent Enterprise Document Assistant

A Retrieval-Augmented Generation (RAG) based document question-answering system that allows users to upload enterprise documents, ask questions in natural language, and receive answers grounded in relevant document content.

## Overview

DocuMind combines multiple retrieval techniques to improve the quality and relevance of information provided to the language model.

The system uses:

- Semantic vector search
- BM25 keyword search
- Reciprocal Rank Fusion (RRF)
- Cohere reranking
- LLM-based answer generation
- Source-aware responses

The goal is to retrieve the most relevant document passages before generating an answer, reducing the risk of unsupported responses.

---

## Architecture

### Document Ingestion

PDF Documents
      ↓
Document Parsing
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
PostgreSQL + pgvector

### Query & Retrieval

User Question
      ↓
┌─────────────────────────┐
│ Vector Search + BM25    │
└────────────┬────────────┘
             ↓
      RRF Rank Fusion
             ↓
      Cohere Reranker
             ↓
       LLM Generation
             ↓
    Answer + Source Citations

The system combines semantic vector search and BM25 keyword retrieval. Their results are merged using Reciprocal Rank Fusion (RRF), reranked for relevance, and passed to the language model to generate a grounded response.

---

## Retrieval Pipeline

### 1. Vector Search

Documents are converted into embeddings and stored using PostgreSQL with pgvector.

Vector similarity is used to identify passages that are semantically related to the user's question.

### 2. BM25 Search

BM25 provides keyword-based retrieval.

This helps the system identify documents containing important terms, phrases, names, or technical terminology that may not always be captured effectively by semantic search alone.

### 3. Reciprocal Rank Fusion

Results from vector search and BM25 are combined using Reciprocal Rank Fusion.

RRF produces a unified ranking from the independent retrieval results.

### 4. Cohere Reranking

The retrieved passages are passed through a reranking stage to improve the ordering of the most relevant results.

### 5. Grounded Answer Generation

The highest-ranked document passages are provided as context to the language model.

The generated response is based on the retrieved context rather than relying only on the model's general knowledge.

### 6. Source Citations

The API returns source information associated with the retrieved passages so that users can trace the answer back to the original document.

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Database | PostgreSQL 16 |
| Vector Database | pgvector |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Embeddings | OpenAI Embeddings |
| Keyword Retrieval | BM25 |
| Reranking | Cohere |
| Containerization | Docker Compose |

---

## Key Features

- PDF document ingestion
- Automatic text extraction
- Document chunking
- Semantic vector retrieval
- BM25 keyword retrieval
- Hybrid retrieval using RRF
- Cross-encoder reranking
- Context-grounded responses
- Source-aware answers
- REST API using FastAPI
- PostgreSQL + pgvector storage
- Evaluation framework for retrieval and answer quality

---

## How It Works

### Step 1 — Upload

A user uploads a PDF document through the API.

### Step 2 — Parse

The document is processed and its text and page information are extracted.

### Step 3 — Chunk

The extracted text is divided into smaller passages suitable for retrieval.

### Step 4 — Embed

Each passage is converted into a vector representation.

### Step 5 — Store

The document chunks and their embeddings are stored in PostgreSQL using pgvector.

### Step 6 — Retrieve

When a user asks a question, the system performs both:

- Semantic vector search
- BM25 keyword search

### Step 7 — Fuse

The results from both retrieval methods are combined using Reciprocal Rank Fusion.

### Step 8 — Rerank

The combined results are reranked based on their relevance to the question.

### Step 9 — Generate

The most relevant context is passed to the language model to generate the final response.

### Step 10 — Cite

Relevant document and page information is returned with the answer.

---

## Setup

### Prerequisites

- Python 3.10+
- Docker
- Docker Compose
- OpenAI API key
- Cohere API key

### 1. Clone the Repository

~~~bash
git clone https://github.com/Vasudev-69/documind-rag.git
cd documind-rag
~~~

### 2. Configure Environment Variables

Create a `.env` file in the project root.

~~~env
POSTGRES_USER=documind
POSTGRES_PASSWORD=documind123
POSTGRES_DB=documind

DATABASE_URL=postgresql+asyncpg://documind:documind123@db:5432/documind

DEBUG=false

OPENAI_API_KEY=
COHERE_API_KEY=

PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin123
~~~

Do not commit `.env` or API keys to GitHub.

### 3. Start the Application

~~~bash
docker compose up --build
~~~

This starts:

- `db` — PostgreSQL with pgvector
- `api` — FastAPI application
- `pgadmin` — PostgreSQL administration interface

### 4. Run Database Migrations

~~~bash
docker compose exec api alembic upgrade head
~~~

### 5. Open API Documentation

Once the application is running:

~~~text
http://localhost:8000/docs
~~~

---

## API Usage

### Create a Tenant

~~~bash
curl -X POST http://localhost:8000/api/v1/tenants/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Example Organization"}'
~~~

### Upload a Document

~~~bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "tenant_id=<uuid>" \
  -F "file=@/path/to/document.pdf"
~~~

### Ask a Question

~~~bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "<uuid>",
    "question": "What is the notice period?",
    "top_k": 5
  }'
~~~

### Example Response

~~~json
{
  "answer": "The required notice period is described in the retrieved document.",
  "sources": [
    {
      "document_title": "Company_Policy.pdf",
      "page_number": 3,
      "content": "Relevant document passage..."
    }
  ]
}
~~~

The response contains source information that allows users to trace the generated answer back to the retrieved document context.

---

## Evaluation

The repository includes an evaluation framework for testing the RAG pipeline.

The evaluation covers:

- Retrieval relevance
- Expected source retrieval
- Answer correctness
- Negative retrieval cases

Run the evaluation using:

~~~bash
python eval_runner.py --tenant-id <uuid>
~~~

A custom evaluation dataset can also be provided:

~~~bash
python eval_runner.py --tenant-id <uuid> --eval-file path/to/custom_eval.json
~~~

### Evaluation Approach

**Retrieval Evaluation**

Checks whether the expected source document is returned among the retrieved results.

**Answer Evaluation**

Checks whether the generated response is consistent with the expected answer and retrieved context.

**Negative Cases**

Tests whether the system avoids retrieving unrelated information when the requested information is not present in the document collection.

> No benchmark score is claimed unless the evaluation has actually been executed on the current implementation and dataset.

---

## Project Structure

~~~text
documind-rag/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── tenants.py
│   │           ├── documents.py
│   │           └── query.py
│   │
│   ├── agent/
│   │   └── nodes.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   └── session.py
│   │
│   ├── models/
│   ├── schemas/
│   │
│   └── services/
│       ├── parsing.py
│       ├── embedding_service.py
│       ├── bm25_service.py
│       ├── rrf.py
│       ├── reranker_service.py
│       └── query_service.py
│
├── alembic/
│
├── eval.json
├── eval_runner.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
~~~

---

## Engineering Highlights

### Hybrid Retrieval

Combines semantic retrieval with lexical retrieval to handle both conceptual questions and exact terminology.

### Reciprocal Rank Fusion

Combines independently ranked results from different retrieval strategies into a unified ranking.

### Reranking

Adds a second relevance-ranking stage before information is passed to the language model.

### Grounded Generation

Uses retrieved document context as the basis for answer generation.

### Source Attribution

Returns document information associated with retrieved passages to improve traceability.

---

## Limitations

- The complete pipeline requires external embedding and reranking APIs.
- Evaluation quality depends on the documents and questions used in the evaluation dataset.
- Important information should be verified against the original documents.
- Production deployment would require additional authentication, monitoring, rate limiting, and security controls.

---

## Attribution

This project is an adapted and extended implementation based on an existing open-source RAG architecture.

The implementation has been modified for the DocuMind enterprise-document use case, including project identity, prompts, evaluation data, configuration, and documentation.

---

## Author

**Vasudev Hirani**

GitHub: **Vasudev-69**
