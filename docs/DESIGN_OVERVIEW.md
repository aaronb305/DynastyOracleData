# DESIGN OVERVIEW: Dynasty Oracle

## Project Structure

- `scripts/data_fetcher.py`: Main ETL script. Fetches, merges, and outputs dynasty market data from Sleeper and KeepTradeCut (KTC).
- `scripts/data_fetcher_for_gem.py`: Stateless tool for fetching and merging dynasty market data for direct use in AI systems (outputs CSV to stdout).
- `core/data_fetcher_core.py`: Shared logic for fetching, cleaning, and merging dynasty market data. Used by both file-based and stateless implementations.
- `tests/test_data_fetcher_core.py`: Automated tests for all shared core logic (pytest, includes mocks for network/Selenium).
- `scripts/requirements.txt`: Python dependencies for the ETL pipeline.
- `data_outputs/`: Contains output CSVs (`dynasty_market_data.csv`, `sleeper_raw.csv`, `ktc_raw.csv`).
- `knowledge_base/`: Dynasty strategy and analytics notes.
- `mcp_server/`: Flask application for LLM tool integration, exposing data via a web endpoint.
- `.gitignore`: Excludes venv, data outputs, and other non-source files from git.
- `README.md`, `CLAUDE.md`, `GEMINI.md`, and `docs/QUICKSTART.md`: Setup and usage instructions, and LLM-specific guidance.

## Data Flow

1. **Fetch Sleeper Data**: Pulls all NFL player data from the Sleeper API (via core package).
2. **Fetch KTC Data**: Uses Selenium to scrape and parse KTC dynasty rankings (via core package).
3. **Normalize & Merge**: Player names are normalized and data is merged using shared logic in `core/data_fetcher_core.py`.
4. **Output/Access**:
   - `data_fetcher.py`: Saves merged and raw data to `data_outputs/`.
   - `data_fetcher_for_gem.py`: Prints merged data as a CSV string to stdout for direct LLM consumption.
   - `mcp_server/main.py`: Exposes the merged data as a CSV string via an HTTP endpoint.

## Maintenance
- All shared logic is in `core/` for easy reuse and testing.
- Only the `scripts/` directory should contain executable scripts for direct execution.
- The `mcp_server/` directory contains the web server implementation.
- All documentation reflects the current structure and workflow.
- All core logic is covered by automated tests in `tests/test_data_fetcher_core.py`.

---
For setup and usage, see `README.md` and `docs/QUICKSTART.md`.
