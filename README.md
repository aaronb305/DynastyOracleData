# Dynasty Oracle Project

## Setup Instructions

### 1. Create and Activate Virtual Environment


#### 1.1 Create the Virtual Environment (only required once)
If you have not already created a virtual environment, run:
```
python -m venv venv
```

#### 1.2 Activate the Virtual Environment (required for every new terminal session)
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
