
import csv
import os
from collections import defaultdict
from datetime import datetime

CUSTOMERS_FILE = "data/clean/customers.csv"
ORDERS_FILE = "data/clean/orders.csv"
OUTPUT_FILE = "output/customer_segments.csv"


def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def calculate_customer_metrics(customers, orders):
    metrics = defaultdict(lambda: {
        "total_orders": 0,
        "total_spent": 0.0,
        "completed_orders": 0,
        "cancelled_orders": 0
    })

    for order in orders:
        customer_id = order["customer_id"]
        data = metrics[customer_id]

        data["total_orders"] += 1
        data["total_spent"] += float(order["order_amount"] or 0)

        if order["status"].lower() == "completed":
            data["completed_orders"] += 1
        elif order["status"].lower() == "cancelled":
            data["cancelled_orders"] += 1

    results = []

    for customer in customers:
        customer_id = customer["customer_id"]
        data = metrics[customer_id]

        total_orders = data["total_orders"]
        total_spent = data["total_spent"]

        average_order_value = (
            total_spent / total_orders if total_orders else 0
        )

        if total_orders == 0:
            segment = "New Customer"
        elif total_spent >= 5000 and total_orders >= 5:
            segment = "High Value"
        elif total_orders >= 5:
            segment = "Loyal Customer"
        elif total_spent >= 2000:
            segment = "Potential High Value"
        else:
            segment = "Regular Customer"

        results.append({
            "customer_id": customer_id,
            "city": customer["city"],
            "age": customer["age"],
            "total_orders": total_orders,
            "completed_orders": data["completed_orders"],
            "cancelled_orders": data["cancelled_orders"],
            "total_spent": round(total_spent, 2),
            "average_order_value": round(average_order_value, 2),
            "segment": segment
        })

    return results


def main():
    if not os.path.exists(CUSTOMERS_FILE):
        print("Customer dataset not found.")
        return

    if not os.path.exists(ORDERS_FILE):
        print("Order dataset not found.")
        return

    customers = load_csv(CUSTOMERS_FILE)
    orders = load_csv(ORDERS_FILE)

    results = calculate_customer_metrics(customers, orders)

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys())
        )
        writer.writeheader()
        writer.writerows(results)

    print("Customer segmentation completed!")
    print("Total customers:", len(results))

    print("\nSegment summary:")
    segments = defaultdict(int)

    for customer in results:
        segments[customer["segment"]] += 1

    for segment, count in sorted(segments.items()):
        print(f"{segment}: {count}")

    print("\nOutput saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
