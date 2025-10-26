
"""
data_fetcher_for_gem.py

Stateless data fetching and cleaning tool for dynasty fantasy football market data.
This module provides a single function, `get_and_clean_data_for_gem`, which fetches player data from the Sleeper API and KeepTradeCut (KTC) rankings, cleans and merges the data, and returns the result as a pandas DataFrame. No files are written; all data is returned directly for use in AI systems or other integrations.

Author: Dynasty Oracle
Date: August 6, 2025
"""

###############################################################
# data_fetcher_for_gem.py
#
# Stateless data fetching and cleaning tool for dynasty fantasy football market data.
# Returns merged DataFrame for use in AI systems or integrations.
# Uses shared logic from core/data_fetcher_core.py.
#
# Author: Dynasty Oracle
# Date: August 6, 2025
###############################################################


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.data_fetcher_core import fetch_sleeper_players, fetch_ktc_player_data, clean_and_merge_data


def get_and_clean_data_for_gem():
    # Fetches, cleans, and merges dynasty market data from Sleeper and KeepTradeCut.
    # Returns:
    #   pd.DataFrame: Merged and cleaned dynasty market data for QB, RB, WR, TE.
    # Raises:
    #   ValueError: If required columns are missing or data fetch fails.

    sleeper_df = fetch_sleeper_players()

    ktc_df = fetch_ktc_player_data()

    if ktc_df is None or sleeper_df is None:
        raise ValueError("Failed to fetch data from Sleeper or KeepTradeCut.")

    merged = clean_and_merge_data(sleeper_df, ktc_df)

    return merged


def main():
    # Main function for stateless data fetcher (for direct use in AI systems)

    merged = get_and_clean_data_for_gem()

    return merged


if __name__ == "__main__":
    # If run as a script, just fetch and return the DataFrame (prints shape for confirmation)

    df = main()
    print(f"Merged dynasty market data shape: {df.shape}")
