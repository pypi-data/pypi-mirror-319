# MLB Odds Scraper

A Python package for scraping MLB odds data from OddsPortal. This package provides tools to easily retrieve and analyze betting odds for MLB games.

## Installation

```bash
pip install mlb_odds_scraper
```

## Features

- Scrape MLB betting odds from OddsPortal
- Support for multiple bookmakers
- Clean and structured data output
- Integration with MLB-StatsAPI for additional game data

## Requirements

- Python >= 3.8
- Chrome/Chromium browser installed

## Dependencies

- pandas >= 1.0.0
- selenium >= 4.0.0
- stealthenium >= 0.1.0
- sqlalchemy >= 1.4.0
- MLB-StatsAPI >= 1.0.0

## Usage

```python
from mlb_odds_scraper import OddsScraper

# Initialize the scraper
scraper = OddsScraper()

# Get odds for a specific date
odds_data = scraper.get_odds_by_date("2024-04-01")

# Export to CSV
odds_data.to_csv("mlb_odds.csv")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 