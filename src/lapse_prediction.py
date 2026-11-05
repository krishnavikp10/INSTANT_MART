
import os
import csv
from datetime import datetime
from collections import defaultdict

CUSTOMERS_FILE = "data/clean/customers.csv"
ORDERS_FILE = "data/clean/orders.csv"
OUTPUT_FILE = "output/lapse_predictions.csv"

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S"
]


def parse_date(value):
    if not value:
        return None

    value = value.strip()

    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        ).replace(tzinfo=None)
    except ValueError:
        return None


def predict_lapse():

    if not os.path.exists(CUSTOMERS_FILE):
        print("Error: Customers dataset not found.")
        return

    if not os.path.exists(ORDERS_FILE):
        print("Error: Orders dataset not found.")
        return

    with open(CUSTOMERS_FILE, newline="", encoding="utf-8-sig") as file:
        customers = list(csv.DictReader(file))

    with open(ORDERS_FILE, newline="", encoding="utf-8-sig") as file:
        orders = list(csv.DictReader(file))

    customer_orders = defaultdict(list)

    for order in orders:

        if order["status"].strip().lower() != "completed":
            continue

        order_date = parse_date(order.get("order_ts", ""))

        if order_date:
            customer_orders[order["customer_id"]].append(order_date)

    all_dates = [
        date
        for dates in customer_orders.values()
        for date in dates
    ]

    if not all_dates:
        print("No valid completed order dates found.")
        return

    reference_date = max(all_dates)

    results = []

    for customer in customers:

        customer_id = customer["customer_id"]
        dates = customer_orders.get(customer_id, [])

        if not dates:
            results.append({
                "customer_id": customer_id,
                "last_purchase_date": "No completed purchase",
                "days_inactive": "",
                "lapse_risk": "No Purchase"
            })
            continue

        last_purchase = max(dates)
        days_inactive = (reference_date - last_purchase).days

        if days_inactive >= 60:
            risk = "High"
        elif days_inactive >= 30:
            risk = "Medium"
        else:
            risk = "Low"

        results.append({
            "customer_id": customer_id,
            "last_purchase_date": last_purchase.strftime("%Y-%m-%d"),
            "days_inactive": days_inactive,
            "lapse_risk": risk
        })

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "customer_id",
                "last_purchase_date",
                "days_inactive",
                "lapse_risk"
            ]
        )
        writer.writeheader()
        writer.writerows(results)

    print("Customer lapse analysis completed!")
    print("Reference date:", reference_date.strftime("%Y-%m-%d"))
    print("Total customers analyzed:", len(results))

    print("\nLapse risk summary:")

    for risk in ["High", "Medium", "Low", "No Purchase"]:
        count = sum(
            1 for row in results
            if row["lapse_risk"] == risk
        )
        print(f"{risk}: {count}")

    print("\nOutput saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    predict_lapse()
