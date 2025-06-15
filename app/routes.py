
from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash, current_app
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .news_processor import process_news
from .pdf_generator import create_pdf_report
from .config import Config
from datetime import datetime
import os

main = Blueprint('main', __name__)

# In-memory user store (replace with database in production)
users = {
    'police_officer': {
        'password': generate_password_hash('securepassword123'),
        'badge_number': 'PD-12345',
        'department': 'Cyber Crime Unit'
    }
}

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password')
            return redirect(url_for('main.login'))
        
        user = users.get(username)
        
        if not user or not check_password_hash(user['password'], password):
            flash('Invalid badge number or password')
            return redirect(url_for('main.login'))
        
        # Create user object and log in
        from .models import User
        user_obj = User(username)
        login_user(user_obj)
        
        # Log access
        current_app.logger.info(f"User {username} logged in at {datetime.now()}")
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))
    
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully')
    return redirect(url_for('main.login'))

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        date = request.form.get('date')
        district = request.form.get('district', Config.DEFAULT_DISTRICT)
        
        # Validate date
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD')
            return render_template('index.html', 
                                districts=Config.POLICE_DISTRICTS,
                                default_district=Config.DEFAULT_DISTRICT)
        
        # Process news
        try:
            data = process_news(date, district)
            if not data:
                flash('No news articles found for the selected date and district')
                return render_template('index.html',
                                    districts=Config.POLICE_DISTRICTS,
                                    default_district=Config.DEFAULT_DISTRICT)
            
            return render_template('report.html', 
                                data=data, 
                                date=date, 
                                district=district,
                                current_user=current_user)
        
        except Exception as e:
            current_app.logger.error(f"Error processing news: {str(e)}")
            flash('An error occurred while generating the report. Please try again.')
            return render_template('index.html',
                                districts=Config.POLICE_DISTRICTS,
                                default_district=Config.DEFAULT_DISTRICT)
    
    # GET request - show form
    return render_template('index.html',
                         districts=Config.POLICE_DISTRICTS,
                         default_district=Config.DEFAULT_DISTRICT)

@main.route('/download-pdf/<date>/<district>')
@login_required
def download_pdf(date, district):
    try:
        # Validate date format first
        datetime.strptime(date, '%Y-%m-%d')
        
        # Generate PDF
        pdf_path = create_pdf_report(date, district)
        
        if not os.path.exists(pdf_path):
            flash('PDF could not be generated')
            return redirect(url_for('main.index'))
        
        # Send file with proper filename
        filename = f"Police_Digest_{district.replace(' ', '_')}_{date}.pdf"
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except ValueError:
        flash('Invalid date format')
        return redirect(url_for('main.index'))
    except Exception as e:
        current_app.logger.error(f"PDF generation error: {str(e)}")
        flash('An error occurred while generating the PDF')
        return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    user_data = users.get(current_user.id, {})
    return render_template('profile.html',
                         badge_number=user_data.get('badge_number'),
                         department=user_data.get('department'))