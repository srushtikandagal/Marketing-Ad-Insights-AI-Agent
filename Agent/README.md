# Marketing Ad Insights Agent

## Overview
This project is a lightweight AI agent that reviews Meta/Google ad performance CSVs and outputs insights and creative improvement suggestions. It is served using a FastAPI backend.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

3. Test the `/run-agent` endpoint:
   - Use a tool like [Postman](https://www.postman.com/) or `curl` to POST a CSV file to `http://localhost:8000/run-agent`.
   - Example `curl` command:
     ```bash
     curl -X POST "http://localhost:8000/run-agent" -F "file=@your_ads.csv"
     ```

## Next Steps
- Integrate LLM for insights and suggestions
- Add RAG/Knowledge Graph features
- Implement evaluation and feedback loop 