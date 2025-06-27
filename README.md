# NBA Player Analyzer

A comprehensive tool for comparing NBA player statistics across different regular seasons.

## Features

- **Player Search**: Search for NBA players by name
- **Season Comparison**: Compare players across different regular seasons
- **Comprehensive Stats**: View points, rebounds, assists, steals, blocks, and shooting percentages
- **Visual Analysis**: Interactive charts and graphs for easy comparison
- **Web Interface**: Modern, responsive web application
- **Command Line Interface**: Original CLI for quick comparisons

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd nba-analyzer-1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)

1. Start the web server:
```bash
python run_app.py
```

2. Open your browser and navigate to: `http://localhost:5000`

3. Use the web interface to:
   - Search for players by name
   - Select seasons (1950-present)
   - View comparison tables and visualizations
   - Enjoy a modern, responsive design

### Command Line Interface

Run the original CLI version:
```bash
python src/main.py
```

Follow the prompts to:
- Enter player names
- Select season years
- View comparison results

## API Endpoints

The web application provides the following API endpoints:

- `GET /` - Main web interface
- `POST /api/search-players` - Search for players by name
- `POST /api/compare-players` - Compare two players' statistics

## Features

### Player Statistics
- **Per Game Averages**: Points, rebounds, assists, steals, blocks
- **Shooting Percentages**: Field goal %, 3-point %, free throw %, true shooting %
- **Regular Season Data**: Comprehensive regular season statistics
- **Historical Data**: Access to NBA statistics from 1950 to present

### Visualizations
- **Bar Charts**: Side-by-side comparison of per-game statistics
- **Shooting Charts**: Visual comparison of shooting percentages
- **Interactive Tables**: Formatted comparison tables

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Search**: Instant player search with autocomplete
- **Error Handling**: Clear error messages and validation
- **Loading States**: Visual feedback during data processing

## Technical Details

### Backend
- **Flask**: Web framework for the API
- **Basketball Reference Scraper**: Data source for NBA statistics
- **Matplotlib**: Chart generation
- **NumPy**: Numerical computations

### Frontend
- **Bootstrap 5**: Modern CSS framework
- **Font Awesome**: Icons
- **Vanilla JavaScript**: No external dependencies
- **Responsive Design**: Mobile-first approach

## Example Usage

### Web Interface
1. Search for "LeBron James"
2. Select "LeBron James" from results
3. Choose season year "2023"
4. Search for "Stephen Curry"
5. Select "Stephen Curry" from results
6. Choose season year "2023"
7. Click "Compare Players"
8. View detailed comparison table and charts

### Command Line
```
=== NBA Player Season Comparison Tool ===
Compare NBA players' regular season statistics across different seasons.

--- PLAYER 1 ---
Full name: LeBron James
Season end year (e.g. 2021 for 2020-21): 2023

--- PLAYER 2 ---
Full name: Stephen Curry
Season end year (e.g. 2021 for 2020-21): 2023
```

## Requirements

- Python 3.7+
- Internet connection (for data fetching)
- Web browser (for web interface)

## Dependencies

- `flask` - Web framework
- `flask-cors` - Cross-origin resource sharing
- `basketball_reference_web_scraper` - NBA data source
- `matplotlib` - Chart generation
- `numpy` - Numerical computations
- `requests` - HTTP requests

## License

This project is for educational purposes. Please respect the terms of service of Basketball Reference.

## Contributing

Feel free to submit issues and enhancement requests!
