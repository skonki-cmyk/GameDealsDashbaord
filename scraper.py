from api import fetch_deals
from database import create_table, insert_game, delete

USD_TO_INR = 87.30

STORES = {
    "1": "Steam",
    "2": "GamersGate",
    "3": "Green Man Gaming",
    "7": "GOG",
    "11": "Humble Bundle",
    "25": "Epic Games"
}


def populate_database():

    create_table()

    delete()

    deals = fetch_deals()

    if not deals:
        print("No deals found.")
        return

    for deal in deals:

        title = deal.get("title", "Unknown")

        store = STORES.get(
            deal.get("storeID"),
            "Other"
        )

        original_price = float(
            deal.get("normalPrice", 0)
        )

        deal_price = float(
            deal.get("salePrice", 0)
        )

        currency = "USD"

        deal_price_inr = round(
            deal_price * USD_TO_INR,
            2
        )

        discount = round(
            float(deal.get("savings", 0)),
            2
        )

        rating = int(
            deal.get("steamRatingPercent") or 0
        )

        image = deal.get("thumb", "")

        url = (
            "https://www.cheapshark.com/redirect?dealID="
            + deal.get("dealID", "")
        )

        insert_game(
            title,
            store,
            original_price,
            deal_price,
            currency,
            deal_price_inr,
            discount,
            rating,
            image,
            url
        )

    print("--------------------------------")
    print("Database populated successfully!")
    print("Games inserted:", len(deals))
    print("--------------------------------")


if __name__ == "__main__":
    populate_database()