# Design Overview: Dynasty Gemini Project

## Purpose
The Dynasty Gemini Project is designed to provide a robust, updatable knowledge base for a custom Gemini AI focused on dynasty fantasy football. It combines dynamic player/contract data with strategic knowledge and clear instructions for optimal LLM performance.

## Key Components
- **scripts/data_fetcher.py**: Python script that fetches, normalizes, and merges player, value, and contract data from Sleeper, KeepTradeCut, and OverTheCap. The output is a single CSV for use as the Gemini's primary data source.
- **knowledge_base/**: Contains four foundational articles on dynasty strategy and analytics, providing context and best practices for the Gemini's responses.
- **custom_instructions.txt**: Defines the Gemini's persona, directives, and how it should use the data and knowledge base.
- **data_outputs/**: Stores the generated `dynasty_market_data.csv` file.

## Data Flow
1. **Fetch**: The script pulls the latest data from public APIs and web sources.
2. **Normalize**: Player names are normalized to ensure accurate merging across sources.
3. **Merge**: DataFrames from each source are merged on normalized names.
4. **Output**: The merged DataFrame is saved as a CSV for upload to Gemini.

## Update Workflow
- Run the script regularly to keep data current.
- Upload the new CSV and knowledge articles to Gemini.
- Update the instructions as needed.

## Extensibility
- The modular design allows for easy addition of new data sources or knowledge articles.
- The normalization logic can be updated to handle new edge cases as needed.

## Best Practices
- Always check for data source changes (API or HTML structure) if the script fails.
- Review the knowledge articles annually to ensure strategic advice remains current.

---
For setup and usage, see QUICKSTART.md and README.md.
