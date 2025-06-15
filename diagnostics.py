from basketball_reference_web_scraper import client

def test_search(player_name):
    print(f"\nTesting search for: {player_name}")
    try:
        result = client.search(term=player_name)
        print(f"Type of result: {type(result)}")
        print(f"Result content: {result}")
        
        if isinstance(result, list):
            print("\nList items:")
            for i, item in enumerate(result, 1):
                print(f"{i}. Type: {type(item)}, Content: {item}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def test_player_stats(player_id, year):
    print(f"\nTesting player stats for: {player_id} in {year}")
    try:
        # Test regular season
        print("\nRegular season stats:")
        reg_stats = client.players_season_totals(season_end_year=year)
        player_data = next((p for p in reg_stats if p['slug'] == player_id), None)
        print(f"Found: {bool(player_data)}")
        if player_data:
            print(f"Games: {player_data['games_played']}")
            print(f"PPG: {player_data['points']/player_data['games_played']:.1f}")
        
        # Test playoffs
        print("\nPlayoff stats:")
        playoff_stats = client.playoff_player_box_scores(
            player_identifier=player_id,
            season_end_year=year
        )
        print(f"Found {len(playoff_stats)} playoff games")
        if playoff_stats:
            print(f"First game stats: {playoff_stats[0]}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Test with LeBron James
test_search("LeBron James")
test_player_stats("jamesle01", 2020)

# Test with Anthony Davis
test_search("Anthony Davis")
test_player_stats("davisan02", 2021)

# Test with a partial name
test_search("Jokic")