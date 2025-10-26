###############################################################
# core/data_fetcher_core.py
#
# Shared logic for fetching, cleaning, and merging dynasty fantasy football market data.
#
# Provides stateless utility functions for:
#   - Normalizing player names
#   - Fetching player data from Sleeper API
#   - Fetching player rankings from KeepTradeCut (KTC)
#   - Cleaning and merging data from both sources
#
# Used by both file-based (data_fetcher.py) and stateless (data_fetcher_for_gem.py) scripts.
#
# Author: Dynasty Oracle
# Date: August 6, 2025
###############################################################


import requests
import pandas as pd
import re
import time
from bs4 import BeautifulSoup
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def normalize_name(name: str) -> str:
    # Normalize player names for merging across sources.
    # Removes suffixes, punctuation, and converts to lowercase.

    if not isinstance(name, str):
        return ''

    name = re.sub(r'[^a-zA-Z\s]', '', name)
    name = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()
    return name.lower()


def fetch_sleeper_players() -> pd.DataFrame:
    # Fetch all NFL players from Sleeper API.
    # Returns a DataFrame with all available fields for each player.

    url = "https://api.sleeper.app/v1/players/nfl"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame.from_dict(data, orient='index')
    return df


def fetch_ktc_player_data() -> Optional[pd.DataFrame]:
    # Fetches the latest player rankings from KeepTradeCut using Selenium.
    # Returns a DataFrame containing player rankings, or None if fetch fails.

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = None

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception:
        return None

    base_url = "https://keeptradecut.com/dynasty-rankings/?page={}"
    players = []
    page = 0

    try:
        while True:
            url = base_url.format(page)
            driver.get(url)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                break

            time.sleep(2)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            script_tags = soup.find_all('script')
            found_json = None

            for script in script_tags:
                if script.string and 'playersArray' in script.string:
                    match = re.search(r'playersArray\s*=\s*(\[.*?\]);', script.string, re.DOTALL)
                    if match:
                        json_blob = match.group(1)
                        try:
                            import json
                            found_json = json.loads(json_blob)
                            break
                        except Exception:
                            continue

            if found_json:
                df_cleaned = pd.DataFrame(found_json)
                return df_cleaned

            rankings_div = soup.find('div', id='rankings-page-rankings')
            if rankings_div:
                player_blocks = rankings_div.find_all('div', class_='player-name-wrapper')
                for block in player_blocks:
                    name_tag = block.find('p', class_='player-name')
                    details_tag = block.find_next_sibling('p', class_='player-details')
                    name = name_tag.get_text(strip=True) if name_tag else None
                    details = details_tag.get_text(strip=True) if details_tag else None
                    position, team, age, height = None, None, None, None

                    if details and details != "RDP":
                        parts = [p.strip() for p in details.split('')]
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
                break
            break

    finally:
        if driver:
            driver.quit()

    df_cleaned = pd.DataFrame(players)
    if df_cleaned.empty:
        return None

    return df_cleaned


def clean_and_merge_data(sleeper_df: pd.DataFrame, ktc_df: pd.DataFrame) -> pd.DataFrame:
    # Cleans and merges Sleeper and KTC dataframes for dynasty market analysis.
    # Returns merged DataFrame for QB, RB, WR, TE only.

    # Data Cleaning: Sleeper
    if 'full_name' in sleeper_df.columns:
        sleeper_df['norm_name'] = sleeper_df['full_name'].apply(normalize_name)
    elif 'player_id' in sleeper_df.columns:
        sleeper_df['norm_name'] = sleeper_df['player_id'].astype(str)
    else:
        raise ValueError("Sleeper DataFrame missing both 'full_name' and 'player_id' columns.")

    valid_positions = {'QB', 'RB', 'WR', 'TE'}
    sleeper_df = sleeper_df[sleeper_df['position'].isin(valid_positions)]
    sleeper_df = sleeper_df.drop_duplicates(subset=['norm_name'])

    # Data Cleaning: KTC
    if 'playerName' in ktc_df.columns:
        ktc_df['norm_name'] = ktc_df['playerName'].apply(normalize_name)
    elif 'name' in ktc_df.columns:
        ktc_df['norm_name'] = ktc_df['name'].apply(normalize_name)
    else:
        str_cols = [col for col in ktc_df.columns if ktc_df[col].dtype == object]
        if str_cols:
            ktc_df['norm_name'] = ktc_df[str_cols[0]].apply(normalize_name)
        else:
            raise ValueError("KTC DataFrame missing 'playerName', 'name', and any string columns for normalization.")

    # Filter sleeper_df to only include players present in ktc_df
    sleeper_df = sleeper_df[sleeper_df['norm_name'].isin(ktc_df['norm_name'])]

    if 'position' in ktc_df.columns:
        ktc_df = ktc_df[ktc_df['position'].isin(valid_positions)]
    ktc_df = ktc_df.drop_duplicates(subset=['norm_name'])

    # Merging
    ktc_fields = [c for c in ktc_df.columns if c not in sleeper_df.columns and c != 'norm_name']
    merge_fields = ktc_fields + ["norm_name"]
    ktc_merge_df = ktc_df[merge_fields]

    merged = pd.merge(
        ktc_merge_df,
        sleeper_df,
        how='left',
        left_on='norm_name',
        right_on='norm_name',
        suffixes=('_ktc', '_sleeper')
    )

    merged = merged.drop_duplicates(subset=['norm_name'])

    if 'position' in merged.columns:
        merged = merged[merged['position'].isin(valid_positions)]
    elif 'position_ktc' in merged.columns:
        merged = merged[merged['position_ktc'].isin(valid_positions)]

    cols_ktc = [c for c in ktc_fields if c in merged.columns]
    cols_sleeper = [c for c in sleeper_df.columns if c not in ('norm_name',) and c in merged.columns]
    col_order = cols_ktc + cols_sleeper + (['norm_name'] if 'norm_name' in merged.columns else [])
    merged = merged[col_order]

    return merged
