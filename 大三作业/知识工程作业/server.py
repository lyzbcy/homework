
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
from typing import List, Optional, Dict, Any

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot_graph import ChatBotGraph

app = FastAPI(title="Medical QA System API", description="API for Medical Knowledge Graph QA System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChatBot
try:
    chatbot = ChatBotGraph()
    print("ChatBot initialized successfully.")
except Exception as e:
    print(f"Error initializing ChatBot: {e}")
    chatbot = None

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    # You could add more fields here, e.g., related entities for graph visualization

class GraphNode(BaseModel):
    id: str
    label: str
    group: str

class GraphLink(BaseModel):
    source: str
    target: str
    label: str

class GraphData(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]

@app.get("/")
async def root():
    return {"message": "Medical QA System API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not chatbot:
        raise HTTPException(status_code=503, detail="ChatBot service unavailable (Neo4j connection failed?)")
    
    try:
        answer = chatbot.chat_main(request.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/sample", response_model=GraphData)
async def get_sample_graph(name: Optional[str] = None):
    """
    Returns a subgraph for visualization. 
    If 'name' is provided, searches for related nodes.
    Otherwise, returns a random sample.
    """
    if not chatbot:
         raise HTTPException(status_code=503, detail="ChatBot service unavailable")

    try:
        graph = chatbot.searcher.g
        
        if name:
            # Context-aware search: Find nodes matching the name and their neighbors
            query = f"""
            MATCH (n)-[r]-(m)
            WHERE n.name CONTAINS '{name}' OR m.name CONTAINS '{name}'
            RETURN n, r, m
            LIMIT 30
            """
        else:
            # Random sample: Use rand() to get diverse nodes
            query = """
            MATCH (n)-[r]->(m)
            WITH n, r, m, rand() AS random
            ORDER BY random
            LIMIT 30
            RETURN n, r, m
            """
            
        data = graph.run(query).data()
        
        nodes = {}
        links = []
        
        for record in data:
            n = record['n']
            m = record['m']
            r = record['r']
            
            n_id = str(n.identity)
            m_id = str(m.identity)
            
            # Use 'name' if available, otherwise fallback
            n_label = n.get('name', 'Unknown')
            m_label = m.get('name', 'Unknown')
            
            # Simple grouping by label
            n_group = list(n.labels)[0] if n.labels else 'Unknown'
            m_group = list(m.labels)[0] if m.labels else 'Unknown'
            
            if n_id not in nodes:
                nodes[n_id] = GraphNode(id=n_id, label=n_label, group=n_group)
            
            if m_id not in nodes:
                nodes[m_id] = GraphNode(id=m_id, label=m_label, group=m_group)
                
            links.append(GraphLink(source=n_id, target=m_id, label=type(r).__name__))
            
        return GraphData(nodes=list(nodes.values()), links=links)
        
    except Exception as e:
        print(f"Error fetching graph data: {e}")
        # Fallback to empty graph if DB fails
        return GraphData(nodes=[], links=[])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
