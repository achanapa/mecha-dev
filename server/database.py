from flask_pymongo import PyMongo

def initialize_db(app):
    app.config['MONGO_URI'] = 'mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/Dimension'
    app.config['MONGO_DBNAME'] = 'Dimension'
    PyMongo.init_app(app)


# from flask_pymongo import PyMongo

# mongo = PyMongo()

# def initialize_db(app):
#     app.config['MONGO_URI'] = 'mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/Dimension'
#     app.config['MONGO_DBNAME'] = 'Dimension'
#     mongo.init_app(app)