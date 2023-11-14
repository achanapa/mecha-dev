from server.database import db

class BoltBitHead(db.Document):
    # Define your BoltBitHead data model here
    bolt_id = db.IntField(required=True)
    M_Size = db.IntField()
    Head_Length = db.IntField()
    Thread_Length = db.IntField()
    Head_Diameter = db.IntField()
    Thread_Diameter = db.IntField()
    Space_Length = db.IntField()
    type_head = db.StringField(required=True)
    type_bit = db.StringField(required=True)

    @staticmethod
    def save_bolt_bit_head(data):
        # Implement logic to save BoltBitHead data
        # For example, you can create a new BoltBitHead document with the provided data
        bolt_bit_head = BoltBitHead(**data)
        bolt_bit_head.save()
