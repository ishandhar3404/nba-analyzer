from basketball_reference_web_scraper import client

def get_regular_season_stats(player_id, year):
    """Get regular season stats using season totals"""
    all_players = client.players_season_totals(season_end_year=year)
    player_data = next((p for p in all_players if p['slug'] == player_id), None)
    
    if not player_data:
        raise ValueError(f"No regular season data found for {player_id} in {year}")
    
    # Calculate stats
    games = player_data['games_played']
    total_rebounds = player_data['offensive_rebounds'] + player_data['defensive_rebounds']
    
    fg_pct = (player_data['made_field_goals'] / player_data['attempted_field_goals']) * 100
    three_pct = (player_data['made_three_point_field_goals'] / player_data['attempted_three_point_field_goals']) * 100
    ft_pct = (player_data['made_free_throws'] / player_data['attempted_free_throws']) * 100
    
    ts_attempts = player_data['attempted_field_goals'] + 0.44 * player_data['attempted_free_throws']
    ts_pct = (player_data['points'] / (2 * ts_attempts)) * 100 if ts_attempts > 0 else 0
    
    return {
        'games_played': games,
        'points': player_data['points'] / games,
        'rebounds': total_rebounds / games,
        'assists': player_data['assists'] / games,
        'steals': player_data['steals'] / games,
        'blocks': player_data['blocks'] / games,
        'fg_pct': fg_pct,
        '3p_pct': three_pct,
        'ft_pct': ft_pct,
        'ts_pct': ts_pct
    }

def get_player_stats(player_id, year):
    """Get player stats for regular season"""
    return get_regular_season_stats(player_id, year)