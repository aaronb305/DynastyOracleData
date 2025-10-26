# GEMINI.md

This file provides guidance to Gemini Code (gemini.ai/code) when working with code in this repository.

## Project Overview

Dynasty Oracle is a Python-based ETL pipeline that fetches, cleans, and merges dynasty fantasy football market data from multiple sources (Sleeper API and KeepTradeCut). The project supports both file-based output and stateless DataFrame returns for AI system integration.

## Common Commands

### Environment Setup
```bash
# Activate virtual environment (required for all commands below)
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows cmd:
.\venv\Scripts\activate.bat

# Unix/macOS:
source venv/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt
```

### Running Scripts
```bash
# Fetch data and write to files (outputs to data_outputs/)
python scripts/data_fetcher.py

# Stateless fetch (returns DataFrame, no file output)
python scripts/data_fetcher_for_gem.py
```

### Testing
```bash
# Run all tests
pytest tests/test_data_fetcher_core.py

# Run specific test
pytest tests/test_data_fetcher_core.py::test_normalize_name_basic

# Run tests with verbose output
pytest tests/test_data_fetcher_core.py -v
```

## Architecture

### Core Design Pattern
The project follows a **shared core logic** architecture to avoid duplication:

- **`core/data_fetcher_core.py`**: All shared fetching, cleaning, and merging logic
  - `normalize_name()`: Standardizes player names for cross-source matching
  - `fetch_sleeper_players()`: Fetches from Sleeper API
  - `fetch_ktc_player_data()`: Scrapes KeepTradeCut rankings via Selenium
  - `clean_and_merge_data()`: Deduplicates, filters positions (QB/RB/WR/TE), and merges datasets

- **`scripts/data_fetcher.py`**: File-based implementation (writes CSVs to `data_outputs/`)
- **`scripts/data_fetcher_for_gem.py`**: Stateless implementation (returns DataFrame for AI systems)

Both scripts import and use the same core functions to ensure consistent behavior.

### Data Flow
1. Fetch Sleeper player data (REST API)
2. Fetch KTC rankings (Selenium web scraping)
3. Normalize player names (remove suffixes, punctuation, lowercase)
4. Filter to relevant positions (QB, RB, WR, TE)
5. Deduplicate by normalized name
6. Merge datasets (left join from KTC to Sleeper)
7. Output merged data (file or DataFrame)

### Testing Strategy
All core logic is unit tested in `tests/test_data_fetcher_core.py` using pytest with mocked network/Selenium calls to ensure reliability and speed.

## Key Implementation Details

### Name Normalization
Player names are normalized using `normalize_name()` to handle variations across data sources:
- Removes suffixes (Jr, Sr, II, III, IV, V)
- Removes punctuation
- Converts to lowercase
- Normalizes whitespace

### Data Merging
- KTC data is the primary dataset (left side of merge)
- Sleeper data is joined on normalized name
- Only KTC fields not present in Sleeper are added
- Final output prioritizes KTC fields, then Sleeper fields
- Results are filtered to QB/RB/WR/TE only

### Selenium Usage
KTC scraping uses headless Chrome with these options:
- `--headless`: No GUI
- `--disable-gpu`: Improved stability
- `--no-sandbox`: Required for some environments
- WebDriverWait for dynamic content loading

## Directory Structure
- `core/`: Shared business logic
- `scripts/`: Executable ETL scripts
- `tests/`: pytest test suite
- `data_outputs/`: Generated CSV files (gitignored)
- `knowledge_base/`: Dynasty strategy documentation for AI systems
- `docs/`: Project documentation

## Important Notes

### When Adding New Features
- Add shared logic to `core/data_fetcher_core.py`
- Update both script implementations if needed
- Add tests to `tests/test_data_fetcher_core.py`
- Use mocks for network/Selenium calls in tests

### Data Sources
- **Sleeper API**: https://api.sleeper.app/v1/players/nfl (REST)
- **KeepTradeCut**: https://keeptradecut.com/dynasty-rankings (Selenium scraping)

### Dependencies
Core dependencies are in `scripts/requirements.txt`:
- pandas: Data manipulation
- requests: Sleeper API calls
- beautifulsoup4: HTML parsing
- selenium: KTC web scraping
- webdriver-manager: Chrome driver management

## Document Maintenance

This document is a living document. Any changes in the project structure, core logic, or important operational details should be reflected and updated in this document to ensure its continued accuracy and usefulness.

## LLM Tool Integration

### `get_dynasty_market_data` Tool

The `scripts/data_fetcher_for_gem.py` script is designed to act as a stateless tool for LLMs to retrieve up-to-date dynasty fantasy football market data.

**Purpose:** Fetches, cleans, and merges player data from the Sleeper API and KeepTradeCut rankings, returning the result as a CSV string. This provides LLMs with a current knowledge base of player values.

**Invocation (Shell Command):**
LLMs should execute the following shell command to run the tool:
```bash
.\venv\Scripts\activate.bat && python scripts/data_fetcher_for_gem.py
```
(For Unix/macOS environments, use `source venv/bin/activate` instead of `.\venv\Scripts\activate.bat`).

**Output:** The tool prints the merged and cleaned dynasty market data as a CSV string to standard output. LLMs should capture and parse this output.

**Prerequisites:**
- Python installed on the system.
- Virtual environment (`venv`) activated.
- All dependencies from `scripts/requirements.txt` installed.
- Chrome browser installed (for Selenium web scraping).

**Example LLM Tool Definition (Conceptual):**
```json
{
  "name": "get_dynasty_market_data",
  "description": "Fetches current dynasty fantasy football market data (Sleeper API & KeepTradeCut) and returns it as a CSV string.",
  "command": ".\\venv\\Scripts\\activate.bat && python scripts/data_fetcher_for_gem.py",
  "output_format": "csv"
}
```
