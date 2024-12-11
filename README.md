# 🚀 RAG-Sales-Bot: Revolutionizing Sales Data Analysis with RAG and Streamlit
RAG-Sales-Bot is an advanced Retrieval-Augmented Generation (RAG) system designed to process and analyze sales data effortlessly. With the integration of Streamlit, FAISS for vector similarity search, and Groq API for complex queries, this bot offers unparalleled efficiency for answering business-critical questions.

🌟 Features
Preloaded Sales Insights: Analyze data across dimensions like customers, products, countries, and time.
Semantic Search with FAISS: Retrieve the most relevant results from the database for natural language queries.
Dynamic Query Handling: Automatically matches user queries to preloaded insights or processes them using the Groq API for custom results.
Streamlit Web Interface: A user-friendly dashboard to interact with the bot seamlessly.
Downloadable Query Logs: Keep track of all your queries and responses with downloadable logs.
🛠️ Methodology
Data Preprocessing:

The bot reads sales data from a CSV file.
Cleans and preprocesses the data (e.g., ensuring correct data types for dates and numeric fields).
Indexes the processed data into FAISS, enabling fast and accurate semantic search.
Query Matching:

Matches user queries to predefined patterns (e.g., "top customer," "sales by product line") for instant responses.
For custom or complex queries, routes the query to the Groq API.
FAISS Integration:

Embeds data into vector representations using a transformer-based model.
Uses FAISS to find the closest matches for user queries, ensuring relevant and context-aware results.
Dynamic Web Interface:

Powered by Streamlit, the bot provides an interactive UI for real-time query handling and data visualization.
Logs and Monitoring:

Every query and its response are logged.
Users can download query logs for future reference.
