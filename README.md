# Integration AI

Natural Language to API Router using RAG and LLM Re-ranking

## Features
- 30 APIs across 10 categories
- RAG-based semantic search with ChromaDB
- LLM Re-ranking for 100% accuracy
- Parameter extraction from natural language
- REST API and Streamlit Dashboard

## Tech Stack
Python, FastAPI, ChromaDB, Groq LLM, Streamlit

## Quick Start
1. Clone repo
2. Create venv and activate
3. pip install -r requirements.txt
4. Add GROQ_API_KEY to .env
5. Run: python main.py

## API Endpoints
- GET / - Health check
- POST /route - Route single query
- POST /batch - Route multiple queries
- GET /apis - List all APIs

## Live Demo
- API: https://integration-ai.onrender.com

## Author
Kethavath Santhosh - github.com/santhosh123-vs
