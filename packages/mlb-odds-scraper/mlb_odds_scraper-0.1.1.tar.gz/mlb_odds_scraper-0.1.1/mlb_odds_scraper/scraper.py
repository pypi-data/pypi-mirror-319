"""MLB Odds Scraper for retrieving odds data from OddsPortal."""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import statsapi

def scrape_page(year, page_num):
    """
    Scrape a single page of MLB odds data.
    
    Args:
        year (int): Year to scrape data for
        page_num (int): Page number to scrape
        
    Returns:
        list: List of dictionaries containing game data
    """
    games = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.oddsportal.com/baseball/usa/mlb-{year}/results/#/page/{page_num}/")
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-b8d70024].eventRow"))
        )
        events = driver.find_elements(By.CSS_SELECTOR, "div[data-v-b8d70024].eventRow")
    except:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-b8d70024][id][set]"))
            )
            events = driver.find_elements(By.CSS_SELECTOR, "div[data-v-b8d70024][id][set]")
        except:
            events = []

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    print(f"Found {len(events)} events on page {page_num}")
    current_date = None
    
    # Find initial date
    for event in events:
        try:
            date_elements = event.find_elements(By.CLASS_NAME, "text-black-main")
            for date_element in date_elements:
                date_text = date_element.text
                if len(date_text.split()) >= 3 and any(yr in date_text for yr in ["202", "201", "200"]) and "Baseball" not in date_text:
                    current_date = date_text.split(' - ')[0].strip()
                    break
            if current_date:
                break
        except:
            continue
            
    # Process events
    for event in events:
        try:
            try:
                date_elements = event.find_elements(By.CLASS_NAME, "text-black-main")
                for date_element in date_elements:
                    date_text = date_element.text
                    if len(date_text.split()) >= 3 and any(yr in date_text for yr in ["202", "201", "200"]) and "Baseball" not in date_text:
                        current_date = date_text.split(' - ')[0].strip()
            except:
                pass
            
            # Try modern team selector first, then older format
            try:
                teams = event.find_elements(By.CLASS_NAME, "participant-name")
            except:
                teams = event.find_elements(By.CSS_SELECTOR, "p.participant-name")

            # Try modern score format first, then older format
            try:
                score_section = event.find_element(By.CSS_SELECTOR, "div.text-gray-dark div.font-bold")
                scores = score_section.text.split('–')
                home_score = scores[0].strip()
                away_score = scores[1].strip()
            except:
                try:
                    score_elements = event.find_elements(By.CLASS_NAME, "font-bold")
                    home_score = score_elements[0].text.strip()
                    away_score = score_elements[1].text.strip()
                except:
                    home_score = ''
                    away_score = ''
                
            if len(teams) < 2:
                continue

            try:
                time_element = event.find_element(By.XPATH, ".//p[contains(text(), ':')]")
                game_time = time_element.text
            except:
                continue

            home_team = teams[0].text
            away_team = teams[1].text
                
            # Try modern odds selector first, then older format
            try:
                odds_elements = event.find_elements(By.CSS_SELECTOR, "[data-testid='add-to-coupon-button'] .height-content")
            except:
                odds_elements = event.find_elements(By.CSS_SELECTOR, ".gradient-green-added-border")

            if len(odds_elements) >= 2:
                home_odds = odds_elements[0].text
                away_odds = odds_elements[1].text

                if all([current_date, game_time, away_team, home_team, away_odds, home_odds]):
                    game_data = {
                        'date': current_date,
                        'time': game_time,
                        'away_team': away_team,
                        'home_team': home_team,
                        'away_odds': away_odds,
                        'home_odds': home_odds,
                        'away_score': away_score,
                        'home_score': home_score
                    }
                    games.append(game_data)
            
        except Exception as e:
            print(f"Error processing event: {e}")
            continue
    
    driver.quit()
    return games

