# QUICKSTART: Dynasty Oracle

## 1. Environment Setup

- Ensure Python 3.12+ is installed and available in your PATH.
- (Recommended) Use a virtual environment for isolation.

### Create and Activate venv

#### Create the Virtual Environment (only required once)
If you have not already created a virtual environment, run:
```
python -m venv venv
```

#### Activate the Virtual Environment (required for every new terminal session)
Activate the venv before running any project commands:
- **Windows (PowerShell):**
  ```
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (cmd):**
  ```
  .\venv\Scripts\activate.bat
  ```
- **Unix/macOS:**
  ```
  source venv/bin/activate
  ```

## 2. Install Dependencies
```
pip install -r scripts/requirements.txt
```


## 3. Run the ETL Script (File Output)
```
python scripts/data_fetcher.py
```
- Output: `data_outputs/dynasty_market_data.csv`
- Raw data: `data_outputs/sleeper_raw.csv`, `data_outputs/ktc_raw.csv`

## 4. Use the Stateless Data Fetcher (for LLMs/AI Systems)

For direct integration with AI systems or other Python tools that can execute shell commands and parse CSV output, use:
```bash
.\venv\Scripts\activate.bat && python scripts/data_fetcher_for_gem.py
```
(For Unix/macOS environments, use `source venv/bin/activate` instead of `.\venv\Scripts\activate.bat`).

This command executes the script, which prints the merged dynasty market data as a CSV string to standard output.

## 5. Run the MCP Server (Flask Application)

For integration with LLMs or applications that prefer a web API, you can run the Flask-based MCP server.

1.  Activate the virtual environment:
    *   Windows: `.\venv\Scripts\activate.bat`
    *   Unix/macOS: `source venv/bin/activate`
2.  Install server dependencies (if not already installed):
    `pip install -r mcp_server/requirements.txt`
3.  Start the Flask development server from the project root directory:
    `python mcp_server/main.py`

Once running, you can access the data via `http://127.0.0.1:5000/dynasty_data`.

## 6. Run and Maintain Tests

Automated tests for all core logic are provided in:
```
tests/test_data_fetcher_core.py
```
Tests use `pytest` and include:
- Name normalization
- Data cleaning and merging
- Mocked network and Selenium fetches

To run all tests:
```
pytest tests/test_data_fetcher_core.py
```

## 7. Deactivate the Virtual Environment

When finished, deactivate the venv:
```
deactivate
```

---
For more details, see `README.md`.
