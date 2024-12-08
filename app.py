import streamlit as st
from rag_app import AdvancedRAGPipeline
import os
import base64

# Initialize RAG Pipeline
rag_pipeline = AdvancedRAGPipeline(csv_path='new.csv')

def download_query_log():
    """
    Download query log file
    """
    log_path = 'logs/query_log.csv'
    
    # Check if log file exists
    if os.path.exists(log_path):
        with open(log_path, 'rb') as file:
            b64 = base64.b64encode(file.read()).decode()
        href = f'<a href="data:text/csv;base64,{b64}" download="query_log.csv">Download Query Log</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
    else:
        st.sidebar.write("No query log found.")

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
    
    # Enhanced Sidebar
    st.sidebar.header("📊 App Features")
    st.sidebar.write("""
    🔍 Intelligent Sales Query Assistant
    - Ask questions about your sales data
    - Get instant, data-driven insights
    - Track and download your query history
    """)
    
    # Add some visual separator
    st.sidebar.markdown("---")
    
    # Query Log Section
    st.sidebar.header("📜 Query History")
    st.sidebar.write("Track and analyze your previous queries")
    
    # Download Query Log Button
    download_query_log_button = st.sidebar.button("🔽 Download Query Log")
    if download_query_log_button:
        download_query_log()
 
    # st.sidebar.markdown("---")
    # st.sidebar.header("💡 Quick Tips")  # Add some fun stats or tips
    # st.sidebar.write("""
    # - Try asking about total sales
    # - Explore sales by product line
    # - Discover top customers
    # """)

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

if __name__ == "__main__":
    main()