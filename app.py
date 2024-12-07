import streamlit as st
from rag_app import AdvancedRAGPipeline
import os
import base64

# Initialize RAG Pipeline
rag_pipeline = AdvancedRAGPipeline()

def download_query_log():
    """
    Download query log file
    """
    query_log = rag_pipeline.get_query_log()
    b64 = base64.b64encode(query_log.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="query_log.txt">Download Query Log</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Sales Data Intelligence",
        page_icon="📊",
        layout="wide"
    )
    
    # Custom CSS for enhanced UI
    st.markdown("""
    <style>
    .reportview-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stTextInput > div > div > input {
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton > button {
        background-color: #2ecc71;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #27ae60;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.title("🚀 Sales Data Intelligence")
    st.write("Ask intelligent questions about your sales data!")
    
    # Sidebar for additional controls
    st.sidebar.header("Query Options")
    sample_queries = [
        "What were the total sales in 2003?",
        "Top performing product lines",
        "Sales by country",
        "Top 5 customers"
    ]
    selected_query = st.sidebar.selectbox("Sample Queries", sample_queries)
    
    # Main chat interface
    query = st.text_input("Enter your sales data query:", 
                           value=selected_query if selected_query else "")
    
    if st.button("Ask Query"):
        if query:
            with st.spinner('Generating response...'):
                # Generate response
                response = rag_pipeline.answer_query(query)
                
                # Display response
                st.success("Response:")
                st.write(response)
    
    # Query log section
    st.sidebar.header("Query Log")
    if st.sidebar.button("View Query Log"):
        log_content = rag_pipeline.get_query_log()
        st.sidebar.text_area("Query Interactions", log_content, height=300)
    
    if st.sidebar.button("Download Query Log"):
        download_query_log()

if __name__ == "__main__":
    main()