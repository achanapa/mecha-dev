from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_db(app):
    db.init_app(app)
    # Connect to the MongoDB database
    app.config['MONGODB_SETTINGS'] = {
        'db': 'Dimension',
        'host': 'mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/',
    }
