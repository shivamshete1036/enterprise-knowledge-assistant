# Enterprise Knowledge Assistant

An AI-powered Enterprise Knowledge Assistant built with **LangGraph, RAG, RAGAS, Guardrails, and MCP**.

The system can answer questions from an enterprise knowledge base, protect sensitive information, evaluate generated answers, and interact with an external ticketing system through a custom MCP server.

## Problem Statement

Organizations store information across multiple systems such as knowledge repositories, policy documents, ticketing systems, CRM applications, and project management tools.

Employees often spend significant time searching for accurate and up-to-date information from these disconnected sources.

This project demonstrates an AI-powered enterprise assistant that:

- Retrieves relevant information from an enterprise knowledge base.
- Generates grounded responses using retrieved context.
- Protects sensitive information using guardrails.
- Evaluates RAG responses using RAGAS.
- Routes action-oriented requests to an MCP-based external system.
- Creates enterprise support tickets through MCP.

## Key Features

### Knowledge Assistant

- Semantic search over enterprise documents.
- ChromaDB vector database.
- Sentence Transformers embeddings.
- Context-grounded answer generation.
- Prevents unsupported information from being generated.

### Intelligent Request Routing

The LangGraph workflow distinguishes between knowledge requests and action requests.

**Knowledge request:**

```text
What is the company's work-from-home policy?
```

**Action request:**

```text
Create a high priority support ticket because employees cannot connect to VPN.
```

Knowledge requests are routed through the RAG pipeline. Action requests are routed to the MCP agent.

### Guardrails

The application includes:

- Input PII detection.
- Output PII protection.
- Presidio-based validation.
- Sensitive information blocking before it reaches the LLM.

### RAGAS Evaluation

The generated RAG responses are evaluated using:

- Faithfulness
- Answer Relevancy

The evaluation scores are stored in the LangGraph state.

### MCP Integration

The application integrates with a custom MCP ticketing system.

Available MCP tools:

```text
create_ticket
get_ticket
search_tickets
```

The current LangGraph MCP agent uses `create_ticket`.

### Ticket Creation

For example:

```text
Create a high priority support ticket because employees
cannot connect to the corporate VPN.
```

The system creates:

```text
Ticket ID: TKT-0001
Title: VPN connection issue
Priority: high
Status: open
```

## System Architecture

```text
                         User
                           |
                           v
                    +-------------+
                    | Input Guard |
                    +------+------+
                           |
                           v
                    +-------------+
                    |   Router    |
                    +------+------+
                           |
             +-------------+-------------+
             |                           |
        Knowledge                     Action
             |                           |
             v                           v
       +-----------+              +-------------+
       | Retriever |              | MCP Agent   |
       +-----+-----+              +------+------+
             |                           |
             v                           v
       +-----------+              +-------------+
       | Response  |              | MCP Client  |
       |   Agent   |              +------+------+
       +-----+-----+                     |
             |                            v
             v                    +-------------+
       +-------------+             | FastMCP     |
       | Output Guard|             | Server      |
       +------+------+
              |                           |
              v                           v
       +-------------+              +-------------+
       |    RAGAS    |              | Ticket DB   |
       |  Evaluator  |              |   SQLite    |
       +-------------+              +-------------+
```

## LangGraph Workflow

### Knowledge Request

```text
START
  |
  v
Input Guard
  |
  v
Router
  |
  v
Retriever
  |
  v
Response Agent
  |
  v
Output Guard
  |
  v
RAGAS Evaluator
  |
  v
END
```

### Action Request

```text
START
  |
  v
Input Guard
  |
  v
Router
  |
  v
MCP Agent
  |
  v
MCP Client
  |
  v
FastMCP Server
  |
  v
SQLite
  |
  v
END
```

This routing prevents action requests from unnecessarily going through the RAG and RAGAS pipeline.

## RAG Pipeline

```text
Enterprise Documents
        |
        v
Document Loader
        |
        v
Chunking
        |
        v
Sentence Transformer
        |
        v
Embeddings
        |
        v
ChromaDB
        |
        v
Semantic Retrieval
        |
        v
LLM
        |
        v
Grounded Answer
```

### Components

