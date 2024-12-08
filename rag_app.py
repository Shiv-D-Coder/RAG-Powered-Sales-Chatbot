import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime
import re
import streamlit as st
import io  # Added io import

# Load environment variables
load_dotenv()

class AdvancedRAGPipeline:
    def __init__(self, csv_path='new.csv'):
        # Initialize Groq client
        groq_api_key = st.secrets["GROQ"]["GROQ_API_KEY"]
        self.groq_client = Groq(api_key=groq_api_key)
        
        # Load and preprocess data
        self.df = pd.read_csv(csv_path)
        self.preprocess_data()
        
        # Initialize query log as a DataFrame
        os.makedirs('logs', exist_ok=True)
    
    def preprocess_data(self):
        # Convert date column
        self.df['ORDERDATE'] = pd.to_datetime(self.df['ORDERDATE'])
        
        # Ensure numeric columns are properly typed
        numeric_columns = ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
        for col in numeric_columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
    
    def answer_query(self, query):
        # Normalize query
        query = query.lower().strip()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Predefined query patterns
        query_patterns = [
            {'pattern': ['total orders', 'number of orders'], 'method': self.total_orders_by_year},
            {'pattern': ['top customer', 'most orders'], 'method': self.customer_with_most_orders},
            {'pattern': ['top customers', 'customers by sales'], 'method': self.top_customers_by_sales},
            {'pattern': ['product line', 'sales by product'], 'method': self.product_line_sales},
            {'pattern': ['sales by country', 'country sales'], 'method': self.sales_by_country},
            {'pattern': ['order status', 'status distribution'], 'method': self.order_status_distribution},
            {'pattern': ['orders by month', 'monthly orders'], 'method': self.orders_by_month_wrapper},
            {'pattern': ['customers by country', 'country customers'], 'method': self.customers_by_country}
        ]
        
        # Match pattern to query
        response = None
        for pattern_obj in query_patterns:
            if any(p in query for p in pattern_obj['pattern']):
                try:
                    if 'year' in query and pattern_obj['method'] == self.orders_by_month_wrapper:
                        year = self.extract_year(query)
                        response = pattern_obj['method'](year) if year else pattern_obj['method']()
                    else:
                        response = pattern_obj['method']()
                    break
                except Exception as e:
                    response = f"Error processing query: {str(e)}"
        
        # Fallback to Groq API for complex queries
        if response is None:
            response = self.generate_groq_response(query)
        
        # Log the query and response
        self.log_query(query, response)
        return self.format_result(response)
    
    def extract_year(self, query):
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', query)
        return int(year_match.group(1)) if year_match else None
    
    def generate_groq_response(self, query):
        try:
            context = f"""
            This is a sales dataset with columns:
            {', '.join(self.df.columns)}
            
            Total rows: {len(self.df)}
            Unique Product Lines: {', '.join(self.df['PRODUCTLINE'].unique())}
            Date Range: {self.df['ORDERDATE'].min()} to {self.df['ORDERDATE'].max()}
            """
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a sales data analyst and given question but do not show how you reach to that conclusion."},
                    {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.0
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def format_result(self, result):
        # Enhanced formatting for different result types
        if isinstance(result, dict):
            # Sort dictionary by values in descending order
            sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
            
            # Format as a neat, aligned string
            max_key_length = max(len(str(key)) for key in sorted_result.keys())
            formatted_lines = [
                f"{str(key).ljust(max_key_length)} : {value}" 
                for key, value in sorted_result.items()
            ]
            return "Results:\n" + "\n".join(formatted_lines)
        
        return result or "No data found."
    
    def log_query(self, query, response):
        # Add new query to log
        log_file = 'logs/query_log.csv'
        
        # Check if log file exists, if not create with headers
        if not os.path.exists(log_file):
            pd.DataFrame(columns=['timestamp', 'query', 'response']).to_csv(log_file, index=False)
        
        # Create log entry
        log_entry = pd.DataFrame([{
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'query': query,
            'response': str(response)
        }])
        
        # Append to existing log
        log_entry.to_csv(log_file, mode='a', header=False, index=False)
    
    def get_query_log(self):
        """
        Generate a downloadable CSV string for query log
        """
        # If no queries logged, return a default message
        if self.query_log.empty:
            return "timestamp,query,response\nNo queries logged yet."
        
        # Convert log to CSV string
        return self.query_log.to_csv(index=False)
    
    def download_query_log(self, filename='query_log.csv'):
        try:
            # Ensure the logs directory exists
            os.makedirs('logs', exist_ok=True)
            
            # Full path for saving
            full_path = os.path.join('logs', filename)
            
            # Save query log
            self.query_log.to_csv(full_path, index=False)
            return f"Query log successfully saved to {full_path}"
        except Exception as e:
            return f"Error saving query log: {str(e)}"
    
    def total_orders_by_year(self):
        return self.df.groupby(self.df['ORDERDATE'].dt.year)['ORDERNUMBER'].nunique().to_dict()
    
    def customer_with_most_orders(self):
        return self.df['CUSTOMERNAME'].value_counts().head(1).to_dict()
    
    def top_customers_by_sales(self, top_n=5):
        return self.df.groupby('CUSTOMERNAME')['SALES'].sum().nlargest(top_n).to_dict()
    
    def product_line_sales(self):
        return self.df.groupby('PRODUCTLINE')['SALES'].sum().to_dict()
    
    def sales_by_country(self):
        return self.df.groupby('COUNTRY')['SALES'].sum().to_dict()
    
    def order_status_distribution(self):
        return self.df['STATUS'].value_counts().to_dict()
    
    def orders_by_month_wrapper(self, year=None):
        if year is None:
            year = self.df['ORDERDATE'].dt.year.max()
        yearly_data = self.df[self.df['ORDERDATE'].dt.year == year]
        return yearly_data.groupby(yearly_data['ORDERDATE'].dt.month)['ORDERNUMBER'].count().to_dict()
    
    def customers_by_country(self):
        return self.df.groupby('COUNTRY')['CUSTOMERNAME'].nunique().to_dict()