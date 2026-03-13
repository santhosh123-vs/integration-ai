"""
Vector Database for API Matching using ChromaDB
"""
import chromadb
from chromadb.utils import embedding_functions
from config import APIS

# Initialize ChromaDB
chroma_client = chromadb.Client()

# Use default embedding function
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Create or get collection
collection = chroma_client.get_or_create_collection(
    name="api_collection",
    embedding_function=embedding_fn
)

def initialize_database():
    """Load all APIs into vector database"""
    
    # Clear existing data
    try:
        existing = collection.get()
        if existing['ids']:
            collection.delete(ids=existing['ids'])
    except:
        pass
    
    # Prepare documents
    documents = []
    metadatas = []
    ids = []
    
    for api_id, api_info in APIS.items():
        # Create rich document for embedding
        doc = f"{api_info['name']}. {api_info['description']}. Keywords: {', '.join(api_info['keywords'])}. Category: {api_info['category']}"
        
        documents.append(doc)
        metadatas.append({
            "api_id": api_id,
            "name": api_info["name"],
            "category": api_info["category"],
            "parameters": ", ".join(api_info["parameters"])
        })
        ids.append(api_id)
    
    # Add to collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    return len(documents)

def search_apis(query: str, top_k: int = 5):
    """Search for matching APIs based on natural language query"""
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    matched_apis = []
    
    if results and results['ids'] and results['ids'][0]:
        for i, api_id in enumerate(results['ids'][0]):
            api_info = APIS.get(api_id, {})
            distance = results['distances'][0][i] if results['distances'] else 0
            
            # Convert distance to confidence score (lower distance = higher confidence)
            confidence = max(0, min(100, (1 - distance / 2) * 100))
            
            matched_apis.append({
                "api_id": api_id,
                "name": api_info.get("name", ""),
                "description": api_info.get("description", ""),
                "category": api_info.get("category", ""),
                "parameters": api_info.get("parameters", []),
                "confidence": round(confidence, 2)
            })
    
    return matched_apis

def get_collection_count():
    """Get number of items in collection"""
    return collection.count()

if __name__ == "__main__":
    print("🔧 Initializing API Vector Database...")
    count = initialize_database()
    print(f"✅ Loaded {count} APIs into vector database")
    
    # Test search
    print("\n🔍 Testing search: 'send email to john'")
    results = search_apis("send email to john", top_k=3)
    for r in results:
        print(f"   {r['confidence']:.1f}% - {r['name']}")
