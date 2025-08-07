###############################################################
# data_fetcher.py
#
# Script to fetch, clean, and merge dynasty fantasy football data from multiple sources and write outputs to files.
# Uses shared logic from core/data_fetcher_core.py.
#
# Author: Dynasty Oracle
# Date: August 6, 2025
###############################################################



import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.data_fetcher_core import fetch_sleeper_players, fetch_ktc_player_data, clean_and_merge_data


def main():
    print("[DEBUG] Entered main()")

    # Fetch data using shared core logic
    sleeper_df = fetch_sleeper_players()

    ktc_df = fetch_ktc_player_data()

    if ktc_df is None:
        print("\nERROR: Failed to fetch KeepTradeCut data. The KTC API may be down or blocking requests. Exiting.")
        return

    # Clean and merge using shared core logic
    merged = clean_and_merge_data(sleeper_df, ktc_df)

    # Save outputs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, '..', 'data_outputs', 'dynasty_market_data.csv')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    merged.to_csv(out_path, index=False)
    print(f"\nMerged dynasty market data saved to {out_path}")

    # Save raw data for inspection
    sleeper_out = os.path.join(script_dir, '..', 'data_outputs', 'sleeper_raw.csv')
    ktc_out = os.path.join(script_dir, '..', 'data_outputs', 'ktc_raw.csv')
    sleeper_df.to_csv(sleeper_out, index=False)
    ktc_df.to_csv(ktc_out, index=False)
    print(f"Raw Sleeper data saved to {sleeper_out}")
    print(f"Raw KTC data saved to {ktc_out}")


if __name__ == "__main__":
    main()
