# 🚀 RAG-Sales-Bot: Revolutionizing Sales Data Analysis with RAG and Streamlit [Live](https://rag-sales-chatbot.streamlit.app/)
RAG-Sales-Bot is an advanced Retrieval-Augmented Generation (RAG) system designed to process and analyze sales data effortlessly. With the integration of Streamlit, FAISS for vector similarity search, and Groq API for complex queries, this bot offers unparalleled efficiency for answering business-critical questions.

### 🌟 Features
1. Preloaded Sales Insights: Analyze data across dimensions like customers, products, countries, and time.
2. Semantic Search with FAISS: Retrieve the most relevant results from the database for natural language queries.
3. Dynamic Query Handling: Automatically matches user queries to preloaded insights or processes them using the Groq API for custom results.
4. Streamlit Web Interface: A user-friendly dashboard to interact with the bot seamlessly.
5. Downloadable Query Logs: Keep track of all your queries and responses with downloadable logs.

# 🛠️ Methodology

### Data Preprocessing:

The bot reads sales data from a CSV file.
Cleans and preprocesses the data (e.g., ensuring correct data types for dates and numeric fields).
Indexes the processed data into FAISS, enabling fast and accurate semantic search.

### Query Matching:

Matches user queries to predefined patterns (e.g., "top customer," "sales by product line") for instant responses.
For custom or complex queries, routes the query to the Groq API.

### FAISS Integration:

Embeds data into vector representations using a transformer-based model.
Uses FAISS to find the closest matches for user queries, ensuring relevant and context-aware results.

### Dynamic Web Interface:

Powered by Streamlit, the bot provides an interactive UI for real-time query handling and data visualization.

### Logs and Monitoring:

Every query and its response are logged.
Users can download query logs for future reference.

# 🧠 Selected Model: llama-3.3-70b-versatile

This project uses Meta's **llama-3.3-70b-versatile**, a state-of-the-art large language model designed for versatility and scalability. Key features of this model include:

**Developer**: Meta

**Context Window**: Supports up to 128,000 tokens, making it ideal for complex, context-rich queries.

**Max Output Tokens**: Can generate outputs up to 32,768 tokens, ensuring detailed and comprehensive responses.

**Applications**: Perfect for use cases involving long document summarization, intricate reasoning, and detailed conversations.



# 🔢 Available Models

| **Model ID**                | **Developer** | **Context Window (Tokens)** | **Max Output Tokens** | **Max File Size** |
|-----------------------------|---------------|-----------------------------|-----------------------|-------------------|
| distil-whisper-large-v3-en  | HuggingFace   | -                           | -                     | 25 MB            |
| gemma2-9b-it                | Google        | 8,192                       | -                     | -                |
| gemma-7b-it                 | Google        | 8,192                       | -                     | -                |
| llama-3.3-70b-versatile     | Meta          | 128,000                     | 32,768                | -                |
| llama-3.1-70b-versatile     | Meta          | 128,000                     | 32,768                | (DEPRECATED)     |
| llama-3.1-8b-instant        | Meta          | 128,000                     | 8,192                 | -                |
| llama-guard-3-8b            | Meta          | 8,192                       | -                     | -                |
| llama3-70b-8192             | Meta          | 8,192                       | -                     | -                |
| llama3-8b-8192              | Meta          | 8,192                       | -                     | -                |
| mixtral-8x7b-32768          | Mistral       | 32,768                      | -                     | -                |
| whisper-large-v3            | OpenAI        | -                           | -                     | 25 MB            |
| whisper-large-v3-turbo      | OpenAI        | -                           | -                     | 25 MB            |

**NOTE:** This is applicabel if you are using Groq.

## 🐳 Dockerized Deployment
This project is fully containerized for hassle-free deployment. With Docker, you can run the bot anywhere with just a few commands.


# 🏃 How to Run

### Option 1: Run Using Docker

Pull the Docker Image

```
docker pull shiv37/rag-sales-bot
```

```
docker run -p 8501:8501 -e GROQ_API_KEY=your_groq_api_key -v /path/to/your/data:/app/data shiv37/rag-sales-bot
```

Replace /path/to/your/data with the path to the folder containing new.csv.
Set your_groq_api_key to your valid Groq API key.

Access the Application Open your browser and navigate to http://localhost:8501.


### Option 2: Clone the Repository and Run Locally
Clone the Repository

```
git clone https://github.com/Shiv-D-Coder/RAG-Sales-Bot.git
cd RAG-Sales-Bot
```
Install Dependencies Make sure you have Python installed. Create a virtual environment (optional) and install the required dependencies:

```
pip install -r requirements.txt
```
Configure API Key

a. Use a .streamlit/secrets.toml file. Create a .streamlit/secrets.toml file in the root directory with the following content:
```
GROQ_API_KEY = "your_groq_api_key"
```

b. Use an .env file. Create an .env file in the root directory with the following content:
```
GROQ_API_KEY=your_groq_api_key
```

Run the Application Start the Streamlit app:

```
streamlit run app.py
```
Access the Application Open your browser and navigate to http://localhost:8501.

📊 Example Queries
Here are some example questions you can ask RAG-Sales-Bot:

1. "Who is the top customer in terms of sales?"
2. "Show me the sales by product line."
3. "What is the total number of orders placed in 2023?"
"4. What is the distribution of order statuses?"

## 🤝 Contributing
We welcome contributions to improve this project. Feel free to fork the repository, create issues, or submit pull requests. Let's make RAG-Sales-Bot even better together!

## 💡 Future Plans
Add support for multilingual queries.
Integrate additional vector databases for enhanced performance.
Include dynamic visualizations for insights like time-series trends and geographical sales distribution.

Ready to transform your sales data into actionable insights? Get started with RAG-Sales-Bot today! 🚀
