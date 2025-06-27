from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.player_service import get_player_id
from services.stats_service import get_regular_season_stats, get_player_stats
from utils.helpers import format_comparison_table
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search-players', methods=['POST'])
def search_players():
    try:
        data = request.get_json()
        search_term = data.get('search_term', '')
        
        if not search_term:
            return jsonify({'error': 'Search term is required'}), 400
        
        from basketball_reference_web_scraper import client
        search_result = client.search(term=search_term)
        
        if not search_result or 'players' not in search_result or not search_result['players']:
            return jsonify({'players': []})
        
        players = []
        for player in search_result['players']:
            players.append({
                'id': player['identifier'],
                'name': player['name']
            })
        
        return jsonify({'players': players})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare-players', methods=['POST'])
def compare_players():
    try:
        data = request.get_json()
        
        # Extract player data
        player1_data = data.get('player1', {})
        player2_data = data.get('player2', {})
        
        # Validate required fields
        required_fields = ['id', 'name', 'year']
        for player_data in [player1_data, player2_data]:
            for field in required_fields:
                if field not in player_data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get stats for both players
        try:
            player1_stats = get_player_stats(player1_data['id'], player1_data['year'])
        except Exception as e:
            return jsonify({'error': f"Failed to get data for {player1_data['name']}: {str(e)}"}), 400
        
        try:
            player2_stats = get_player_stats(player2_data['id'], player2_data['year'])
        except Exception as e:
            return jsonify({'error': f"Failed to get data for {player2_data['name']}: {str(e)}"}), 400
        
        # Format player names
        player1_full = f"{player1_data['name']} ({player1_data['year']} regular season)"
        player2_full = f"{player2_data['name']} ({player2_data['year']} regular season)"
        
        # Create comparison table
        comparison_table = format_comparison_table(player1_full, player1_stats, player2_full, player2_stats)
        
        # Create visualization
        chart_data = create_comparison_chart(player1_full, player1_stats, player2_full, player2_stats)
        
        return jsonify({
            'comparison_table': comparison_table,
            'chart_data': chart_data,
            'player1_stats': player1_stats,
            'player2_stats': player2_stats
        })
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

def create_comparison_chart(player1_name, player1_stats, player2_name, player2_stats):
    """Create comparison chart and return as base64 encoded image"""
    fig, ax = plt.subplots(2, 1, figsize=(12, 14))
    
    # Basic stats comparison
    categories = ['points', 'rebounds', 'assists', 'steals', 'blocks']
    player1_values = [player1_stats[cat] for cat in categories]
    player2_values = [player2_stats[cat] for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax[0].bar(x - width/2, player1_values, width, label=player1_name, color='#1f77b4')
    ax[0].bar(x + width/2, player2_values, width, label=player2_name, color='#ff7f0e')
    
    ax[0].set_title('Per Game Statistics Comparison', fontsize=16, fontweight='bold')
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
    
    ax[1].bar(x - width/2, player1_shooting, width, label=player1_name, color='#1f77b4')
    ax[1].bar(x + width/2, player2_shooting, width, label=player2_name, color='#ff7f0e')
    
    ax[1].set_title('Shooting Percentage Comparison', fontsize=16, fontweight='bold')
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
                 ha='center', fontsize=10, fontweight='bold')
    
    for i in ax[1].patches:
        ax[1].text(i.get_x() + i.get_width()/2, i.get_height()+0.5, 
                 f'{i.get_height():.1f}%', 
                 ha='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
    img.seek(0)
    chart_data = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return chart_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 