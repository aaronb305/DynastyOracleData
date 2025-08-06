"""
data_fetcher.py

This script fetches and merges dynasty fantasy football data from multiple sources:
- Sleeper API: Player info (name, team, age, position, player ID)
- KeepTradeCut (KTC): Superflex dynasty trade values
- OverTheCap: Contract info (Contract End Year, 2026 Cap Hit, Potential Out Year)

The final merged dataset is saved as 'dynasty_market_data.csv' in the data_outputs/ directory.

Author: Dynasty Oracle
Date: August 7, 2025
"""

import requests
import pandas as pd
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os

# ---------------------------
# Utility Functions
# ---------------------------

def normalize_name(name):
    """
    Normalize player names for merging across sources.
    Removes suffixes, punctuation, and converts to lowercase.
    """
    name = re.sub(r'[^a-zA-Z\s]', '', name)  # Remove punctuation
    name = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', name, flags=re.IGNORECASE)  # Remove suffixes
    name = re.sub(r'\s+', ' ', name).strip()  # Remove extra spaces
    return name.lower()

# ---------------------------
# Sleeper API Fetch
# ---------------------------

def get_sleeper_players():
    """
    Fetch all NFL players from Sleeper API (full response).
    Returns a DataFrame with all available fields for each player.
    """
    print("Fetching player data from Sleeper API...")
    url = "https://api.sleeper.app/v1/players/nfl"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    # Convert the full response to a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    print(f"  -> Retrieved {len(df)} players from Sleeper (full data). Columns: {list(df.columns)}")
    return df

# ---------------------------
# KeepTradeCut Scraper
# ---------------------------

def get_ktc_player_data():
    """
    Fetches the latest player rankings directly from KeepTradeCut's internal data source.
    
    Returns:
        A pandas DataFrame containing the player rankings, or None if the request fails.
    """
    print("[DEBUG] Entered get_ktc_player_data()")
    import traceback
    print("[DEBUG] Before Selenium driver creation")
    driver = None
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Disable headless for debugging
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-dev-shm-usage')
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        print("[DEBUG] After Selenium driver creation")
    except Exception as e:
        print("[ERROR] Exception during Selenium driver creation:")
        traceback.print_exc()
        return pd.DataFrame([])
    # Use Selenium to render JavaScript and extract all player data fields from KTC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    base_url = "https://keeptradecut.com/dynasty-rankings/?page={}"
    players = []
    page = 0
    if driver is None:
        print("[ERROR] Selenium driver was not created.")
        return pd.DataFrame([])
    try:
        while True:
            url = base_url.format(page)
            print(f"Fetching KTC dynasty rankings page {page} (Selenium)...")
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                print("Timeout: Page did not load.")
                break
            time.sleep(2)
            page_source = driver.page_source
            import json, re
            soup = BeautifulSoup(page_source, "html.parser")
            # Try to find a <script> tag with a player array or JSON blob
            script_tags = soup.find_all('script')
            found_json = None
            for idx, script in enumerate(script_tags):
                if script.string and 'playersArray' in script.string:
                    print(f"\n[DEBUG] <script> tag #{idx} containing 'playersArray':\n{script.string[:500]}\n---END SCRIPT---\n")
                    # Extract the playersArray JS assignment
                    match = re.search(r'playersArray\s*=\s*(\[.*?\]);', script.string, re.DOTALL)
                    if match:
                        json_blob = match.group(1)
                        try:
                            # Unescape unicode and parse JSON
                            found_json = json.loads(json_blob)
                            print(f"[DEBUG] Extracted playersArray with {len(found_json)} players.")
                            break
                        except Exception as e:
                            print(f"[ERROR] Failed to parse playersArray JSON: {e}")
                            continue
            if found_json:
                print(f"[DEBUG] Found {len(found_json)} players in JSON array.")
                df_cleaned = pd.DataFrame(found_json)
                return df_cleaned
            # Fallback to previous HTML scraping if no JSON found
            rankings_div = soup.find('div', id='rankings-page-rankings')
            if rankings_div:
                print(f"[FOUND] rankings-page-rankings div found on page {page}.")
                player_blocks = rankings_div.find_all('div', class_='player-name-wrapper')
                for block in player_blocks:
                    name_tag = block.find('p', class_='player-name')
                    details_tag = block.find_next_sibling('p', class_='player-details')
                    name = name_tag.get_text(strip=True) if name_tag else None
                    details = details_tag.get_text(strip=True) if details_tag else None
                    position, team, age, height = None, None, None, None
                    if details and details != "RDP":
                        parts = [p.strip() for p in details.split('–')]
                        if len(parts) >= 4:
                            position = parts[0]
                            team = parts[1]
                            age = parts[2].replace('y.o.', '').strip()
                            height = parts[3]
                        elif len(parts) == 3:
                            position = parts[0]
                            team = parts[1]
                            age = parts[2].replace('y.o.', '').strip()
                        elif len(parts) == 2:
                            position = parts[0]
                            team = parts[1]
                        elif len(parts) == 1:
                            position = parts[0]
                    value = None
                    parent = block.parent
                    value_tag = None
                    for cls in ['ktc-player-value', 'value', 'ktc-value', 'player-value']:
                        value_tag = parent.find(class_=cls) if parent else None
                        if value_tag:
                            break
                    if not value_tag and parent:
                        for sib in parent.find_all(['span', 'div'], recursive=False):
                            txt = sib.get_text(strip=True)
                            if txt.isdigit():
                                value_tag = sib
                                break
                    if value_tag:
                        value = value_tag.get_text(strip=True)
                    players.append({
                        'name': name,
                        'details': details,
                        'position': position,
                        'team': team,
                        'age': age,
                        'height': height,
                        'value': value
                    })
            else:
                print(f"[NOT FOUND] rankings-page-rankings div NOT found on page {page}.")
            break
    finally:
        driver.quit()
    df_cleaned = pd.DataFrame(players)
    if df_cleaned.empty:
        print("Could not extract player data from KTC pages. The page structure may have changed.")
        return None
    return df_cleaned



# ---------------------------
# Main Function
# ---------------------------

def main():
    print("[DEBUG] Entered main()")
    """
    Fetches, merges, and saves dynasty market data.
    """

    sleeper_df = get_sleeper_players()
    ktc_df = get_ktc_player_data()

    if ktc_df is None:
        print("\nERROR: Failed to fetch KeepTradeCut data. The KTC API may be down or blocking requests. Exiting.")
        return

    # For now, just print the shape and columns of both dataframes for analysis
    print("\n[SLEEPER DF] shape:", sleeper_df.shape, "columns:", list(sleeper_df.columns))
    print("[KTC DF] shape:", ktc_df.shape, "columns:", list(ktc_df.columns))

    # TODO: Analyze and update merging/cleaning logic after confirming data

    # Save raw data for inspection
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sleeper_out = os.path.join(script_dir, '..', 'data_outputs', 'sleeper_raw.csv')
    ktc_out = os.path.join(script_dir, '..', 'data_outputs', 'ktc_raw.csv')
    os.makedirs(os.path.dirname(sleeper_out), exist_ok=True)
    sleeper_df.to_csv(sleeper_out, index=False)
    ktc_df.to_csv(ktc_out, index=False)
    print(f"\nRaw Sleeper data saved to {sleeper_out}")
    print(f"Raw KTC data saved to {ktc_out}")

if __name__ == "__main__":
    main()
