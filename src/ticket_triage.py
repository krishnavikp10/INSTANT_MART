
import csv
import os

INPUT_FILE = os.path.join("output", "classified_tickets.csv")
OUTPUT_FILE = os.path.join("output", "triaged_tickets.csv")

VALID_CATEGORIES = {
    "billing",
    "delivery",
    "technical",
    "fraud"
}


def determine_priority(category, ticket_text):
    text = ticket_text.lower()

    urgent_words = [
        "urgent", "immediately", "critical",
        "account hacked", "unauthorized",
        "stolen", "fraud", "scam"
    ]

    high_words = [
        "failed", "missing", "charged twice",
        "payment issue", "not received"
    ]

    if category == "fraud" or any(word in text for word in urgent_words):
        return "Critical"

    if any(word in text for word in high_words):
        return "High"

    if category in ["billing", "technical"]:
        return "Medium"

    return "Normal"


def triage_tickets():
    if not os.path.exists(INPUT_FILE):
        print("Error: Classified tickets file not found.")
        print("Run python src/classify.py first.")
        return

    os.makedirs("output", exist_ok=True)

    with open(INPUT_FILE, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        tickets = list(reader)

        if not tickets:
            print("No tickets found.")
            return

        print("Input columns:", reader.fieldnames)

    triaged = []

    for ticket in tickets:
        category = (
            ticket.get("predicted_category")
            or ticket.get("category")
            or ticket.get("true_category")
            or "technical"
        ).strip().lower()

        if category not in VALID_CATEGORIES:
            category = "technical"

        ticket_text = ticket.get("text", "")

        priority = determine_priority(category, ticket_text)

        ticket["triage_category"] = category
        ticket["priority"] = priority

        triaged.append(ticket)

    fieldnames = list(triaged[0].keys())

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(triaged)

    print("\nTicket triage completed!")
    print("Total tickets:", len(triaged))

    print("\nPriority summary:")
    for priority in ["Critical", "High", "Medium", "Normal"]:
        count = sum(1 for t in triaged if t["priority"] == priority)
        print(f"{priority}: {count}")

    print("\nCategory summary:")
    for category in sorted(VALID_CATEGORIES):
        count = sum(
            1 for t in triaged
            if t["triage_category"] == category
        )
        print(f"{category}: {count}")

    print("\nOutput saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    triage_tickets()
