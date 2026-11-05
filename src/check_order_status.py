import csv

files = [
    "data/raw/orders.csv",
    "data/clean/orders.csv"
]

for filename in files:
    print("\nFile:", filename)

    with open(filename, "r", newline="", encoding="utf-8-sig") as file:
        rows = csv.DictReader(file)
        counts = {}

        for row in rows:
            status = row.get("status", "").strip().lower()
            counts[status] = counts.get(status, 0) + 1

    print("Order status counts:", counts)