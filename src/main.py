from services.player_service import get_player_id
from services.stats_service import get_regular_season_stats, get_player_stats
from utils.visualization import compare_players_visual
from utils.helpers import format_comparison_table

def main():
    print("=== NBA Player Season Comparison Tool ===")
    print("Compare NBA players' regular season statistics across different seasons.\n")
    
    # Player 1
    print("--- PLAYER 1 ---")
    name1 = input("Full name: ")
    year1 = int(input("Season end year (e.g. 2021 for 2020-21): "))
    
    # Player 2
    print("\n--- PLAYER 2 ---")
    name2 = input("Full name: ")
    year2 = int(input("Season end year (e.g. 2021 for 2020-21): "))
    
    try:
        # Get player IDs
        player_id1 = get_player_id(name1)
        player_id2 = get_player_id(name2)
        
        # Get season stats
        print(f"\nFetching data for {name1} ({year1})...")
        stats1 = get_player_stats(player_id1, year1)
        print(f"✓ Successfully retrieved regular season data for {name1}")
        
        print(f"Fetching data for {name2} ({year2})...")
        stats2 = get_player_stats(player_id2, year2)
        print(f"✓ Successfully retrieved regular season data for {name2}")
        
        # Format player names with season info
        player1_full = f"{name1} ({year1} regular season)"
        player2_full = f"{name2} ({year2} regular season)"
        
        # Print comparison
        print(format_comparison_table(player1_full, stats1, player2_full, stats2))
        
        # Visual comparison
        compare_players_visual(player1_full, stats1, player2_full, stats2)
        
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()