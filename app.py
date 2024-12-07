import streamlit as st
from rag_app import AdvancedRAGPipeline  # Assuming AdvancedRAGPipeline is in `rag_app.py`
import os
import base64
from io import StringIO


# Initialize RAG Pipeline
rag_pipeline = AdvancedRAGPipeline(csv_path='new.csv')

def download_query_log():
    """
    Download query log file
    """
    query_log = rag_pipeline.get_query_log()
    b64 = base64.b64encode(query_log.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="query_log.csv">Download Query Log</a>'
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
    
    # Sidebar with app explanation
    st.sidebar.header("What This App Does")
    st.sidebar.write("""
    1. This app allows you to ask data-driven questions about your sales data and get intelligent responses.
    2. It leverages advanced retrieval-augmented generation (RAG) techniques to process your queries and provide insights.
    """)

    # Main chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "Welcome to the Sales Data Intelligence Chat!"}]
    
    # Display previous chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Get the user's question using Streamlit's chat input
    query = st.chat_input("Enter your sales data query:")
    
    if query:
        # Append user query to chat history
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Display user input
        with st.chat_message("user"):
            st.write(query)
        
        # Generate response using RAG pipeline
        with st.chat_message("assistant"):
            botmsg = st.empty()
            with st.spinner("Generating response..."):
                response = rag_pipeline.answer_query(query)
                botmsg.write(response)
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Download Query Log Button
    st.sidebar.header("Download Query Log")
    download_query_log_button = st.sidebar.button("Download Query Log")
    if download_query_log_button:
        download_query_log()

if __name__ == "__main__":
    main()
