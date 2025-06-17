import matplotlib.pyplot as plt
import numpy as np

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