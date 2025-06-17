from basketball_reference_web_scraper import client

def get_player_id(full_name):
    """Get player identifier using search"""
    search_result = client.search(term=full_name)
    if not search_result or 'players' not in search_result or not search_result['players']:
        raise ValueError(f"No players found for: {full_name}")
    
    players = search_result['players']
    if len(players) == 1:
        return players[0]['identifier']
    
    print(f"\nMultiple players found for '{full_name}':")
    for i, player in enumerate(players, 1):
        print(f"{i}. {player['name']} ({player['identifier']})")
    
    selection = int(input("Enter the number of the correct player: ")) - 1
    return players[selection]['identifier']