

from mongo import find_event_by_event_id, update_event_by_event_id
from pytest_utils import mock_db


def test_find_event_by_event_id():

    db = mock_db()
    db['events'].insert_one({'event_id': 123})

    result = find_event_by_event_id(db, 123)
    assert result['event_id'] == 123

    result = find_event_by_event_id(db, 456)
    assert result is None


def test_update_event_by_event_id():

    db = mock_db()
    db['events'].insert_one({'event_id': 123, 'name': 'Old Event'})

    update_event_by_event_id(db, 123, {'name': 'New Event'})
    result = find_event_by_event_id(db, 123)
    assert result['name'] == 'New Event'

    update_event_by_event_id(db, 456, {'name': 'Another Event'})
    result = find_event_by_event_id(db, 456)
    assert result is None