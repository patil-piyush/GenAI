from fastapi import Body, FastAPI
from ollama import Client



app = FastAPI()



client = Client(
    host="http://localhost:11434",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chat")
def chat(
    message: str = Body(..., description="The message")
):
    response = client.chat(model="qwen2.5:3b", messages=[
        {"role": "user", "content": message},
    ])
    
    return {"response": response.message.content}