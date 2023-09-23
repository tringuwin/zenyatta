import constants

def get_event_role_id(event):

    if 'event_role_id' in event:
        return event['event_role_id']
    
    return None

def get_event_by_id(db, event_id):

    events = db['events']

    search_query = {"event_id": event_id}

    return events.find_one(search_query)

def get_event_channel_id(event):

    if 'event_channel_id' in event:
        return event['event_channel_id']
    
    return constants.EVENT_CHANNEL_ID