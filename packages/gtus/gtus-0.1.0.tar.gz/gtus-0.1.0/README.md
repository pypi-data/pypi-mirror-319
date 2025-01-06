# GTUS - Google Trends for US States

`gtus`is a Python package that enables users to collect and analyze Google Trends data across various US states. This package is designed to handle multiple queries, manage API delays, and support exporting data to multiple formats, all while being user-friendly and versatile.

---

## Features

1. **Collect Google Trends Data:**
   - Fetch state-level data for multiple queries simultaneously.
   - Collect data for all US states or specific states.
   - Customize the timeframe for data collection.

2. **Error Handling and Retry Logic:**
   - Built-in retry mechanism with exponential backoff to handle rate-limiting errors (`Too Many Requests`).

3. **Data Export Options:**
   - Save data in Excel format, with each state’s data in separate sheets.
   - Export data to a JSON file.
   - Create a consolidated DataFrame for advanced analysis.

4. **Asynchronous Functionality:**
   - Collect data asynchronously for faster execution.

---

## Installation

Install GTUS via pip:

```bash
pip install gtus
```

---

## Getting Started

Here's how to start using gtus to collect Google Trends data.

## Usage Examples

### 1. Collect Data for All States

If no states are specified, GTUS will automatically collect data for all US states:

```python
from gtus import GTUS

queries = ["telemedicine", "remote work"]
# Initialize GTUS object without specifying states
gtus = GTUS(queries=queries, timeframe="2022-01-01 2023-01-01")

# Collect data
gtus.collect_all_trends()

# Export to Excel
gtus.export_to_excel("google_trends_all_states.xlsx")

# Export to JSON
gtus.export_to_json("google_trends_all_states.json")

# Create a consolidated DataFrame
dataframe = gtus.create_consolidated_dataframe()
print(dataframe.head())
```

### 2. Fetch Data for a Specific State and Query
You can specify a subset of states and queries:


```python
states = ["CA", "NY", "TX"]
queries = ["remote work", "telehealth"]

# Initialize GTUS object
gtus = GTUS(queries=queries, states=states, timeframe="2022-01-01 2023-01-01")

```

### 3. Asynchronous Data Collection

```python
from gtus import AsyncGTUS
import asyncio

async def fetch_async():
    queries = ["online learning", "work from home"]

    # Initialize AsyncGTUS object
    async_gtus = AsyncGTUS(queries=queries, timeframe="2022-01-01 2023-01-01")

    await async_gtus.collect_all_trends_async()

    # Export to Excel and JSON
    async_gtus.export_to_excel("async_google_trends.xlsx")
    async_gtus.export_to_json("async_google_trends.json")

asyncio.run(fetch_async())
```

### 4. Consolidated DataFrame

Combine all collected data into a single DataFrame:

```python
consolidated_df = gtus.create_consolidated_dataframe()
print(consolidated_df.head())
```

---

## Advanced Configuration

### Customize Timeframes
You can specify custom timeframes for data collection:

```python
gtus = GTUS(queries=["climate change"], states=["WA"], timeframe="2010-01-01 2020-12-31")
```

### Adjust Retry Settings

Customize retry attempts and delays for handling rate limits:

```python
gtus = GTUS(queries=["data science"], states=["NY"], delay=10)
result = gtus.fetch_state_trends(query="data science", state="NY", max_retries=5, backoff_factor=2)
```

---

## Dependencies

- `pandas`
- `pytrends`
- `aiohttp`

---

## Contributing

Contributions are welcome! Please submit issues or pull requests via [GitHub](https://github.com/leventbulut/gtus).

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

Start exploring Google Trends data with GTUS today!
