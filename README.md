# Marketing Ad Insights AI Agent

## Overview
This project is a lightweight AI agent that reviews Meta/Google ad performance CSVs and outputs actionable insights and creative improvement suggestions. It is built with a FastAPI backend, a modern Streamlit UI, and leverages local LLMs (Vicuna via Ollama), RAG (ChromaDB), and a knowledge graph for context-aware recommendations.

---

## Architecture
- **FastAPI**: Backend API for file upload, data processing, and agent orchestration.
- **Streamlit**: User interface for uploading CSVs, viewing insights, submitting feedback, and running automated evaluation.
- **Pandas**: For CSV parsing and summarization of ad metrics.
- **Vicuna LLM (via Ollama)**: Local large language model for generating insights and suggestions.
- **LangChain**: For prompt management and LLM orchestration.
- **ChromaDB**: Vector database for Retrieval Augmented Generation (RAG), grounding insights in historical data.
- **Knowledge Graph**: Python dictionary mapping ad platforms and creative types to best practices.
- **Automated Evaluation**: Script for F1 and ROUGE scoring of agent outputs.

---

## User Experience & Workflow

1. **Upload your ad performance CSV** using the drag-and-drop or file browser.
2. **Preview your uploaded data** instantly in a table.
3. **Automated insights generation**: The system processes your file and generates actionable insights and creative suggestions.
4. **Visual feedback**: Progress and success messages keep you informed at every step.
5. **Automated Evaluation**: Upload a CSV of agent outputs and references to benchmark your agent’s performance with F1 and ROUGE scores.

### Main Interface Screenshot

*Upload your CSV and access automated evaluation in one place.*

<img width="1833" height="899" alt="image" src="https://github.com/user-attachments/assets/6f67a1ba-e782-432f-a337-2a15a3f1a998" />


## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the Vicuna model with Ollama:**
   ```bash
   ollama run vicuna
   ```
3. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
4. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Features
- FastAPI backend for robust, asynchronous processing
- Streamlit UI for seamless user experience
- Local LLM (Vicuna via Ollama) for privacy and cost efficiency
- RAG (ChromaDB) for grounding insights in historical data
- Knowledge graph for context-aware best practices
- Automated evaluation (F1, ROUGE) and feedback loop

---

## Evaluation Strategy
- **User feedback loop**: Users rate insights and leave comments; feedback is logged for continuous improvement.
- **Automated metrics**: F1 and ROUGE scores are computed by comparing agent outputs to reference answers.
- **Manual and automated testing**: Both user feedback and objective metrics are used to evaluate performance.

---

## Pattern Recognition & Improvement Loop
- **Feedback-driven refinement**: User feedback is logged and can be used to refine prompts and improve the agent.
- **Memory module**: ChromaDB stores past insights for retrieval and grounding.
- **Prompt refinement**: Prompts can be updated based on feedback and observed errors.

---

## Potential Improvements
- Integrate advanced knowledge graphs (e.g., Neo4j)
- Add multi-modal data support (images, videos)
- Expand to more ad platforms and data formats
- Containerize for cloud deployment and multi-user access

---

*Built with ❤️ by your AI Marketing Assistant. Powered by FastAPI, Streamlit, and Vicuna LLM.*


