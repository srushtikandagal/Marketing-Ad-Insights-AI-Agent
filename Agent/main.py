from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import io
import os
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import chromadb
from chromadb.utils import embedding_functions
import hashlib

app = FastAPI()

# Initialize ChromaDB client and collection
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("ad_insights")

# Use a simple embedding function (e.g., from LangChain or ChromaDB's default)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Helper to summarize ad metrics
def summarize_ad_metrics(df):
    summary = {}
    for col in df.columns:
        if df[col].dtype in ["float64", "int64"]:
            summary[col] = {
                "mean": float(df[col].mean()),
                "min": float(df[col].min()),
                "max": float(df[col].max())
            }
    return summary

# Helper to hash summary for unique key
def hash_summary(summary):
    return hashlib.sha256(str(summary).encode()).hexdigest()

# Simple knowledge graph: platform and creative type best practices
KNOWLEDGE_GRAPH = {
    "Facebook": {
        "carousel": "Carousel ads on Facebook often have higher engagement for e-commerce and storytelling.",
        "video": "Video ads on Facebook perform best when under 15 seconds and with captions.",
        "image": "High-contrast images with minimal text work well on Facebook."
    },
    "Instagram": {
        "story": "Instagram Stories with interactive elements (polls, stickers) boost engagement.",
        "reel": "Short, vertical videos with trending music perform well as Reels.",
        "image": "Bright, visually striking images are most effective on Instagram feeds."
    },
    "Google": {
        "search": "Use clear, keyword-rich headlines and strong CTAs in Google Search ads.",
        "display": "Responsive display ads with multiple asset variations improve reach.",
        "video": "YouTube ads should capture attention in the first 5 seconds."
    }
}

def extract_platform_and_type(df):
    # Try to extract platform and ad type from columns if present
    platform = None
    ad_type = None
    for col in df.columns:
        if col.lower() == "platform":
            platform = df[col].mode()[0]  # Most common platform
        if col.lower() in ["ad type", "creative type"]:
            ad_type = df[col].mode()[0]
    return platform, ad_type

@app.post("/run-agent")
async def run_agent(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    summary = summarize_ad_metrics(df)
    summary_str = str(summary)
    summary_hash = hash_summary(summary_str)

    # Knowledge graph: get best practice tip if possible
    platform, ad_type = extract_platform_and_type(df)
    kg_tip = ""
    if platform and ad_type:
        tip = KNOWLEDGE_GRAPH.get(platform, {}).get(ad_type.lower())
        if tip:
            kg_tip = f"\n\nBest practice for {platform} {ad_type} ads: {tip}"

    # RAG: Check for similar summaries in ChromaDB
    similar_insights = []
    try:
        query_embedding = embedding_fn(summary_str)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        if results and results['documents'] and results['distances'][0][0] < 0.2:
            similar_insights = results['documents'][0]
    except Exception as e:
        similar_insights = []

    # Prepare prompt for LLM, including RAG and KG context
    prompt_context = ""
    if similar_insights:
        prompt_context += f"Past similar campaign insights: {similar_insights[0]}\n\n"
    if kg_tip:
        prompt_context += kg_tip + "\n\n"
    prompt = PromptTemplate(
        input_variables=["context", "summary"],
        template="""
{context}You are a marketing analytics expert. Given the following ad performance summary:
{summary}

1. Provide 2-3 actionable insights about the ad performance.
2. Suggest 2 creative improvements for future campaigns.
3. If you see any underperforming metrics, mention them and suggest how to improve.
Respond in clear bullet points.
"""
    )
    llm = Ollama(model="vicuna")
    prompt_str = prompt.format(context=prompt_context, summary=summary)
    insights = llm(prompt_str)

    # Store the new summary and insights in ChromaDB for future RAG
    try:
        collection.add(
            documents=[insights],
            embeddings=[embedding_fn(summary_str)],
            ids=[summary_hash]
        )
    except Exception as e:
        pass

    return JSONResponse({
        "columns": df.columns.tolist(),
        "num_rows": len(df),
        "summary": summary,
        "insights": insights,
        "rag": bool(similar_insights),
        "kg_tip": kg_tip
    }) 