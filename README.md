# \# DocuMind — Intelligent Enterprise Document Assistant

# 

# A document question-answering system built using Retrieval-Augmented Generation (RAG).

# 

# DocuMind allows users to upload enterprise documents, ask questions in natural language, and receive answers supported by relevant document sources.

# 

# \## Architecture

# 

# ```text

# Document Upload

# &#x20;     ↓

# PDF Parsing

# &#x20;     ↓

# Text Chunking

# &#x20;     ↓

# Embeddings ───────────────→ PostgreSQL + pgvector

# &#x20;     ↓

# User Question

# &#x20;     ↓

# &#x20;┌───────────────────────┐

# &#x20;│ Hybrid Retrieval      │

# &#x20;│                       │

# &#x20;│ Vector Search         │

# &#x20;│ BM25 Keyword Search   │

# &#x20;└───────────────────────┘

# &#x20;     ↓

# Reciprocal Rank Fusion

# &#x20;     ↓

# Cohere Reranking

# &#x20;     ↓

# LLM Response Generation

# &#x20;     ↓

# Answer + Source Citations


