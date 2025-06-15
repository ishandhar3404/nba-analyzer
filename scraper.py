from basketball_reference_web_scraper import client
import matplotlib.pyplot as plt
import numpy as np

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

def get_season_stats(player_id, year, season_type="regular"):
    """Get player stats using the more reliable season totals method"""
    try:
        if season_type == "regular":
            all_players = client.players_season_totals(season_end_year=year)
        else:
            all_players = client.players_advanced_season_totals(season_end_year=year)
            
        player_data = next((p for p in all_players if p['slug'] == player_id), None)
        
        if not player_data:
            raise ValueError(f"No data found for {player_id} in {year} {season_type} season")
        
        # Calculate total rebounds
        total_rebounds = player_data['offensive_rebounds'] + player_data['defensive_rebounds']
        
        # Calculate shooting percentages
        fg_pct = (player_data['made_field_goals'] / player_data['attempted_field_goals']) * 100
        three_pct = (player_data['made_three_point_field_goals'] / player_data['attempted_three_point_field_goals']) * 100
        ft_pct = (player_data['made_free_throws'] / player_data['attempted_free_throws']) * 100
        
        # Calculate true shooting percentage
        ts_attempts = player_data['attempted_field_goals'] + 0.44 * player_data['attempted_free_throws']
        ts_pct = (player_data['points'] / (2 * ts_attempts)) * 100 if ts_attempts > 0 else 0
        
        # Return per-game averages
        games = player_data['games_played']
        return {
            'games_played': games,
            'points': player_data['points'] / games,
            'rebounds': total_rebounds / games,
            'offensive_rebounds': player_data['offensive_rebounds'] / games,
            'defensive_rebounds': player_data['defensive_rebounds'] / games,
            'assists': player_data['assists'] / games,
            'steals': player_data['steals'] / games,
            'blocks': player_data['blocks'] / games,
            'fg_pct': fg_pct,
            '3p_pct': three_pct,
            'ft_pct': ft_pct,
            'ts_pct': ts_pct
        }
        
    except Exception as e:
        raise ValueError(f"Error fetching stats: {str(e)}")

def compare_players_visual(player1_name, player1_stats, player2_name, player2_stats):
    """Create visual comparison of two players"""
    fig, ax = plt.subplots(2, 1, figsize=(12, 14))
    
    # Basic stats comparison
    categories = ['points', 'rebounds', 'assists', 'steals', 'blocks']
    player1_values = [player1_stats[cat] for cat in categories]
    player2_values = [player2_stats[cat] for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax[0].bar(x - width/2, player1_values, width, label=player1_name)
    ax[0].bar(x + width/2, player2_values, width, label=player2_name)
    
    ax[0].set_title('Per Game Statistics Comparison', fontsize=16)
    ax[0].set_xticks(x)
    ax[0].set_xticklabels([cat.capitalize() for cat in categories])
    ax[0].legend()
    ax[0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Shooting comparison
    shooting_categories = ['fg_pct', '3p_pct', 'ft_pct', 'ts_pct']
    labels = ['FG%', '3P%', 'FT%', 'TS%']
    player1_shooting = [player1_stats[cat] for cat in shooting_categories]
    player2_shooting = [player2_stats[cat] for cat in shooting_categories]
    
    x = np.arange(len(labels))
    
    ax[1].bar(x - width/2, player1_shooting, width, label=player1_name)
    ax[1].bar(x + width/2, player2_shooting, width, label=player2_name)
    
    ax[1].set_title('Shooting Percentage Comparison', fontsize=16)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(labels)
    ax[1].set_ylabel('Percentage')
    ax[1].set_ylim(0, 100)
    ax[1].legend()
    ax[1].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels
    for i in ax[0].patches:
        ax[0].text(i.get_x() + i.get_width()/2, i.get_height()+0.5, 
                 f'{i.get_height():.1f}', 
                 ha='center', fontsize=10)
    
    for i in ax[1].patches:
        ax[1].text(i.get_x() + i.get_width()/2, i.get_height()+0.5, 
                 f'{i.get_height():.1f}%', 
                 ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.show()

def main():
    print("=== NBA Player Season Comparison Tool ===")
    
    # Player 1
    print("\n--- PLAYER 1 ---")
    name1 = input("Full name: ")
    year1 = int(input("Season end year (e.g. 2021 for 2020-21): "))
    season_type1 = input("Season type (regular/playoffs): ").lower() or "regular"
    
    # Player 2
    print("\n--- PLAYER 2 ---")
    name2 = input("Full name: ")
    year2 = int(input("Season end year (e.g. 2021 for 2020-21): "))
    season_type2 = input("Season type (regular/playoffs): ").lower() or "regular"
    
    try:
        # Get player IDs
        player_id1 = get_player_id(name1)
        player_id2 = get_player_id(name2)
        
        # Get season stats
        print(f"\nFetching data for {name1} ({year1})...")
        stats1 = get_season_stats(player_id1, year1, season_type1)
        print(f"Fetching data for {name2} ({year2})...")
        stats2 = get_season_stats(player_id2, year2, season_type2)
        
        # Print comparison
        print(f"\n{name1} ({year1} {season_type1}) vs {name2} ({year2} {season_type2})")
        print("="*60)
        print(f"{'Stat':<20} {name1.split()[-1]:>15} {name2.split()[-1]:>15}")
        print("-"*60)
        
        stats_to_show = [
            ('Games', 'games_played', '{:.0f}'),
            ('Points', 'points', '{:.1f}'),
            ('Rebounds', 'rebounds', '{:.1f}'),
            ('Off Reb', 'offensive_rebounds', '{:.1f}'),
            ('Def Reb', 'defensive_rebounds', '{:.1f}'),
            ('Assists', 'assists', '{:.1f}'),
            ('Steals', 'steals', '{:.1f}'),
            ('Blocks', 'blocks', '{:.1f}'),
            ('FG%', 'fg_pct', '{:.1f}%'),
            ('3P%', '3p_pct', '{:.1f}%'),
            ('FT%', 'ft_pct', '{:.1f}%'),
            ('TS%', 'ts_pct', '{:.1f}%'),
        ]
        
        for stat_name, stat_key, fmt in stats_to_show:
            val1 = fmt.format(stats1[stat_key])
            val2 = fmt.format(stats2[stat_key])
            print(f"{stat_name:<20} {val1:>15} {val2:>15}")
        
        # Visual comparison
        compare_players_visual(
            f"{name1} ({year1})", stats1,
            f"{name2} ({year2})", stats2
        )
        
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        print("Tip: Try a different season type or check the player's stats availability")

if __name__ == "__main__":
    main()