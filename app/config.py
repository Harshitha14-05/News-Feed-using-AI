import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_news_api_key')
    OPENAI_KEY = os.getenv('OPENAI_KEY', 'your_openai_key')
    
    # Application Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    PDF_OUTPUT_DIR = os.getenv('PDF_OUTPUT_DIR', 'static/pdfs')
    
    # Police Districts
    POLICE_DISTRICTS = [
        "Mumbai Police",
        "Delhi Police",
        "Bangalore Police",
        "Hyderabad Police",
        "Chennai Police",
        "Kolkata Police"
    ]
    
    DEFAULT_DISTRICT = "Mumbai Police"
    
    # News Processing
    MAX_ARTICLES = 50
    CLUSTER_THRESHOLD = 0.5
    
    @staticmethod
    def init_app(app):
        pass