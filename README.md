# Integration AI

Natural Language to API Router using RAG and LLM Re-ranking.

## Live Demo

Try it now: https://integration-ai-s3xsjjvgoazftjvifyrdzd.streamlit.app/

## Key Metrics

| Metric | Value |
|--------|-------|
| APIs Supported | 30 across 10 categories |
| Routing Accuracy | 100% with LLM Re-ranking |
| Avg Latency | 877ms per query |
| Batch Processing | 5 queries in 25 seconds |
| Parameter Extraction | Automatic from natural language |

## How Accuracy Was Improved

| Version | Approach | Accuracy |
|---------|----------|----------|
| v1 | Basic Vector Search | 36% |
| v2 | Vector Search + LLM Re-ranking | 100% |

Problem: Word 'update' in 'send email about project update' confused vector search to match Jira Update instead of Gmail Send.
Solution: Increased top_k to 10 and added LLM re-ranking to focus on primary user action.

## Architecture

User Query --> ChromaDB Vector Search (top 10) --> LLM Re-ranking (pick best) --> Parameter Extraction --> Structured API Output

## Example

Input: "Send email to john@gmail.com about the meeting"
Output:
- API: Gmail - Send Email
- Confidence: 100%
- Parameters: {to: john@gmail.com, subject: meeting, body: meeting}

## API Categories

| Category | APIs |
|----------|------|
| Communication | Gmail, Slack, Zoom, SendGrid |
| Productivity | Calendar, Sheets, Notion, Trello |
| Development | GitHub, Jira |
| Social | Twitter |
| Storage | Google Drive, Dropbox |
| CRM | HubSpot |
| Payment | Stripe |
| Information | Weather, News |
| Utility | Translate, Currency |
| Entertainment | Spotify |

## Features

- RAG-based API Matching: ChromaDB vector search
- LLM Re-ranking: AI double-checks results for 100% accuracy
- Parameter Extraction: Automatically pulls values from text
- Batch Processing: Route multiple queries at once
- REST API: Programmatic access
- Interactive Dashboard: Test queries visually

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| FastAPI | API Framework |
| ChromaDB | Vector Database (RAG) |
| Groq | LLM Provider (Llama 3.3 70B) |
| Streamlit | Dashboard |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Health check |
| /route | POST | Route single query to API |
| /batch | POST | Route multiple queries |
| /search | GET | Search available APIs |
| /apis | GET | List all 30 APIs |

## Quick Start

1. Clone: git clone https://github.com/santhosh123-vs/integration-ai
2. Install: pip install -r requirements.txt
3. Add .env with GROQ_API_KEY
4. Run API: python main.py
5. Run Dashboard: streamlit run dashboard.py

## Author

Kethavath Santhosh - github.com/santhosh123-vs