- **Document Loader** — loads enterprise knowledge documents.
- **Chunker** — splits documents into smaller chunks.
- **Embedding Model** — `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector Store** — ChromaDB.
- **Retriever** — retrieves the most relevant documents.
- **Response Agent** — generates an answer using only retrieved context.

## Guardrails

The project uses Guardrails and Microsoft Presidio components to protect sensitive information.

### Input Protection

Sensitive information is detected before the request reaches the RAG or MCP pipeline.

Example:

```text
My email is shivam@example.com.
What is the work-from-home policy?
```

The input guard blocks the request.

### Output Protection

Generated responses are also checked before being returned to the user.

This helps prevent accidental exposure of sensitive information.

## RAGAS Evaluation

RAG responses are evaluated using RAGAS.

### Faithfulness

Measures whether the generated answer is supported by the retrieved context.

### Answer Relevancy

Measures how relevant the generated answer is to the user's question.

Example:

```python
{
    "faithfulness": 1.0,
    "answer_relevancy": 0.67
}
```

The project uses:

```text
RAGAS: 0.4.3
Instructor: 1.15.4
```

The RAGAS evaluator uses the Ollama OpenAI-compatible API.

## MCP Integration

The project contains a custom MCP server for an enterprise ticketing system.

### MCP Architecture

```text
LangGraph MCP Agent
        |
        v
    MCP Client
        |
        v
 MCP Protocol
        |
        v
   FastMCP Server
        |
        v
   Ticket System
        |
        v
      SQLite
```

### MCP Server

```text
mcp_server/ticket_server.py
```

### MCP Client

```text
mcp_client/ticket_client.py
```

### Available Tools

```text
create_ticket
get_ticket
search_tickets
```

The LangGraph MCP agent currently uses `create_ticket`. The server already exposes `get_ticket` and `search_tickets`, which can be integrated into the agent later.

## Example MCP Interaction

### User Request

```text
Create a high priority support ticket because employees
cannot connect to the corporate VPN.
```

### Router

```text
ACTION
```

### MCP Agent

```text
Detected priority: high
Ticket title: VPN connection issue
```

### MCP Server

```text
{
    "success": true,
    "ticket_id": "TKT-0001",
    "title": "VPN connection issue",
    "priority": "high",
    "status": "open"
}
```

### Final Response

```text
I've created a support ticket for you.

Ticket ID: TKT-0001
Title: VPN connection issue
Priority: High
Status: Open
```

## Project Structure

```text
enterprise-knowledge-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── config/
│   └── __init__.py
│
├── evaluation/
│   ├── ragas_evaluator.py
│   └── __init__.py
│
├── graph/
│   ├── state.py
│   ├── workflow.py
│   └── nodes/
│       ├── input_guard.py
│       ├── output_guard.py
│       ├── router.py
│       ├── retriever_agent.py
│       ├── response_agent.py
│       ├── evaluator_agent.py
│       └── mcp_agent.py
│
├── knowledge_base/
│   └── general/
│       └── company_overview.txt
│
├── mcp_client/
│   └── ticket_client.py
│
├── mcp_server/
│   └── ticket_server.py
│
├── rag/
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── index_knowledge_base.py
│
├── utils/
│   ├── ragas_compat.py
│   └── guardrails/
│       ├── input_guard.py
│       ├── output_guard.py
│       ├── pii_validator.py
│       └── presidio_config.py
│
└── tests/
    ├── test_chunker.py
    ├── test_document_loader.py
    ├── test_embeddings.py
    ├── test_end_to_end.py
    ├── test_full_graph.py
    ├── test_input_guard.py
    ├── test_mcp_graph.py
    ├── test_output_guard.py
    ├── test_ragas_evaluator.py
    ├── test_response_agent.py
    ├── test_retriever.py
    ├── test_vector_store.py
    └── test_workflow.py
