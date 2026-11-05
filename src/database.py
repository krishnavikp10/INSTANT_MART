
import sqlite3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "instamart.db"
CLEAN_PATH = ROOT / "data" / "clean"

TABLE_SCHEMAS = {
    "customers": """
        customer_id TEXT PRIMARY KEY,
        city TEXT,
        signup_date TEXT,
        age INTEGER,
        gender TEXT
    """,
    "products": """
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price_inr REAL
    """,
    "orders": """
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        product_id TEXT,
        quantity INTEGER,
        order_ts TEXT,
        status TEXT,
        discount_pct REAL,
        order_amount REAL,
        delivery_minutes REAL
    """,
    "tickets": """
        ticket_id TEXT PRIMARY KEY,
        customer_id TEXT,
        order_id TEXT,
        text TEXT,
        true_category TEXT
    """
}


def rebuild_database():
    """Rebuild database tables using the latest cleaned CSV files."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        for table, schema in TABLE_SCHEMAS.items():
            csv_path = CLEAN_PATH / f"{table}.csv"

            if not csv_path.exists():
                raise FileNotFoundError(
                    f"Cleaned CSV not found: {csv_path}"
                )

            with csv_path.open(
                "r", newline="", encoding="utf-8-sig"
            ) as file:
                reader = csv.DictReader(file)

                columns = reader.fieldnames

                if not columns:
                    raise ValueError(f"Empty CSV file: {csv_path}")

                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                cursor.execute(
                    f"CREATE TABLE {table} ({schema})"
                )

                placeholders = ", ".join("?" for _ in columns)
                column_names = ", ".join(columns)

                insert_query = (
                    f"INSERT INTO {table} "
                    f"({column_names}) VALUES ({placeholders})"
                )

                rows = [
                    tuple(row[column] for column in columns)
                    for row in reader
                ]

                cursor.executemany(insert_query, rows)

                print(f"{table}: {len(rows)} records imported")

        conn.commit()
        print("\nDatabase rebuilt successfully!")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_record_count(table_name):
    if table_name not in TABLE_SCHEMAS:
        raise ValueError("Invalid table name")

    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
    finally:
        conn.close()


def main():
    rebuild_database()

    print("\nInstaMart Database Connection Successful!")
    print("\nAvailable tables:")

    for table in TABLE_SCHEMAS:
        print(f"{table}: {get_record_count(table)} records")


if __name__ == "__main__":
    main()
