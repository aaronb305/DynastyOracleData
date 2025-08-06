# QUICKSTART: Dynasty Oracle

## 1. Environment Setup

- Ensure Python 3.12+ is installed and available in your PATH.
- (Recommended) Use a virtual environment for isolation.

### Create and Activate venv
```
python -m venv venv
```
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

## 3. Run the ETL Script
```
python scripts/data_fetcher.py
```
- Output: `data_outputs/dynasty_market_data.csv`
- Raw data: `data_outputs/sleeper_raw.csv`, `data_outputs/ktc_raw.csv`

## 4. Troubleshooting

- If you see errors about missing modules, ensure your venv is activated and requirements are installed.
- If you have issues with Selenium or ChromeDriver, ensure Chrome is installed and up to date.

## 5. Deactivate the Virtual Environment

When finished, deactivate the venv:
```
deactivate
```

---
For more details, see `README.md`.
