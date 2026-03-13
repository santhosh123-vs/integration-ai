"""
Integration AI - Streamlit Dashboard
"""
import streamlit as st
import requests
import json
import time

# API URL - Change for deployment
API_URL = "http://localhost:8003"

st.set_page_config(
    page_title="Integration AI",
    page_icon="🔌",
    layout="wide"
)

# Header
st.markdown("""
<h1 style='text-align: center;'>🔌 Integration AI</h1>
<p style='text-align: center; color: #666;'>Natural Language to API Router using RAG</p>
<hr>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🎯 Route Query", "📦 Batch Process", "🔍 Search APIs", "📋 All APIs"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Built by Kethavath Santhosh**")
st.sidebar.markdown("[GitHub](https://github.com/santhosh123-vs)")

def check_api():
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        return r.status_code == 200
    except:
        return False

# Check API Status
api_status = check_api()
if api_status:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Disconnected")
    st.error("⚠️ API server not running. Start with: `python main.py`")

# Page: Route Query
if page == "🎯 Route Query":
    st.header("🎯 Route Natural Language to API")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter your request:",
            placeholder="e.g., Send an email to john@example.com about the meeting"
        )
    
    with col2:
        top_k = st.number_input("Top K Results", min_value=1, max_value=10, value=3)
    
    # Example queries
    st.markdown("**Try these examples:**")
    examples = [
        "Send an email to john@example.com about the meeting",
        "Create a calendar event for tomorrow at 3pm",
        "Post a tweet about our new product launch",
        "Search for files in Google Drive",
        "Create a new Jira ticket for the bug",
        "Schedule a Zoom meeting for Friday",
        "Upload file to Dropbox",
        "Get weather in New York"
    ]
    
    cols = st.columns(4)
    for i, ex in enumerate(examples):
        if cols[i % 4].button(ex[:30] + "...", key=f"ex_{i}"):
            query = ex
    
    if st.button("🚀 Route Query", type="primary") and query:
        with st.spinner("Routing..."):
            try:
                start = time.time()
                r = requests.post(
                    f"{API_URL}/route",
                    json={"query": query, "top_k": top_k},
                    timeout=30
                )
                result = r.json()
                latency = (time.time() - start) * 1000
                
                if result.get("success"):
                    match = result["best_match"]
                    
                    # Best Match Card
                    st.success(f"✅ Matched: **{match['name']}**")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Confidence", f"{match['confidence']}%")
                    col2.metric("Category", match['category'].title())
                    col3.metric("Latency", f"{latency:.0f}ms")
                    
                    # Parameters
                    st.subheader("🔧 Extracted Parameters")
                    st.json(match['parameters'])
                    
                    # API Details
                    with st.expander("📋 API Details"):
                        st.write(f"**API ID:** `{match['api_id']}`")
                        st.write(f"**Description:** {match['description']}")
                    
                    # Alternative Matches
                    if result.get("alternative_matches"):
                        st.subheader("🔄 Alternative Matches")
                        for alt in result["alternative_matches"]:
                            st.write(f"- **{alt['name']}** ({alt['confidence']}%) - {alt['category']}")
                else:
                    st.error("❌ No matching API found")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Page: Batch Process
elif page == "📦 Batch Process":
    st.header("📦 Batch Process Multiple Queries")
    
    queries_text = st.text_area(
        "Enter queries (one per line):",
        height=200,
        placeholder="Send email to john\nCreate calendar event\nPost tweet"
    )
    
    if st.button("🚀 Process Batch", type="primary") and queries_text:
        queries = [q.strip() for q in queries_text.split("\n") if q.strip()]
        
        with st.spinner(f"Processing {len(queries)} queries..."):
            try:
                r = requests.post(
                    f"{API_URL}/batch",
                    json={"queries": queries},
                    timeout=60
                )
                result = r.json()
                
                st.success(f"✅ Processed {result['total_queries']} queries in {result['latency_ms']}ms")
                
                for i, res in enumerate(result['results']):
                    if res['success']:
                        match = res['best_match']
                        st.write(f"**{i+1}. {res['query']}**")
                        st.write(f"   → {match['name']} ({match['confidence']}%)")
                    else:
                        st.write(f"**{i+1}. {res['query']}** → ❌ No match")
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Page: Search APIs
elif page == "🔍 Search APIs":
    st.header("🔍 Search Available APIs")
    
    search_query = st.text_input("Search:", placeholder="email, calendar, slack...")
    
    if search_query:
        try:
            r = requests.get(f"{API_URL}/search", params={"q": search_query, "limit": 10})
            result = r.json()
            
            st.write(f"Found **{result['count']}** matching APIs:")
            
            for api in result['results']:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    col1.write(f"**{api['name']}**")
                    col2.write(f"{api['confidence']}%")
                    st.write(f"*{api['description']}*")
                    st.write(f"Category: `{api['category']}` | Parameters: `{api['parameters']}`")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Page: All APIs
elif page == "📋 All APIs":
    st.header("📋 All Available APIs")
    
    try:
        r = requests.get(f"{API_URL}/apis")
        result = r.json()
        
        st.write(f"**Total APIs:** {result['total']}")
        
        # Group by category
        categories = {}
        for api_id, api in result['apis'].items():
            cat = api['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({"id": api_id, **api})
        
        for cat, apis in sorted(categories.items()):
            with st.expander(f"📁 {cat.title()} ({len(apis)} APIs)"):
                for api in apis:
                    st.write(f"**{api['name']}** (`{api['id']}`)")
                    st.write(f"*{api['description']}*")
                    st.write(f"Parameters: `{', '.join(api['parameters'])}`")
                    st.markdown("---")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #888;'>
    Integration AI v1.0 | Built with FastAPI + ChromaDB + Groq | 
    <a href='https://github.com/santhosh123-vs'>GitHub</a>
</p>
""", unsafe_allow_html=True)
