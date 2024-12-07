import os
import json
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

class AdvancedRAGPipeline:
    def __init__(self, 
                 data_path: str = 'sales_data_sample.csv',
                 metrics_path: str = 'sales_metrics.json'):
        """
        Advanced RAG Pipeline with enhanced capabilities
        
        Args:
            data_path (str): Path to sales data CSV
            metrics_path (str): Path to metrics JSON
        """
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load API keys
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ API Key is missing!")
        
        # Initialize Groq client
        self.groq_client = Groq(api_key=self.groq_api_key)
        
        # Load and preprocess data
        self.raw_data = pd.read_csv(data_path, encoding='Windows-1252')
        self.preprocess_data()
        
        # Embedding and retrieval setup
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.prepare_knowledge_base()
        
        # Query logging
        self.query_log_path = 'query_log.txt'
    
    def preprocess_data(self):
        """
        Advanced data preprocessing with more sophisticated cleaning
        """
        # Date parsing
        self.raw_data['ORDERDATE'] = pd.to_datetime(self.raw_data['ORDERDATE'])
        
        # Advanced feature engineering
        self.raw_data['TOTAL_SALES'] = self.raw_data['QUANTITYORDERED'] * self.raw_data['PRICEEACH']
        
        # Complex aggregations
        self.metrics = {
            'yearly_sales': self.raw_data.groupby(self.raw_data['ORDERDATE'].dt.year)['TOTAL_SALES'].sum().to_dict(),
            'monthly_sales': self.raw_data.groupby([
                self.raw_data['ORDERDATE'].dt.year, 
                self.raw_data['ORDERDATE'].dt.month
            ])['TOTAL_SALES'].sum().to_dict(),
            'top_customers': self.raw_data.groupby('CUSTOMERNAME')['TOTAL_SALES'].sum().nlargest(10).to_dict(),
            'product_line_performance': self.raw_data.groupby('PRODUCTLINE')['TOTAL_SALES'].sum().to_dict(),
            'geographical_insights': {
                'sales_by_country': self.raw_data.groupby('COUNTRY')['TOTAL_SALES'].sum().to_dict(),
                'orders_by_country': self.raw_data.groupby('COUNTRY')['ORDERNUMBER'].count().to_dict()
            }
        }
    
    def prepare_knowledge_base(self):
        """
        Create semantic search index with enhanced context
        """
        # Create context-rich text representations
        context_texts = [
            f"In {year}, total sales were ${sales:,.2f}" for year, sales in self.metrics['yearly_sales'].items()
        ] + [
            f"Top performing product line: {line} with ${sales:,.2f} in sales" 
            for line, sales in self.metrics['product_line_performance'].items()
        ] + [
            f"Top customer {name} generated ${sales:,.2f} in total sales" 
            for name, sales in self.metrics['top_customers'].items()
        ] + [
            f"Sales in {country}: ${sales:,.2f}" 
            for country, sales in self.metrics['geographical_insights']['sales_by_country'].items()
        ]
        
        # Generate embeddings
        self.embeddings = self.embedding_model.encode(context_texts)
        
        # FAISS index for semantic retrieval
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)
        self.context_texts = context_texts
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[str]:
        """
        Semantic context retrieval
        """
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.context_texts[i] for i in indices[0]]
    
    def generate_response(self, query: str, context: List[str]) -> str:
        """
        Generate response using Groq API with retrieved context
        """
        system_prompt = """
        You are an expert sales data analyst. Provide clear, concise, and accurate 
        responses based on the given context. If the query cannot be directly answered 
        from the context, explain that additional information is needed.
        """
        
        context_str = "\n".join(context)
        
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context:\n{context_str}\n\nQuery: {query}"}
                ],
                model="llama3-70b-8192"
            )
            
            response = chat_completion.choices[0].message.content
            return response
        
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "I'm unable to process this query at the moment."
    
    def log_query(self, query: str, response: str):
        """
        Log user queries and responses
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | Query: {query}\nResponse: {response}\n{'='*50}\n"
        
        with open(self.query_log_path, 'a') as log_file:
            log_file.write(log_entry)
    
    def answer_query(self, query: str) -> str:
        """
        Comprehensive query answering method
        """
        # Retrieve relevant context
        context = self.retrieve_context(query)
        
        # Generate response
        response = self.generate_response(query, context)
        
        # Log the interaction
        self.log_query(query, response)
        
        return response
    
    def get_query_log(self) -> str:
        """
        Retrieve the entire query log
        """
        try:
            with open(self.query_log_path, 'r') as log_file:
                return log_file.read()
        except FileNotFoundError:
            return "No query logs found."

# Example usage
if __name__ == "__main__":
    rag_pipeline = AdvancedRAGPipeline()
    
    # Test queries
    test_queries = [
        "What were the total sales in 2003?",
        "Which product line performed best?",
        "Top customers in sales"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        print(f"Response: {rag_pipeline.answer_query(query)}\n")