```

Generated runtime data such as ChromaDB files and the SQLite ticket database are excluded from Git.

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Agent Orchestration | LangGraph |
| LLM | Ollama |
| RAG Framework | LangChain |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| Evaluation | RAGAS |
| LLM Evaluation Adapter | Instructor |
| Guardrails | Guardrails AI |
| PII Detection | Microsoft Presidio |
| Agent Tool Protocol | MCP |
| MCP Server | FastMCP |
| Ticket Database | SQLite |
| UI | Streamlit |
| Environment | uv |

## Installation

### Clone the repository

```bash
git clone https://github.com/shivamshete1036/enterprise-knowledge-assistant.git
cd enterprise-knowledge-assistant
```

### Create the environment

```bash
uv venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
uv pip install -r requirements.txt
```

## Ollama Setup

The project uses Ollama through its OpenAI-compatible API.

Make sure Ollama is installed and running.

The application currently uses:

```text
gpt-oss:120b-cloud
```

Verify the model is available through your Ollama setup before running the application.

## Knowledge Base Indexing

The enterprise knowledge base is stored under:

```text
knowledge_base/
```

To index the knowledge base:

```bash
uv run python -m rag.index_knowledge_base
```

Generated ChromaDB data is stored under:

```text
data/chroma/
```

This generated data is ignored by Git.

## Running the Application

The Streamlit interface is provided by `app.py`.

Run:

```bash
uv run streamlit run app.py
```

## Testing

The project contains component-level and integration tests.

### RAGAS

```bash
uv run python -m tests.test_ragas_evaluator
```

### Full RAG flow

```bash
uv run python -m tests.test_end_to_end
```

### MCP integration

```bash
uv run python -m tests.test_mcp_graph
```

### Full graph

```bash
uv run python -m tests.test_full_graph
```

The tests cover major components including:

- Document loading
- Chunking
- Embeddings
- Vector store
- Retrieval
- Response generation
- Input guardrails
- Output guardrails
- RAGAS evaluation
- LangGraph workflow
- MCP integration
- End-to-end execution

## Example Queries

### Knowledge Query

```text
What does the company say about working from home?
```

Expected route:

```text
Input Guard
    ↓
Router
    ↓
Retriever
    ↓
Response
    ↓
Output Guard
    ↓
RAGAS
```

### MCP Action

```text
Create a high priority support ticket because employees
cannot connect to the corporate VPN.
```

Expected route:

```text
Input Guard
    ↓
Router
    ↓
MCP Agent
    ↓
MCP Client
    ↓
FastMCP Server
    ↓
SQLite
```

### PII Protection

```text
My email is example@example.com.
What is the company work-from-home policy?
```

Expected behavior:

```text
Input Guard
    ↓
Request blocked
```

The private information should not reach the LLM.

## Design Principles

### Grounded Generation

The RAG response agent is instructed to answer only from retrieved enterprise context.

### Separation of Concerns

Different responsibilities are handled by separate LangGraph nodes:

```text
Guardrails
Retrieval
Response Generation
Evaluation
External Actions
```

### Conditional Routing

The router prevents unnecessary execution of unrelated components.

### External System Interaction

MCP provides a standardized interface between the AI agent and the enterprise ticket system.

### Evaluation

RAG responses are evaluated instead of assuming that every generated answer is correct.

## Current Limitations

- The MCP agent currently focuses on ticket creation.
- `get_ticket` and `search_tickets` are available on the MCP server but are not yet routed through natural-language requests.
- The knowledge base is currently small and can be expanded with additional enterprise documents.
- The Streamlit UI is being developed as the next integration layer.
- RAGAS evaluation is primarily applicable to knowledge/RAG requests rather than external action requests.

## Future Enhancements

Potential improvements include:

- Natural-language ticket lookup.
- Ticket search through MCP.
- Ticket status updates.
- More enterprise knowledge sources.
- Hybrid search combining semantic and keyword retrieval.
- Query rewriting.
- Reranking.
- More comprehensive RAG evaluation.
- LangSmith observability.
- Authentication and authorization.
- Conversation memory.
- Production database integration.
- Rich Streamlit dashboard.
- Human approval for sensitive enterprise actions.

## Project Goal

The goal of this project is to demonstrate an **agentic enterprise knowledge assistant** that can:

1. Understand a user's request.
2. Protect sensitive information.
3. Decide which workflow is appropriate.
4. Retrieve enterprise knowledge when required.
5. Generate grounded responses.
6. Evaluate RAG response quality.
7. Interact with external enterprise systems through MCP.
8. Return a useful action-oriented response to the user.

## License

This project is developed for educational and demonstration purposes.
