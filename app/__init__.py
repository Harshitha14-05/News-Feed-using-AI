from flask import Flask
from flask_login import LoginManager
from .config import Config

def create_app():
    # Corrected this line - changed _name_ to __name__
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    
    # Mock user for MVP
    from flask_login import UserMixin
    class User(UserMixin):
        def __init__(self, id):
            self.id = id
    
    # In-memory user store (replace with database in production)
    users = {'police_officer': {'password': 'securepassword123'}}  # Mock credentials
    
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id) if user_id in users else None
    
    from .routes import main
    app.register_blueprint(main)
    
    return app