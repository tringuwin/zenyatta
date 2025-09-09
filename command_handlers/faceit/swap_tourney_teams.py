

from helpers import get_constant_value, set_constant_value
from safe_send import safe_send


async def swap_tourney_teams(db, message):
    
    tourney_widget_data = get_constant_value(db, 'tourney_widget')
    
    new_tourney_widget_data = {
        'team1': tourney_widget_data['team2'],
        'team2': tourney_widget_data['team1'],
        'team1_score': tourney_widget_data['team2_score'],
        'team2_score': tourney_widget_data['team1_score'],
        'team1_color': tourney_widget_data['team1_color'], # keep the color of team1
        'team2_color': tourney_widget_data['team2_color'], # keep the color of team2
    }

    set_constant_value(db, 'tourney_widget', new_tourney_widget_data)

    await safe_send(message.channel, "Tournament teams swapped")