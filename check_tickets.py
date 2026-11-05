import sqlite3

connection = sqlite3.connect("data/instamart.db")

query = """
SELECT ticket_id, text, true_category
FROM tickets
WHERE LOWER(TRIM(true_category)) = 'none'
ORDER BY ticket_id
"""

results = connection.execute(query).fetchall()

print("Total invalid tickets:", len(results))

for ticket_id, description, category in results:
    print("\nTicket ID:", ticket_id)
    print("Description:", repr(description))
    print("Category:", repr(category))

connection.close()