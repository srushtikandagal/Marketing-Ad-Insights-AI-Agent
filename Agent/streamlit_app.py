import streamlit as st
import requests
import pandas as pd
from io import StringIO
import subprocess
import io
import re

st.set_page_config(page_title="Ad Insights AI Agent", page_icon="🤖", layout="centered")
st.title("📊 Marketing Ad Insights AI Agent")
st.markdown("""
Upload your Meta/Google ad performance CSV and get actionable insights and creative suggestions powered by a local LLM (Vicuna via Ollama). This tool helps marketers quickly understand campaign performance and discover ways to improve future ads.
""")

with st.expander("How does it work?", expanded=False):
    st.markdown("""
    1. Upload your ad performance CSV file.
    2. The agent analyzes your data and summarizes key metrics.
    3. An AI model (Vicuna) generates actionable insights and creative suggestions.
    4. Results are displayed below for easy review and export.
    """)

st.markdown("---")

uploaded_file = st.file_uploader("Upload your ad performance CSV", type=["csv"])

if uploaded_file is not None:
    st.info("Processing your file and generating insights... This may take a moment.")
    # Display the uploaded CSV preview
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head(10), use_container_width=True)

    # Send file to FastAPI backend
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
    try:
        response = requests.post("http://localhost:8000/run-agent", files=files, timeout=120)
        if response.status_code == 200:
            result = response.json()
            st.success("Insights generated!")

            st.subheader("Key Metrics Summary")
            st.json(result["summary"])

            st.subheader("AI-Generated Insights & Suggestions")
            insights_html = result['insights'].replace('\n', '<br>')
            st.markdown(f"""
            <div style='background-color:#f0f2f6;padding:1.2em;border-radius:10px;'>
            <b>{insights_html}</b>
            </div>
            """, unsafe_allow_html=True)

            if result.get("kg_tip"):
                st.info(f"Knowledge Graph Tip: {result['kg_tip']}")

            with st.expander("Show all columns and row count"):
                st.write(f"Columns: {result['columns']}")
                st.write(f"Number of rows: {result['num_rows']}")

            st.markdown("---")
            st.download_button(
                label="Download Insights as Text",
                data=result['insights'],
                file_name="ad_insights.txt",
                mime="text/plain"
            )

            # Feedback loop
            st.markdown("---")
            st.subheader("How helpful were these insights?")
            feedback_col1, feedback_col2 = st.columns([1, 3])
            with feedback_col1:
                rating = st.radio("Rating:", [1, 2, 3, 4, 5], index=4, horizontal=True, key="rating")
            with feedback_col2:
                comment = st.text_input("Additional comments (optional):", key="comment")
            if st.button("Submit Feedback"):
                import datetime
                import csv
                feedback_data = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "rating": rating,
                    "comment": comment,
                    "insights": result['insights'],
                    "summary": str(result['summary'])
                }
                # Append feedback to a local CSV file
                feedback_file = "feedback_log.csv"
                file_exists = False
                try:
                    with open(feedback_file, "r") as f:
                        file_exists = True
                except FileNotFoundError:
                    file_exists = False
                with open(feedback_file, "a", newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=feedback_data.keys())
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(feedback_data)
                st.success("Thank you for your feedback!")
        else:
            st.error(f"Error from backend: {response.text}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
else:
    st.info("Please upload a CSV file to get started.")

st.markdown("---")
st.header("🔍 Automated Evaluation: Benchmark Your Agent's Performance")

# State to persist uploaded file and results
if 'eval_file_uploaded' not in st.session_state:
    st.session_state['eval_file_uploaded'] = None
if 'eval_results' not in st.session_state:
    st.session_state['eval_results'] = None

with st.expander("Evaluate Agent Outputs vs. Gold Standard", expanded=False):
    st.markdown("""
    <div style='font-size:1.1em;'>
    <b>Why Evaluate?</b><br>
    Quantitative evaluation helps you track your AI agent's progress and ensures your insights are not just creative, but also accurate and reliable.<br><br>
    <b>How to Use:</b>
    <ol>
      <li>Download the <b>sample evaluation CSV</b> or prepare your own with two columns: <code>output</code> (agent's output) and <code>reference</code> (expected answer).</li>
      <li>Upload your evaluation CSV below (only once).</li>
      <li>Click <b>Run Evaluation</b> to compute F1 and ROUGE scores. You can re-run as needed without re-uploading.</li>
      <li>Review the results summary to identify strengths and areas for improvement.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    # Provide a sample CSV for download (use BytesIO for binary data)
    sample_csv = "output,reference\nIncrease ad spend for high CTR campaigns,Consider increasing budget for top CTR ads\nUse carousel ads for e-commerce,Carousel ads work well for e-commerce\n"
    sample_bytes = io.BytesIO(sample_csv.encode("utf-8"))
    st.download_button("Download Sample Evaluation CSV", sample_bytes, file_name="outputs_vs_refs_sample.csv", mime="text/csv")

    eval_file = st.file_uploader("Upload your evaluation CSV", type=["csv"], key="eval")
    if eval_file is not None:
        eval_path = "outputs_vs_refs.csv"
        with open(eval_path, "wb") as f:
            f.write(eval_file.getbuffer())
        st.session_state['eval_file_uploaded'] = eval_path
        st.session_state['eval_results'] = None  # Reset results on new upload
        st.success("Evaluation file uploaded! Now you can run evaluation as many times as you like.")

    if st.session_state['eval_file_uploaded']:
        if st.button("Run Evaluation"):
            with st.spinner("Running evaluation and benchmarking your agent (may take up to 3 minutes for large files)..."):
                try:
                    result = subprocess.run([
                        "python", "evaluate_outputs.py"
                    ], capture_output=True, text=True, timeout=180)
                    if result.returncode == 0:
                        output = result.stdout
                        match = re.search(r"ROUGE-1: ([0-9.]+), ROUGE-L: ([0-9.]+), F1: ([0-9.]+)", output)
                        if match:
                            rouge1, rougel, f1 = match.groups()
                            st.session_state['eval_results'] = (rouge1, rougel, f1)
                        else:
                            st.session_state['eval_results'] = output
                        st.success("Evaluation complete! Here are your results:")
                    else:
                        st.error(f"Error running evaluation: {result.stderr}")
                except Exception as e:
                    st.error(f"Failed to run evaluation: {e}")
        # Show results if available
        if st.session_state['eval_results']:
            if isinstance(st.session_state['eval_results'], tuple):
                rouge1, rougel, f1 = st.session_state['eval_results']
                col1, col2, col3 = st.columns(3)
                col1.metric("ROUGE-1", f"{float(rouge1)*100:.1f}%")
                col2.metric("ROUGE-L", f"{float(rougel)*100:.1f}%")
                col3.metric("F1 Score", f"{float(f1)*100:.1f}%")
            else:
                st.code(st.session_state['eval_results'])

st.markdown("---")
st.caption("Built with ❤️ by your AI Marketing Assistant. Powered by FastAPI, Streamlit, and Vicuna LLM.") 