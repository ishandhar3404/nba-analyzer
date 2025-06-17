def format_comparison_table(player1_name, player1_stats, player2_name, player2_stats):
    """Format player comparison as a table"""
    output = []
    output.append(f"\n{player1_name} vs {player2_name}")
    output.append("="*60)
    output.append(f"{'Stat':<20} {player1_name.split()[-1]:>15} {player2_name.split()[-1]:>15}")
    output.append("-"*60)
    
    stats_to_show = [
        ('Games', 'games_played', '{:.0f}'),
        ('Points', 'points', '{:.1f}'),
        ('Rebounds', 'rebounds', '{:.1f}'),
        ('Assists', 'assists', '{:.1f}'),
        ('Steals', 'steals', '{:.1f}'),
        ('Blocks', 'blocks', '{:.1f}'),
        ('FG%', 'fg_pct', '{:.1f}%'),
        ('3P%', '3p_pct', '{:.1f}%'),
        ('FT%', 'ft_pct', '{:.1f}%'),
        ('TS%', 'ts_pct', '{:.1f}%'),
    ]
    
    for stat_name, stat_key, fmt in stats_to_show:
        val1 = fmt.format(player1_stats[stat_key])
        val2 = fmt.format(player2_stats[stat_key])
        output.append(f"{stat_name:<20} {val1:>15} {val2:>15}")
    
    return "\n".join(output)