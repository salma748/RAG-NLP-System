# Mini-RAG: Recipe Knowledge Assistant

## Overview

Mini-RAG is a containerized Retrieval-Augmented Generation (RAG) system built with FastAPI. The system enables intelligent natural-language querying over a collection of recipe documents and can answer questions about ingredients, cooking steps, quantities, and preparation instructions in both English and Arabic.

The application processes raw HTML recipe files, converts them into semantic embeddings, stores them in a vector database, retrieves the most relevant information for a user query, and generates context-aware answers using a Large Language Model (LLM).

---

## Features

* HTML recipe document ingestion
* English and Arabic language support
* Custom parsing and preprocessing pipeline
* Token-based chunking strategy
* Semantic embeddings using Sentence Transformers
* Vector similarity search with Qdrant
* MongoDB document storage
* FastAPI REST API
* Dockerized deployment
* Retrieval-Augmented Generation (RAG)
* Factory Design Pattern for LLM and Vector Database providers

---

## System Architecture

```text
User Query
    │
    ▼
FastAPI API Layer
    │
    ▼
Embedding Model
    │
    ▼
Qdrant Vector Database
    │
    ▼
Top-K Retrieval
    │
    ▼
LLM Context Injection
    │
    ▼
Generated Answer
```

### Architecture Layers

1. Client Layer

   * Streamlit UI
   * HTTP Client

2. API Layer

   * FastAPI routes
   * Health checks
   * Upload endpoints
   * Processing endpoints
   * Search endpoints
   * Answer generation endpoints

3. Controller Layer

   * File management
   * Data processing
   * Chunk generation
   * Vector search
   * RAG answer generation

4. Data Layer

   * MongoDB
   * Project storage
   * Chunk storage

5. Stores Layer

   * LLM Factory
   * VectorDB Factory
   * Embedding Provider
   * Prompt Templates

6. Infrastructure Layer

   * Docker
   * Docker Compose
   * MongoDB Container
   * Qdrant Container
   * FastAPI Container

---

## Workflow

### 1. Ingest

HTML recipe files are uploaded and stored under a project namespace.

### 2. Process

The uploaded files are parsed, cleaned, and split into semantic chunks.

### 3. Index

Chunks are embedded using a multilingual Sentence Transformer model and stored in Qdrant.

### 4. Query

User questions are embedded and matched against indexed chunks using cosine similarity.

### 5. Generate

The most relevant chunks are injected into an LLM prompt to generate the final answer.

---

## Embedding Model

Model:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Configuration:

* Embedding Dimension: 384
* Similarity Metric: Cosine Similarity

---

## Chunking Strategy

* Chunk Size: 500 Tokens
* Overlap: 50 Tokens

This strategy balances retrieval accuracy with contextual completeness while reducing information loss between chunks.

---

## API Endpoints

### Health Check

```http
GET /api/
```

Returns application status.

---

### Upload File

```http
POST /api/data/upload/{project_id}
```

Uploads an HTML recipe document.

---

### Process Documents

```http
POST /api/data/process/{project_id}
```

Parses files and creates chunks.

---

### Push Embeddings to Vector Store

```http
POST /api/nlp/index/push/{project_id}
```

Generates embeddings and stores them in Qdrant.

---

### Search Similar Chunks

```http
POST /api/nlp/index/search/{project_id}
```

Retrieves top-k relevant chunks.

---

### Generate Answer

```http
POST /api/nlp/index/answer/{project_id}
```

Executes the complete Retrieval-Augmented Generation pipeline.

---

## Technologies Used

* Python
* FastAPI
* MongoDB
* Qdrant
* Docker
* Docker Compose
* Sentence Transformers
* OpenAI-Compatible LLM APIs
* Streamlit

---

## Running the Project

### Prerequisites

* Docker Engine 24+
* Docker Compose v2

### Build and Run

```bash
docker compose up --build
```

### Services

* FastAPI Application
* MongoDB
* Qdrant

---

## Project Structure

```text
RAG-NLP-System
│
├── src/
├── docker/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── docs/
    └── Mini_RAG_Technical_Report.pdf
```

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

This project was developed as part of the NLP Engineering Project and demonstrates the design and implementation of a production-oriented Retrieval-Augmented Generation (RAG) system using modern NLP, vector databases, software engineering principles, and containerized deployment.
