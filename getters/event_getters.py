def get_event_role_id(event):

    if 'event_role_id' in event:
        return event['event_role_id']
    
    return None