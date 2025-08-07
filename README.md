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


### 3. Run the Data Fetcher Script (File Output)

With the venv activated, run:
```
python scripts/data_fetcher.py
```

This will fetch, merge, and output dynasty market data to `data_outputs/dynasty_market_data.csv`.

### 4. Use the Stateless Data Fetcher (Direct DataFrame)

For direct integration with AI systems or other Python tools, use:
```
from scripts.data_fetcher_for_gem import get_and_clean_data_for_gem
df = get_and_clean_data_for_gem()
```

This returns the merged dynasty market data as a pandas DataFrame (no files written).



### 5. Run and Maintain Tests

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

### 6. Deactivate the Virtual Environment

When you are done, deactivate the virtual environment:
- **All platforms:**
  ```
  deactivate
  ```

---


---

## Integrating with Custom GPT/GEM/AI Models

You can use Dynasty Oracle data and logic to power custom AI agents, including GPT, GEM, or other LLM-based systems.

### Agent Setup
- Use the contents of `custom_instructions.txt` as the system prompt or instructions when configuring your agent.
- This ensures the agent understands the domain, workflow, and best practices for dynasty fantasy football analysis.

### Building the Knowledge Base
- Include all files from the `knowledge_base/` directory for strategy, analytics, and key metrics.
- Add actual dynasty market data for richer context:
  - **Recommended:** Use the import code option in your AI platform and call `get_and_clean_data_for_gem()` from `scripts/data_fetcher_for_gem.py` to fetch and clean the latest data as a pandas DataFrame.
  - **Alternative:** Upload the latest `data_outputs/dynasty_market_data.csv` directly to your knowledge base if code import is not available.

### Example: Importing Data for AI Agent
```python
from scripts.data_fetcher_for_gem import get_and_clean_data_for_gem
df = get_and_clean_data_for_gem()
# Use df as context for your agent, or export to CSV for upload
```

### Notes
- Always keep your knowledge base up to date by re-running the data fetcher before major analysis or training.
- For best results, combine strategy files, analytics, and fresh market data.

For troubleshooting or more details, see `QUICKSTART.md`.
