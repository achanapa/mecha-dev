from server.database import db

class BoltDimension(db.Document):
    # Define your BoltDimension data model here
    bolt_id = db.IntField(required=True)
    M_Size = db.IntField()
    Head_Length = db.IntField()
    Thread_Length = db.IntField()
    Head_Diameter = db.IntField()
    Thread_Diameter = db.IntField()
    Space_Length = db.IntField()

    @staticmethod
    def get_recent_bolt_data():
        # Implement logic to fetch and return recent bolt data
        # For example, you can fetch the latest bolt data based on a timestamp
        return BoltDimension.objects.order_by('-timestamp').first().to_json()
