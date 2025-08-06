# DESIGN OVERVIEW: Dynasty Oracle

## Project Structure

- `scripts/data_fetcher.py`: Main ETL script. Fetches, merges, and outputs dynasty market data from Sleeper and KeepTradeCut (KTC).
- `scripts/requirements.txt`: Python dependencies for the ETL pipeline.
- `data_outputs/`: Contains output CSVs (`dynasty_market_data.csv`, `sleeper_raw.csv`, `ktc_raw.csv`).
- `knowledge_base/`: Dynasty strategy and analytics notes.
- `.gitignore`: Excludes venv, data outputs, and other non-source files from git.
- `README.md` and `QUICKSTART.md`: Setup and usage instructions.

## Data Flow

1. **Fetch Sleeper Data**: Pulls all NFL player data from the Sleeper API.
2. **Fetch KTC Data**: Uses Selenium to scrape and parse KTC dynasty rankings.
3. **Normalize & Merge**: Player names are normalized for robust merging.
4. **Output**: Merged and raw data are saved to `data_outputs/`.

## Maintenance
- Only the `scripts/` directory should contain code.
- Remove any legacy or duplicate directories (e.g., `dynasty_gemini_project/`).
- All documentation should reflect the current structure and workflow.

---
For setup and usage, see `README.md` and `QUICKSTART.md`.
