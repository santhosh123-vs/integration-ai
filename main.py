"""
Integration AI - FastAPI Server
NL to API Router with RAG
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time

from vector_db import initialize_database, search_apis, get_collection_count
from router import route_query, batch_route
from config import get_all_apis, get_categories

# Initialize FastAPI
app = FastAPI(
    title="Integration AI",
    description="Natural Language to API Router using RAG",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup():
    print("🚀 Starting Integration AI...")
    count = initialize_database()
    print(f"✅ Loaded {count} APIs into vector database")

# Request Models
class RouteRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class BatchRouteRequest(BaseModel):
    queries: List[str]
    top_k: Optional[int] = 3

# Endpoints
@app.get("/")
async def root():
    return {
        "name": "Integration AI",
        "description": "Natural Language to API Router",
        "version": "1.0.0",
        "total_apis": len(get_all_apis()),
        "categories": get_categories(),
        "endpoints": ["/route", "/batch", "/search", "/apis"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "apis_loaded": get_collection_count()
    }

@app.post("/route")
async def route_nl_to_api(request: RouteRequest):
    """Route natural language to best matching API"""
    start_time = time.time()
    
    result = route_query(request.query, request.top_k)
    
    result["latency_ms"] = round((time.time() - start_time) * 1000, 2)
    
    return result

@app.post("/batch")
async def batch_route_queries(request: BatchRouteRequest):
    """Route multiple queries at once"""
    start_time = time.time()
    
    results = batch_route(request.queries)
    
    return {
        "total_queries": len(request.queries),
        "results": results,
        "latency_ms": round((time.time() - start_time) * 1000, 2)
    }

@app.get("/search")
async def search(q: str, limit: int = 5):
    """Search APIs by query"""
    results = search_apis(q, top_k=limit)
    return {
        "query": q,
        "results": results,
        "count": len(results)
    }

@app.get("/apis")
async def list_apis():
    """List all available APIs"""
    apis = get_all_apis()
    return {
        "total": len(apis),
        "apis": apis
    }

@app.get("/apis/{api_id}")
async def get_api(api_id: str):
    """Get specific API details"""
    apis = get_all_apis()
    if api_id not in apis:
        raise HTTPException(status_code=404, detail="API not found")
    return apis[api_id]

@app.get("/categories")
async def list_categories():
    """List all API categories"""
    return {
        "categories": get_categories()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
