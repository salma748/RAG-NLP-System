# Mini-RAG: Recipe Knowledge Assistant

## Overview

Mini-RAG is a containerized Retrieval-Augmented Generation (RAG) system developed as part of an NLP Engineering Project.

The system enables intelligent question answering over recipe documents by combining semantic search with Large Language Models (LLMs). Users can upload recipe documents, process and index them, and ask questions in natural language to receive context-aware answers grounded in the retrieved content.

The project supports both English and Arabic queries and follows clean software engineering practices through a layered architecture, Factory Design Pattern, and Docker-based deployment.

---

## Key Features

* Retrieval-Augmented Generation (RAG)
* English and Arabic language support
* HTML document ingestion and processing
* Semantic chunking and indexing
* Vector similarity search using Qdrant
* MongoDB document storage
* FastAPI REST API
* Dockerized deployment
* Factory Pattern for LLM providers
* Factory Pattern for Vector Database providers
* Modular and maintainable architecture

---

## Technology Stack

### Backend

* FastAPI
* Python

### Databases

* MongoDB
* Qdrant Vector Database

### NLP

* Sentence Transformers
* OpenAI-Compatible LLM APIs

### Infrastructure

* Docker
* Docker Compose

---

## System Workflow

1. Upload HTML recipe documents.
2. Parse and clean document content.
3. Split content into chunks.
4. Generate embeddings for chunks.
5. Store embeddings in Qdrant.
6. Store metadata and chunks in MongoDB.
7. Receive a user query.
8. Retrieve the most relevant chunks.
9. Inject retrieved context into the LLM prompt.
10. Generate a grounded answer.

---

## Embedding Model

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### Configuration

* Embedding Dimension: 384
* Similarity Metric: Cosine Similarity

---

## Chunking Strategy

| Parameter  | Value      |
| ---------- | ---------- |
| Chunk Size | 500 Tokens |
| Overlap    | 50 Tokens  |

This strategy helps preserve context across chunk boundaries while maintaining efficient retrieval performance.

---

## API Endpoints

### Health Check

```http
GET /api/
```

### Upload Documents

```http
POST /api/data/upload/{project_id}
```

### Process Documents

```http
POST /api/data/process/{project_id}
```

### Generate and Store Embeddings

```http
POST /api/nlp/index/push/{project_id}
```

### Semantic Search

```http
POST /api/nlp/index/search/{project_id}
```

### RAG Question Answering

```http
POST /api/nlp/index/answer/{project_id}
```

---

## Project Structure

```text
src/
├── controllers/
├── helpers/
├── models/
├── routes/
├── stores/
│   ├── llm/
│   │   ├── LLMFactory.py
│   │   └── LLMInterface.py
│   │
│   └── vectordb/
│       ├── VectorDBFactory.py
│       └── VectorDBInterface.py
│
├── main.py

docker/
├── mongodb/
└── qdrant_data/

Dockerfile
docker-compose.yaml
requirements.txt
```

---

## Design Patterns

### LLM Factory Pattern

The system uses an LLM Factory Pattern that abstracts the underlying language model provider and allows switching between providers without changing business logic.

### Vector Database Factory Pattern

A VectorDB Factory Pattern abstracts vector database implementations, making the retrieval layer extensible and maintainable.

---

## Running the Project

### Prerequisites

* Docker Engine 24+
* Docker Compose v2

### Build and Run

```bash
docker compose up --build
```

### Services Started

* FastAPI Application
* MongoDB Container
* Qdrant Container

---

## Documentation

The complete technical report is available in:

```text
docs/Mini_RAG_Technical_Report.pdf
```

---

## Team 37

* Salma Mohamed Hafez
* Hager Ibrahim Shaaban
* Farah Mohamed Mostafa
* Sama Mohamed Ali
* Shady Ahmed Soliman
* Salma Fathy Saeed

---

## Academic Project

This project was developed for the NLP Engineering Project and demonstrates the implementation of a production-oriented Retrieval-Augmented Generation (RAG) pipeline using modern NLP techniques, vector databases, software engineering principles, and containerized deployment.
