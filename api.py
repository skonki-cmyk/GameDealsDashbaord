import requests

API_URL = "https://www.cheapshark.com/api/1.0/deals"

HEADERS = {
    "User-Agent": "GameDealsDashboard/1.0 (student project)"
}


def fetch_deals():

    try:

        response = requests.get(
            API_URL,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        deals = response.json()

        return deals

    except requests.exceptions.RequestException as e:

        print("Error fetching deals:")
        print(e)

        return []


if __name__ == "__main__":

    deals = fetch_deals()

    print("Total deals:", len(deals))

    if deals:
        print("\nFirst Deal:\n")
        print(deals[0])