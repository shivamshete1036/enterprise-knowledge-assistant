# Enterprise Knowledge Assistant

An AI-powered Enterprise Knowledge Assistant built using **LangGraph**, **RAG**, **MCP**, **Guardrails**, **RAGAS**, **LangSmith**, and **Streamlit**.

## Features

- Enterprise knowledge retrieval using RAG and ChromaDB
- LangGraph-based workflow orchestration
- MCP integration for IT support tickets
- PII protection using Guardrails AI and Microsoft Presidio
- RAGAS evaluation using Faithfulness and Answer Relevancy
- LangSmith observability and tracing
- Streamlit user interface
- Reproducible dependency management with `uv`

## Architecture

```text
User → Streamlit → LangGraph → Input Guard → Router
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                    Knowledge                    Action
                         │                         │
                    Retriever                 MCP Agent
                         │                    ┌────┼────┐
                      ChromaDB             Create  Get    Search
                         │                  Ticket Ticket  Tickets
                    Response Agent               │
                         │                  MCP Server
                    Output Guard
                         │
                    RAGAS Evaluator
                         │
                        END

                  LangSmith Observability
```

## RAG Pipeline

```text
Knowledge Base → Document Loader → Chunking
→ Sentence Transformer → Embeddings → ChromaDB
→ Semantic Retrieval → LLM Response
```

Embedding model:

```text
all-MiniLM-L6-v2
```

## LangGraph Orchestration

### Knowledge request

```text
Input Guard → Router → Retriever → Response Agent
→ Output Guard → RAGAS Evaluator → END
```

Example:

```text
How many annual leave days does a full-time employee receive?
```

### MCP action request

```text
Input Guard → Router → MCP Agent → MCP Server → Ticket Operation → END
```

Example:

```text
Create a high priority support ticket because employees cannot connect to the corporate VPN.
```

## MCP Integration

The MCP server currently exposes three tools:

### `create_ticket`

Creates a support ticket.

```text
Create a high priority support ticket because employees cannot connect to the corporate VPN.
```

### `get_ticket`

Retrieves an existing ticket.

```text
Give me the details of TKT-0016.
```

### `search_tickets`

Searches support tickets.

```text
Find all support tickets related to VPN.
```

## Guardrails and PII Protection

PII protection uses:

- Guardrails AI
- Microsoft Presidio
- spaCy

Protected information includes:

```text
EMAIL
PHONE
CREDIT CARD
IP ADDRESS
PAN
AADHAAR
PASSPORT
```

Example:

```text
Original:
My email is shivam@example.com. What does the company say about working from home?

Sanitized:
My email is [EMAIL_REDACTED]. What does the company say about working from home?
```

## RAGAS Evaluation

The system evaluates:

- **Faithfulness** — whether the answer is supported by retrieved context.
- **Answer Relevancy** — whether the answer is relevant to the user's question.

Example:

```text
Faithfulness: 1.0000
Answer Relevancy: 0.9274
```

## LangSmith Observability

LangSmith is used for application tracing and observability.

Example configuration:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=enterprise-knowledge-assistant
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Environment Management | uv |
| UI | Streamlit |
| Orchestration | LangGraph |
| LLM Framework | LangChain |
| RAG | Retrieval-Augmented Generation |
| Embeddings | Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| Document Processing | PyPDF |
| MCP | Model Context Protocol |
| MCP Server | FastMCP |
| Guardrails | Guardrails AI |
| PII Detection | Microsoft Presidio |
| NLP | spaCy |
| Evaluation | RAGAS |
| Observability | LangSmith |

## Project Structure

```text
enterprise-knowledge-assistant/
├── app.py
├── config/
├── data/
│   └── chroma/
├── evaluation/
├── graph/
│   ├── workflow.py
│   ├── state.py
│   └── nodes/
├── knowledge_base/
├── mcp_client/
│   └── ticket_client.py
├── mcp_server/
│   └── ticket_server.py
├── rag/
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── index_knowledge_base.py
├── tests/
├── utils/
│   └── guardrails/
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requirements

The currently tested environment uses:

```text
Python 3.10
uv
```

The project is configured for:

```text
>=3.10,<3.11
```

## Installation

### Clone the repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-knowledge-assistant
```

### Install dependencies

```powershell
uv sync
```

The committed `pyproject.toml` and `uv.lock` recreate the tested dependency environment.

## Environment Configuration

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=your_google_api_key

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=enterprise-knowledge-assistant
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

```

## Knowledge Base Indexing

Place enterprise `.txt` documents inside:

```text
knowledge_base/
```

Run:

```powershell
uv run python -m rag.index_knowledge_base
```

The indexing process is:

```text
Documents → Loading → Chunking → Embedding → ChromaDB
```

## Running the Application

```powershell
uv run streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Testing

### Full MCP + LangGraph Integration

```powershell
uv run python -m tests.test_mcp_full_graph
```

This verifies RAG retrieval, MCP ticket creation, ticket retrieval, ticket search, and LangGraph routing.

### PII Sanitization

```powershell
uv run python -m tests.test_pii_sanitization
```

### Full Graph PII Protection

```powershell
uv run python -m tests.test_full_graph
```

### LangSmith Connection

```powershell
uv run python -m tests.test_langsmith_connection
```

Expected:

```text
LangSmith connection successful
```

### LangSmith Trace

```powershell
uv run python -m tests.test_langsmith_trace
```

## Example Queries

### Knowledge

```text
How many annual leave days does a full-time employee receive?
```

```text
What is the company VPN policy?
```

```text
What are the standard working hours?
```

```text
Can employees work remotely?
```

### MCP

Create a ticket:

```text
Create a high priority support ticket because employees cannot connect to the corporate VPN.
```

Get a ticket:

```text
Give me the details of TKT-0016.
```

Search tickets:

```text
Find all support tickets related to VPN.
```

## Dependency Management

The project uses `uv` for reproducible dependency management.

- `pyproject.toml` defines project dependencies.
- `uv.lock` contains the exact resolved dependency versions.

For a new machine:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-knowledge-assistant
uv sync
uv run streamlit run app.py
```

## Security

The project includes:

- PII detection and sanitization
- Guardrails before LLM processing
- Environment-based secret management
- Grounded responses using retrieved enterprise documents
- MCP-based separation for external ticket operations

## Current MCP Tools

```text
1. create_ticket
2. get_ticket
3. search_tickets
```
## Project Goal

The goal of this project is to demonstrate an enterprise AI assistant combining:

```text
RAG
+
LangGraph
+
MCP
+
Guardrails
+
RAGAS
+
LangSmith
```

to provide grounded knowledge retrieval, safe LLM interactions, external system integration, response evaluation, and end-to-end observability.