def scrape_oddsportal_mlb(year, max_pages=None):
    """
    Scrape MLB odds data for a specific year.
    
    Args:
        year (int): Year to scrape MLB data for
        max_pages (int, optional): Maximum number of pages to scrape. If None, scrapes all pages.
    
    Returns:
        list: List of dictionaries containing game data and odds
        
    Usage:
        >>> games = scrape_oddsportal_mlb(2024) # Scrapes all pages
        >>> games = scrape_oddsportal_mlb(2024, max_pages=5) # Scrapes first 5 pages only
    """
    # Get total pages
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.oddsportal.com/baseball/usa/mlb-{year}/results/#/page/1/")
    pagination = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagination"))
    )
    page_links = pagination.find_elements(By.CSS_SELECTOR, "a.pagination-link")
    total_pages = max([int(link.get_attribute('data-number')) for link in page_links if link.get_attribute('data-number')])
    driver.quit()
    
    if max_pages:
        total_pages = min(max_pages, total_pages)
    
    print(f"Will scrape {total_pages} pages")
    
    # Scrape pages concurrently
    all_games = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_page, year, page) for page in range(1, total_pages + 1)]
        for future in futures:
            all_games.extend(future.result())
            
    print(f"Total games collected: {len(all_games)}")
    return all_games

def scrape_oddsportal_mlb_years(start_year=2006, end_year=2025, max_pages=None):
    """
    Scrapes MLB odds data for multiple years.
    
    Args:
        start_year (int): First year to scrape (inclusive)
        end_year (int): Last year to scrape (exclusive)
        max_pages (int, optional): Maximum number of pages to scrape per year
        
    Returns:
        pd.DataFrame: Combined dataframe of all scraped games
        
    Usage:
        >>> df = scrape_oddsportal_mlb_years(2020, 2024) # Scrapes 2020-2023
        >>> df = scrape_oddsportal_mlb_years() # Scrapes 2006-2024
    """
    all_games = []
    for year in range(start_year, end_year):
        print(f"\nScraping year {year}...")
        games = scrape_oddsportal_mlb(year, max_pages)
        all_games.extend(games)
        
    return pd.DataFrame(all_games)

def process_game_data(df):
    """
    Process raw MLB game data by cleaning and transforming fields.
    
    Args:
        df (pd.DataFrame): Raw dataframe containing MLB game data
        
    Returns:
        pd.DataFrame: Processed dataframe with cleaned and transformed data
        
    Usage:
        >>> processed_df = process_game_data(raw_df)
        >>> processed_df.head()
           game_date  game_datetime  home_team  away_team ...
    """
    processed_df = df.copy()
    processed_df['game_date'] = pd.to_datetime(processed_df['date'])
    processed_df['game_datetime'] = pd.to_datetime(processed_df['date'] + ' ' + processed_df['time']).dt.tz_localize('US/Eastern').dt.tz_convert('UTC')
    
    # Drop rows containing All Star Game matchups
    processed_df = processed_df[~(processed_df['away_team'].isin(['American League', 'National League']) | 
                                processed_df['home_team'].isin(['American League', 'National League']))]
    
    processed_df['home_team_abbr'] = processed_df['home_team'].str.replace('St.Louis', 'St. Louis')
    processed_df['away_team_abbr'] = processed_df['away_team'].str.replace('St.Louis', 'St. Louis')
    
    # Get unique team names
    teams = pd.unique(processed_df['away_team_abbr'].tolist() + processed_df['home_team_abbr'].tolist())

    # Create mapping of team names to IDs
    team_mapping = {}
    for team in teams:
        team_info = statsapi.lookup_team(team)
        if team_info:
            team_mapping[team] = team_info[0]['id']
        else:
            team_mapping[team] = None

    # Map team names to IDs in processed_df
    processed_df['home_team'] = processed_df['home_team_abbr'].map(team_mapping)
    processed_df['away_team'] = processed_df['away_team_abbr'].map(team_mapping)
    
    # Convert odds columns - replace + with empty string and convert to numeric
    processed_df['away_odds'] = pd.to_numeric(processed_df['away_odds'].str.replace('+', ''))
    processed_df['home_odds'] = pd.to_numeric(processed_df['home_odds'].str.replace('+', ''))

    # Convert score columns to numeric
    processed_df['away_score'] = pd.to_numeric(processed_df['away_score'])
    processed_df['home_score'] = pd.to_numeric(processed_df['home_score'])
    processed_df.dropna(subset=['home_score','away_score'], inplace=True)
    
    return processed_df[['game_date','game_datetime','home_team','away_team','home_odds','away_odds',
                        'home_score','away_score','home_team_abbr','away_team_abbr']] 