from datetime import datetime
import re
import string

def validate_date(date_str):
    """Validate date string format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def clean_text(text):
    """Clean and normalize text for processing"""
    if not text:
        return ""
    
    # Remove special characters and normalize whitespace
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def format_datetime(value, format='%Y-%m-%d %H:%M'):
    """Jinja2 filter for datetime formatting"""
    if not value:
        return ""
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').strftime(format)

def setup_jinja_filters(app):
    """Register custom Jinja2 filters"""
    app.jinja_env.filters['datetimeformat'] = format_datetime