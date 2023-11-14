from flask import Flask
from server.routes import bolt_dimension_bp, bolt_bit_head_bp
from server.config import Config
from server.database import initialize_db

def create_app():
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize the database connection
    initialize_db(app)

    # Register blueprints
    app.register_blueprint(bolt_dimension_bp)
    app.register_blueprint(bolt_bit_head_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
