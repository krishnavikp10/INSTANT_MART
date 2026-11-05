
"""Offline support-ticket classification using mock_llm.py."""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mock_llm

RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
OUTPUT = ROOT / "output"

OUTPUT.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """
CLASSIFY
You are an Instamart customer support ticket classifier.
Classify each ticket into exactly one category:
billing, delivery, technical, fraud.
Return JSON with category and reason.
"""


def classify_ticket(text):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]

    for attempt in range(3):
        try:
            response = mock_llm.chat(messages)
            result = json.loads(response.choices[0].message.content)

            if result.get("category") not in mock_llm.CATS:
                raise ValueError("Invalid category")

            return result["category"], result.get("reason", "")

        except mock_llm.TransientLLMError:
            if attempt == 2:
                return "technical", "Temporary model failure"

        except (json.JSONDecodeError, ValueError, TypeError):
            return "technical", "Invalid model response"

    return "technical", "Classification failed"


def main():
    input_file = CLEAN / "tickets.csv"

    if not input_file.exists():
        print("Clean tickets.csv not found. Run clean_data.py first.")
        return

    with input_file.open("r", newline="", encoding="utf-8-sig") as file:
        tickets = list(csv.DictReader(file))

    results = []

    mock_llm.reset()

    for ticket in tickets:
        text = " ".join(str(value) for value in ticket.values())
        category, reason = classify_ticket(text)

        result = dict(ticket)
        result["predicted_category"] = category
        result["classification_reason"] = reason
        results.append(result)

    output_file = OUTPUT / "classified_tickets.csv"

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    print(f"Successfully classified {len(results)} tickets.")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    main()
