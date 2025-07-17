# Marketing Ad Insights Agent

## Overview
This project is a lightweight AI agent that reviews Meta/Google ad performance CSVs and outputs insights and creative improvement suggestions. It is served using a FastAPI backend and features a modern Streamlit UI.

## User Experience

The app provides a clean, intuitive interface for marketers and analysts:

- **Upload your ad performance CSV** using a drag-and-drop or file browser.
- **Preview your uploaded data** instantly in a table, so you can verify your file before analysis.
- **Automated insights generation**: The system processes your file and generates actionable insights and creative suggestions using a local LLM (Vicuna via Ollama).
- **Visual feedback**: Progress and success messages keep you informed at every step.
- **Modern, user-friendly design**: The interface is clean, responsive, and easy to use, as shown below:

### 1. Upload & Preview Workflow
![Upload and Preview Screenshot](insights_upload.png)
*Users upload their CSV and instantly preview the data before analysis.*

### 2. Insights & Feedback Workflow
![Insights and Feedback Screenshot](insights_feedback.png)
*View actionable insights, download results, and provide feedback directly in the app.*

### 3. Automated Evaluation Workflow
![Automated Evaluation Screenshot](automated_evaluation.png)
*Benchmark your agent’s performance with F1 and ROUGE scores using the built-in evaluation tool.*

## How It Works

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

5. **Test the `/run-agent` endpoint:**
   - Use the Streamlit UI or a tool like Postman/curl to POST a CSV file to `http://localhost:8000/run-agent`.

## Features
- FastAPI backend for robust, asynchronous processing
- Streamlit UI for seamless user experience
- Local LLM (Vicuna via Ollama) for privacy and cost efficiency
- RAG (ChromaDB) for grounding insights in historical data
- Knowledge graph for context-aware best practices
- Automated evaluation (F1, ROUGE) and feedback loop

## Next Steps
- Integrate more advanced knowledge graphs
- Add multi-modal data support
- Expand to support more ad platforms and data formats

---

*Built with ❤️ by your AI Marketing Assistant. Powered by FastAPI, Streamlit, and Vicuna LLM.* 
