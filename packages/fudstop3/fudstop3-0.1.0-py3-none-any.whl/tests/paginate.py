import asyncio
import aiohttp
import json
from urllib.parse import urlencode

API_KEY = "354IrMn2tL7naiFNxKDCHfhZoTcnf3Ip"
BASE_URL = "https://api.polygon.io/v3/snapshot"

async def fetch_page(session, url):
    """Fetch one page of data from the Polygon.io API."""
    # Append the API key as a query parameter using urlencode
    query_params = {"apiKey": API_KEY}
    url_with_api_key = f"{url}&{urlencode(query_params)}"

    async with session.get(url_with_api_key) as response:
        response.raise_for_status()
        data = await response.json()
        return data
async def paginate_snapshots(session, initial_url):
    """
    Paginate through all pages starting from initial_url.
    Collect and return all option snapshots in a single list.
    """
    all_results = []
    url = initial_url
    
    while url:
        print(f"Fetching: {url}")
        data = await fetch_page(session, url)

        # Collect results from this page
        results = data.get("results", [])
        all_results.extend(results)

        # Prepare for the next iteration
        url = data.get("next_url")  # If this is None or missing, the loop ends
    
    return all_results

async def main():
    # Build the initial URL
    initial_url = f"{BASE_URL}?type=options&limit=250&apiKey={API_KEY}"

    async with aiohttp.ClientSession() as session:
        # Fetch all pages
        all_options = await paginate_snapshots(session, initial_url)

    print(f"Total options retrieved: {len(all_options)}")

    # Example: Write out to a JSON file
    with open("polygon_options.json", "w") as f:
        json.dump(all_options, f, indent=2)
    print("Saved all options to polygon_options.json")

if __name__ == "__main__":
    asyncio.run(main())
