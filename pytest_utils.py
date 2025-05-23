
import mongomock

MOCK_GEMS = {
    'red': 1,
    'blue': 2,
    'yellow': 3,
    'green': 4,
    'purple': 5,
    'orange': 6,
    'pink': 7,
    'teal': 8,
    'white': 9,
    'black': 10
}

def mock_db():
    client = mongomock.MongoClient()
    db = client['testdb']
    return db
