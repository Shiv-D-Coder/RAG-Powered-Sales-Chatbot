import streamlit as st
from rag_app import AdvancedRAGPipeline
import os
import base64

# Initialize RAG Pipeline
rag_pipeline = AdvancedRAGPipeline(csv_path='new.csv')

def set_background(image_url):
    """
    Set a background image for the app using a URL.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            opacity: 0.7;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to download the query log using st.download_button in sidebar
def download_query_log_sidebar():
    """
    Create a download button for the query log file in the sidebar.
    """
    log_path = 'logs/query_log.csv'
    if os.path.exists(log_path):
        with open(log_path, 'rb') as file:
            b64 = base64.b64encode(file.read()).decode()
        
        st.sidebar.download_button(
            label="Download Query Log",
            data=base64.b64decode(b64),
            file_name="query_log.csv",
            mime="text/csv",
            help="Click to download your query log"
        )
    else:
        st.sidebar.write("No query log found.")

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Sales Data Intelligence",
        page_icon="📊",
        layout="wide"
    )
    
    # Set background image
    image_url = "https://img.freepik.com/free-vector/gradient-network-connection-background_23-2148879890.jpg"  # Replace with your actual image link
    # set_background(image_url)

    # Custom CSS for enhanced UI
    st.markdown("""
    <style>
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
    st.sidebar.markdown("---")

    # Query Log Section in Sidebar
    st.sidebar.header("📜 Query History")
    download_query_log_sidebar()

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
