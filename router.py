"""
AI Router - Routes natural language to correct API using RAG + LLM Re-ranking (v2)
"""
import os
import json
from groq import Groq
from dotenv import load_dotenv
from vector_db import search_apis, initialize_database
from config import APIS, MODEL

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def rerank_with_llm(query: str, candidates: list) -> list:
    """Use LLM to re-rank API candidates for better accuracy"""
    
    candidate_text = ""
    for i, c in enumerate(candidates):
        candidate_text += f"{i+1}. {c['api_id']}: {c['name']} - {c['description']}\n"
    
    # === PROMPT IMPROVEMENT v2 ===
    prompt = f"""You are an expert API router. Your job is to find the single best API that performs the user's primary action.
Pay close attention to main verbs like 'send', 'create', 'post', 'search', 'get', 'convert'.

User Request: "{query}"

Candidate APIs:
{candidate_text}

Analyze the user's primary goal and pick the best matching API.
Return ONLY a JSON object with:
- "best_api_index": the number (1-{len(candidates)}) of the best match
- "confidence": your confidence 0-100

Return ONLY valid JSON, no explanation."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0, # Set to 0 for deterministic output
            max_tokens=100
        )
        
        result = response.choices[0].message.content.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        result = result.strip()
        
        parsed = json.loads(result)
        best_idx = int(parsed.get("best_api_index", 1)) - 1
        confidence = float(parsed.get("confidence", 50))
        
        if 0 <= best_idx < len(candidates):
            best = candidates[best_idx]
            best["confidence"] = confidence
            remaining = [c for i, c in enumerate(candidates) if i != best_idx]
            return [best] + remaining
    except:
        pass
    
    return candidates

def extract_parameters(query: str, api_info: dict) -> dict:
    prompt = f"""Extract parameters from this user request for the API action.
User Request: "{query}"
API: {api_info['name']}
Required Parameters: {', '.join(api_info['parameters'])}
Return ONLY valid JSON. If a value is not found, use null."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"): result = result[4:]
        return json.loads(result.strip())
    except:
        return {param: None for param in api_info['parameters']}

def route_query(query: str, top_k: int = 10) -> dict:
    matches = search_apis(query, top_k=top_k)
    if not matches: return {"success": False, "message": "No matching API found"}
    matches = rerank_with_llm(query, matches)
    best_match = matches[0]
    api_id = best_match['api_id']
    api_info = APIS.get(api_id, {})
    parameters = extract_parameters(query, api_info)
    return {
        "success": True, "query": query,
        "best_match": {
            "api_id": api_id, "name": best_match['name'], "description": best_match['description'],
            "category": best_match['category'], "confidence": best_match['confidence'], "parameters": parameters
        },
        "alternative_matches": matches[1:] if len(matches) > 1 else []
    }

def batch_route(queries: list) -> list:
    return [route_query(query) for query in queries]

if __name__ == "__main__":
    print("🚀 Integration AI - NL to API Router (v2 - Improved Prompt)")
    print("="*50)
    initialize_database()
    print("✅ Database Initialized")
    
    test_queries = [
        "Send an email to todome6258@flosek.com about the project update",
        "Create a calendar event for tomorrow at 3pm",
        "Post a tweet about our new product launch",
        "Send slack message to the team about deployment",
        "Create a new Jira ticket for the login bug"
    ]
    
    print("\n🧪 Testing Router with Improved Prompt:")
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = route_query(query)
        if result['success']:
            match = result['best_match']
            print(f"   ✅ Matched: {match['name']}")
            print(f"   📊 Confidence: {match['confidence']}%")
            print(f"   🔧 Parameters: {match['parameters']}")
        else:
            print(f"   ❌ No match found")
