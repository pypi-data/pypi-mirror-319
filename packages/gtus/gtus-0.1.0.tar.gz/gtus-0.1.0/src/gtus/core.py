# core.py

from pytrends.request import TrendReq
import pandas as pd
import time
import json
from requests.exceptions import RequestException
import asyncio
import aiohttp

class GTUS:
    def __init__(self, queries, states=None, timeframe='today 5-y', delay=5, gprop=''):
        self.pytrend = TrendReq()
        self.queries = queries
        self.states = states or [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]
        self.timeframe = timeframe
        self.delay = delay
        self.gprop = gprop
        self.all_data = {}

    def fetch_state_trends(self, query, state, max_retries=3, backoff_factor=1.5):
        for attempt in range(max_retries):
            try:
                self.pytrend.build_payload(
                    kw_list=[query],
                    timeframe=self.timeframe,
                    geo='US-' + state,
                    gprop=self.gprop
                )
                state_trends = self.pytrend.interest_over_time()
                return state_trends
            except RequestException as e:
                if attempt == max_retries - 1:
                    print(f"Error fetching data for query '{query}' in state '{state}': {e}")
                    return None
                wait_time = self.delay * (backoff_factor ** attempt)
                time.sleep(wait_time)
        return None

    def collect_all_trends(self):
        for state in self.states:
            state_data = {}
            for query in self.queries:
                result = self.fetch_state_trends(query, state)
                if result is not None and not result.empty:
                    state_data[query] = result
            self.all_data[state] = state_data

    def export_to_json(self, filename="google_trends_by_state.json"):
        json_data = {}
        for state, query_data in self.all_data.items():
            json_data[state] = {
                query: df.to_dict(orient='records')  # Convert DataFrame to JSON-serializable format
                for query, df in query_data.items()
                if not df.empty
            }

        # Convert keys to strings where necessary
        cleaned_data = {
            state: {query: [{k: (str(v) if isinstance(v, pd.Timestamp) else v) for k, v in row.items()} for row in data]
                    for query, data in queries.items()}
            for state, queries in json_data.items()
        }

        # Save to JSON
        with open(filename, 'w') as f:
            json.dump(cleaned_data, f, indent=4)
        print(f"Data exported to {filename}")

    def export_to_excel(self, filename="google_trends_by_state.xlsx"):
        with pd.ExcelWriter(filename) as writer:
            for state, query_data in self.all_data.items():
                # Combine all queries into a single DataFrame per state
                combined_data = pd.concat(
                    [df.rename(columns={query: query}) for query, df in query_data.items()], axis=1
                ).drop(columns=['isPartial'], errors='ignore')  # Remove 'isPartial' column
                combined_data.to_excel(writer, sheet_name=state[:31])
        print(f"Data exported to {filename}")

    def create_consolidated_dataframe(self):
        all_data = []
        for state, query_data in self.all_data.items():
            for query, df in query_data.items():
                if not df.empty:
                    df = df.drop(columns=['isPartial'], errors='ignore')  # Remove 'isPartial' column
                    df['State'] = state
                    df['Query'] = query
                    all_data.append(df.reset_index())
        
        return pd.concat(all_data, ignore_index=True)

class AsyncGTUS(GTUS):
    async def fetch_state_trends_async(self, query, state, session, max_retries=3, backoff_factor=1.5):
        for attempt in range(max_retries):
            try:
                payload = {
                    'hl': 'en-US',
                    'tz': 360,
                    'req': {
                        'comparisonItem': [
                            {
                                'geo': {'country': f'US-{state}'},
                                'time': self.timeframe,
                                'keyword': query
                            }
                        ],
                        'category': 0,
                        'property': self.gprop
                    }
                }
                async with session.post("https://trends.google.com/trends/api/widgetdata", json=payload) as response:
                    if response.status == 200:
                        return await response.json()
            except aiohttp.ClientError as e:
                if attempt == max_retries - 1:
                    print(f"Error fetching data for query '{query}' in state '{state}': {e}")
                    return None
                wait_time = self.delay * (backoff_factor ** attempt)
                await asyncio.sleep(wait_time)
        return None

    async def collect_all_trends_async(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for state in self.states:
                for query in self.queries:
                    tasks.append(self.fetch_state_trends_async(query, state, session))

            results = await asyncio.gather(*tasks)
            # Process results (left as an exercise to map results back into self.all_data)

# Example usage
if __name__ == "__main__":
    queries = ["telemedicine", "remote work"]
    states = ["CA", "NY"]

    gtus = GTUS(queries, states)
    gtus.collect_all_trends()
    gtus.export_to_json()
    gtus.export_to_excel()

    # Create a consolidated DataFrame
    consolidated_df = gtus.create_consolidated_dataframe()
    print(consolidated_df.head())
