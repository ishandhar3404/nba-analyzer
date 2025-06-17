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

def get_playoff_stats(player_id, year):
    """Get playoff stats by aggregating box scores"""
    try:
        box_scores = client.playoff_player_box_scores(
            player_identifier=player_id,
            season_end_year=year
        )
    except Exception as e:
        raise ValueError(f"Failed to get playoff box scores: {str(e)}")
    
    if not box_scores:
        raise ValueError(f"No playoff games found for {player_id} in {year}")
    
    # Aggregate stats
    totals = {
        'games_played': len(box_scores),
        'points': 0,
        'offensive_rebounds': 0,
        'defensive_rebounds': 0,
        'assists': 0,
        'steals': 0,
        'blocks': 0,
        'made_field_goals': 0,
        'attempted_field_goals': 0,
        'made_three_point_field_goals': 0,
        'attempted_three_point_field_goals': 0,
        'made_free_throws': 0,
        'attempted_free_throws': 0,
    }
    
    for game in box_scores:
        totals['points'] += game['points']
        totals['offensive_rebounds'] += game['offensive_rebounds']
        totals['defensive_rebounds'] += game['defensive_rebounds']
        totals['assists'] += game['assists']
        totals['steals'] += game['steals']
        totals['blocks'] += game['blocks']
        totals['made_field_goals'] += game['made_field_goals']
        totals['attempted_field_goals'] += game['attempted_field_goals']
        totals['made_three_point_field_goals'] += game['made_three_point_field_goals']
        totals['attempted_three_point_field_goals'] += game['attempted_three_point_field_goals']
        totals['made_free_throws'] += game['made_free_throws']
        totals['attempted_free_throws'] += game['attempted_free_throws']
    
    # Calculate per-game averages
    games = totals['games_played']
    stats = {
        'games_played': games,
        'points': totals['points'] / games,
        'rebounds': (totals['offensive_rebounds'] + totals['defensive_rebounds']) / games,
        'assists': totals['assists'] / games,
        'steals': totals['steals'] / games,
        'blocks': totals['blocks'] / games,
    }
    
    # Calculate shooting percentages
    stats['fg_pct'] = (totals['made_field_goals'] / totals['attempted_field_goals']) * 100 if totals['attempted_field_goals'] > 0 else 0
    stats['3p_pct'] = (totals['made_three_point_field_goals'] / totals['attempted_three_point_field_goals']) * 100 if totals['attempted_three_point_field_goals'] > 0 else 0
    stats['ft_pct'] = (totals['made_free_throws'] / totals['attempted_free_throws']) * 100 if totals['attempted_free_throws'] > 0 else 0
    
    # Calculate true shooting percentage
    ts_attempts = totals['attempted_field_goals'] + 0.44 * totals['attempted_free_throws']
    stats['ts_pct'] = (totals['points'] / (2 * ts_attempts)) * 100 if ts_attempts > 0 else 0
    
    return stats