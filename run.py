#!/usr/bin/env python3
from app import create_app
from app.utils import setup_jinja_filters
import os
from datetime import datetime

# Create and configure the Flask application
app = create_app()

# Setup custom Jinja2 filters
setup_jinja_filters(app)

# Add current year to template context
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    # Configuration
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    # Create necessary directories
    os.makedirs(app.config['PDF_OUTPUT_DIR'], exist_ok=True)
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True,
        ssl_context='adhoc' if os.getenv('USE_HTTPS') else None
    )