import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from graph import graph
from pydantic import BaseModel
from agent import *
from template import html
import asyncio
from load_docs import *
from split_docs import *
from store_docs import *

app = FastAPI()


class TopicInput(BaseModel):
    topic: str


class ChatInput(BaseModel):
    topic: str
    messages: list[str]
    thread_id: str


topic_docs_cache: dict[str, list] = {}  # stores split Document chunks per topic
topic_doc_ids_cache: dict[str, list] = {}  # stores Chroma document IDs per topic


@app.post("/ingest_topic")
async def ingest_topic(input: TopicInput):
    topic = input.topic.lower().strip()
    if topic in topic_docs_cache:
        return {"message": f"Topic '{topic}' already ingested.", "num_docs": len(topic_docs_cache[topic])}

    # Step 1: Fetch PubMed docs
    docs = load_docs(topic)

    # Step 2: Split into chunks
    all_splits = split_docs(docs)

    # Step 3: Add to vector store
    all_document_ids = store_docs(all_splits)

    # Step 4: Cache in memory
    topic_docs_cache[topic] = all_splits
    topic_doc_ids_cache[topic] = all_document_ids

    return {"message": f"Topic '{topic}' ingested.", "num_docs": len(all_splits)}


@app.post("/chat")
async def chat(input: ChatInput):
    topic = input.topic.lower().strip()

    if topic not in topic_docs_cache:
        return {"error": f"Topic '{topic}' has not been ingested yet. Call /ingest_topic first."}

    config = {"configurable": {"thread_id": input.thread_id}}
    response = await agent_executor.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content


# Streaming
# Serve the HTML chat interface
@app.get("/")
async def get():
    return HTMLResponse(html)


#
#
# # WebSocket endpoint for real-time streaming
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = agent_executor.ainvoke({"messages": [data]}, config=config, stream_mode="messages")
        await websocket.send_text(result["messages"][-1].content)
