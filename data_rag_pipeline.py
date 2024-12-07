import os
import json
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

class AdvancedRAGPipeline:
    def __init__(self, 
                 data_path: str = 'sales_data_sample.csv'):
        """
        Advanced RAG Pipeline with comprehensive dataset analysis
        
        Args:
            data_path (str): Path to sales data CSV
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
        self.raw_data = pd.read_csv(data_path)
        
        # Preprocess and generate comprehensive insights
        self.preprocess_data()
        
        # Query logging
        self.query_log_path = 'query_log.txt'
    
    def preprocess_data(self):
        """
        Advanced data preprocessing with comprehensive feature engineering
        """
        # Date parsing and feature engineering
        self.raw_data['ORDERDATE'] = pd.to_datetime(self.raw_data['ORDERDATE'])
        self.raw_data['TOTAL_SALES'] = self.raw_data['QUANTITYORDERED'] * self.raw_data['PRICEEACH']
        
        # Comprehensive data insights
        self.insights = {
            'yearly_analysis': self._yearly_sales_analysis(),
            'monthly_analysis': self._monthly_sales_analysis(),
            'product_line_performance': self._product_line_performance(),
            'customer_insights': self._customer_performance(),
            'geographical_insights': self._geographical_analysis(),
            'order_status_analysis': self._order_status_analysis()
        }
    
    def _yearly_sales_analysis(self):
        """Analyze sales performance by year"""
        yearly_sales = self.raw_data.groupby(self.raw_data['ORDERDATE'].dt.year).agg({
            'TOTAL_SALES': 'sum',
            'ORDERNUMBER': 'count',
            'QUANTITYORDERED': 'sum'
        }).reset_index()
        yearly_sales.columns = ['Year', 'Total Sales', 'Total Orders', 'Total Quantity']
        return yearly_sales.to_dict('records')
    
    def _monthly_sales_analysis(self):
        """Analyze sales performance by month"""
        monthly_sales = self.raw_data.groupby([
            self.raw_data['ORDERDATE'].dt.year, 
            self.raw_data['ORDERDATE'].dt.month
        ]).agg({
            'TOTAL_SALES': 'sum',
            'ORDERNUMBER': 'count',
            'QUANTITYORDERED': 'sum'
        }).reset_index()
        monthly_sales.columns = ['Year', 'Month', 'Total Sales', 'Total Orders', 'Total Quantity']
        return monthly_sales.to_dict('records')
    
    def _product_line_performance(self):
        """Analyze product line performance"""
        product_line_sales = self.raw_data.groupby('PRODUCTLINE').agg({
            'TOTAL_SALES': 'sum',
            'ORDERNUMBER': 'count',
            'QUANTITYORDERED': 'sum'
        }).reset_index()
        product_line_sales.columns = ['Product Line', 'Total Sales', 'Total Orders', 'Total Quantity']
        return product_line_sales.to_dict('records')
    
    def _customer_performance(self):
        """Analyze top customer performance"""
        customer_sales = self.raw_data.groupby('CUSTOMERNAME').agg({
            'TOTAL_SALES': 'sum',
            'ORDERNUMBER': 'count',
            'QUANTITYORDERED': 'sum'
        }).nlargest(10, 'TOTAL_SALES').reset_index()
        customer_sales.columns = ['Customer Name', 'Total Sales', 'Total Orders', 'Total Quantity']
        return customer_sales.to_dict('records')
    
    def _geographical_analysis(self):
        """Analyze geographical sales performance"""
        geo_sales = self.raw_data.groupby('COUNTRY').agg({
            'TOTAL_SALES': 'sum',
            'ORDERNUMBER': 'count',
            'CUSTOMERNAME': 'nunique'
        }).reset_index()
        geo_sales.columns = ['Country', 'Total Sales', 'Total Orders', 'Unique Customers']
        return geo_sales.to_dict('records')
    
    def _order_status_analysis(self):
        """Analyze order status distribution"""
        status_analysis = self.raw_data.groupby('STATUS').agg({
            'ORDERNUMBER': 'count',
            'TOTAL_SALES': 'sum'
        }).reset_index()
        status_analysis.columns = ['Status', 'Total Orders', 'Total Sales']
        return status_analysis.to_dict('records')
    
    def generate_prompt(self, query: str) -> str:
        """
        Generate a comprehensive prompt with dataset insights
        
        Args:
            query (str): User's input query
        
        Returns:
            str: Comprehensive prompt with context
        """
        # Create a comprehensive context string from insights
        context = "Dataset Insights:\n"
        
        # Add insights from different perspectives
        for key, insights in self.insights.items():
            context += f"\n{key.replace('_', ' ').title()}:\n"
            for insight in insights[:3]:  # Limit to top 3 for each category
                context += f"- {json.dumps(insight)}\n"
        
        # Construct final prompt
        prompt = f"""
        You are an expert sales data analyst. Analyze the following query in the context of the provided dataset insights.

        Dataset Context:
        {context}

        Query: {query}

        Provide a detailed, data-driven response. If the exact answer is not possible, explain why and suggest how the question might be refined.
        """
        
        return prompt
    
    def answer_query(self, query: str) -> str:
        """
        Generate a comprehensive response using the entire dataset
        
        Args:
            query (str): User's input query
        
        Returns:
            str: Detailed response
        """
        # Generate prompt with comprehensive context
        prompt = self.generate_prompt(query)
        
        try:
            # Generate response using Groq API
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful sales data analyst."},
                    {"role": "user", "content": prompt}
                ],
                model="whisper-large-v3",
                max_tokens=800
            )
            
            response = chat_completion.choices[0].message.content
            
            # Log the query and response
            self.log_query(query, response)
            
            return response
        
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def log_query(self, query: str, response: str):
        """
        Log user queries and responses
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | Query: {query}\nResponse: {response}\n{'='*50}\n"
        
        with open(self.query_log_path, 'a') as log_file:
            log_file.write(log_entry)
    
    def get_query_log(self) -> str:
        """
        Retrieve the entire query log
        """
        try:
            with open(self.query_log_path, 'r') as log_file:
                return log_file.read()
        except FileNotFoundError:
            return "No query logs found."

# Example usage for testing
if __name__ == "__main__":
    rag_pipeline = AdvancedRAGPipeline()
    
    # Test queries
    test_queries = [
        "What were the total sales in 2003?",
        "Which product line performed best?",
        "Top customers in sales",
        "Sales performance by country"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        print(f"Response: {rag_pipeline.answer_query(query)}\n")