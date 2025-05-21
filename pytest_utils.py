
import mongomock

def mock_db():
    client = mongomock.MongoClient()
    db = client['testdb']
    return db