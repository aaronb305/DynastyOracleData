# Dynasty Oracle Project

## Setup Instructions

### 1. Create and Activate Virtual Environment

Open a terminal in the project root and run:

```
python -m venv venv
```

Activate the virtual environment:
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

### 2. Install Requirements

With the venv activated, run:
```
pip install -r scripts/requirements.txt
```

### 3. Run the Data Fetcher Script

With the venv activated, run:
```
python scripts/data_fetcher.py
```

This will fetch, merge, and output dynasty market data to `data_outputs/dynasty_market_data.csv`.

### 4. Deactivate the Virtual Environment

When you are done, deactivate the virtual environment:
- **All platforms:**
  ```
  deactivate
  ```

---

For troubleshooting or more details, see `QUICKSTART.md`.
