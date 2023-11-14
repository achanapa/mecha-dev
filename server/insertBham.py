from pymongo import MongoClient

CONNECTION_STRING = 'mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/'
client = MongoClient(CONNECTION_STRING)
Database = client['Dimension']
Collection = Database['BoltBitHead']

data = {
    '_id': 2,
    'M_Size': 4,
    'Head_Length' : 4, 
    'Thread_Length' : 12.2, 
    'Head_Diameter' : 4, 
    'Thread_Diameter' : 3.89, 
    'Space_Length' : 0,
    'type_head': 'HEX',
    'type_bit': 'ALLEN'
}

Collection.insert_one(data)

cursor = Collection.find()
count = Collection.count_documents({})
print(count)
print(cursor[count-1])

# for i in cursor:
#     print('Bolt size = '+str(i['M_Size']))
#     print('With Head Length of '+str(i['Head_Length'])+' mm and Head Diameter of '+str(i['Head_Diameter'])+' mm')
#     print('Thread Length of '+str(i['Thread_Length'])+' mm and Thread Diameter of '+str(i['Thread_Diameter'])+' mm')
#     if float(i['Space_Length']) != 0:
#         print('Space Length of '+str(i['Space_Length'])+' mm')