# Quickstart Guide: Dynasty Gemini Project

This guide will help you get up and running with the Dynasty Gemini Project in just a few steps.

## 1. Prerequisites
- Python 3.8 or newer
- pip (Python package manager)

## 2. Setup
1. **Navigate to the scripts directory:**
   ```
   cd dynasty_gemini_project/scripts
   ```
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## 3. Fetch the Latest Data
Run the data fetcher script to generate the latest dynasty market data:
```sh
python data_fetcher.py
```
- This will create `dynasty_market_data.csv` in the `data_outputs` folder.

## 4. Update Your Gemini Knowledge Base
1. Upload all files from the `knowledge_base` folder and the new `dynasty_market_data.csv` to your Gemini's knowledge base.
2. Copy the contents of `custom_instructions.txt` into the Gemini's instruction field.
3. Save and start a new chat to use the updated Dynasty Oracle expert.

---
For more details, see the README and DESIGN_OVERVIEW.md files.
