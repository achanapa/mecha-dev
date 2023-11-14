from flask import Flask
from routes.bolt_bit_head import bolt_bit_head_bp
from routes.bolt_dimension import bolt_dimension_bp
from config import Config
from database import initialize_db
from flask_pymongo import PyMongo
from models.bolt_dimension import BoltDimension
from database import initialize_db



# def create_app():
#     app = Flask(__name__)

#     # Load configuration from Config class
#     app.config.from_object(Config)

#     # Initialize the database connection
#     initialize_db(app)

#     # Initialize the BoltDimension model with the app context
#     BoltDimension.init_app(app)

#     # Register blueprints
#     app.register_blueprint(bolt_dimension_bp)
#     app.register_blueprint(bolt_bit_head_bp)

#     return app

def create_app():
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize the database connection
    initialize_db(app)

    # Initialize the BoltDimension model with the app context
    BoltDimension.init_app(app)

    # Register blueprints
    app.register_blueprint(bolt_dimension_bp)
    app.register_blueprint(bolt_bit_head_bp)

    return app




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
