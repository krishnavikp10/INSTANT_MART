
"""Clean InstaMart raw datasets and save prepared CSV files."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"

CLEAN.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def write_csv(path, rows):
    if not rows:
        print(f"Skipped empty dataset: {path.name}")
        return

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {path.name}: {len(rows)} rows")


def clean_other_file(filename, key):
    path = RAW / filename
    rows = read_csv(path)
    cleaned = []
    seen = set()

    for row in rows:
        value = row.get(key, "").strip()

        if not value or value in seen:
            continue

        seen.add(value)
        cleaned.append(row)

    write_csv(CLEAN / filename, cleaned)


def clean_orders():
    rows = read_csv(RAW / "orders.csv")
    cleaned = []
    seen = set()
    duplicates = 0
    missing_ids = 0
    invalid_numbers = 0

    numeric_fields = [
        "quantity",
        "order_amount",
        "discount_pct",
        "delivery_minutes"
    ]

    for row in rows:
        order_id = row.get("order_id", "").strip()

        if not order_id:
            missing_ids += 1
            continue

        if order_id in seen:
            duplicates += 1
            continue

        seen.add(order_id)

        for field in numeric_fields:
            value = row.get(field, "").strip()

            if not value:
                row[field] = ""
                continue

            try:
                number = float(value)

                if field in ("quantity", "delivery_minutes"):
                    row[field] = str(int(number))
                else:
                    row[field] = str(round(number, 2))

            except (ValueError, TypeError):
                row[field] = ""
                invalid_numbers += 1

        cleaned.append(row)

    write_csv(CLEAN / "orders.csv", cleaned)

    print("Duplicate orders removed:", duplicates)
    print("Orders with missing IDs removed:", missing_ids)
    print("Invalid numeric values handled:", invalid_numbers)


def clean_tickets():
    rows = read_csv(RAW / "tickets.csv")
    cleaned = []
    seen = set()
    removed = 0

    for row in rows:
        ticket_id = row.get("ticket_id", "").strip()
        description = row.get("text", "").strip()
        category = row.get("true_category", "").strip().lower()

        if (
            not ticket_id
            or ticket_id in seen
            or not description
            or not category
            or category == "none"
        ):
            removed += 1
            continue

        seen.add(ticket_id)
        cleaned.append(row)

    write_csv(CLEAN / "tickets.csv", cleaned)
    print("Invalid tickets removed:", removed)


def main():
    print("INSTANTMART DATA CLEANING")
    print("=" * 45)

    clean_other_file("customers.csv", "customer_id")
    clean_other_file("products.csv", "product_id")
    clean_orders()
    clean_tickets()

    print("\nDATA CLEANING COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
