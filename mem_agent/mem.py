from dotenv import load_dotenv
load_dotenv()
from mem0 import Memory
import os
import json

from openai import OpenAI



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEO_URI = os.getenv("NEO_URI")
NEO_USERNAME = os.getenv("NEO_USERNAME")
NEO_PASSWORD = os.getenv("NEO_PASSWORD")


client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": "models/gemini-embedding-001",
            "embedding_dims": 768
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": "gemini-2.5-flash",
            "temperature": 0.2,
            "max_tokens": 2000
        }
    },
    "graph_store":{
        "provider":"neo4j",
        "config": {"uri": NEO_URI, "username": NEO_USERNAME, "password": NEO_PASSWORD}  
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "piyush_memories",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768
        }
    },
}



mem_client = Memory.from_config(config)

while True:

    user_query = input("User query: ")

    search_memory = mem_client.search(
        query=user_query,
        filters={
            "user_id": "piyush"
        }
    )
    
    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
    ]
    
    print("Found memories:", memories)
    
    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """
    
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    assistant_response = response.choices[0].message.content

    print("Assistant response:", assistant_response)

    mem_client.add(
        user_id = "piyush",
        messages = [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": assistant_response}
        ]
    )

    print("Conversation added to memory.")