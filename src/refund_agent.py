
"""Offline Instamart refund agent using mock_llm.py."""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mock_llm

ORDERS_FILE = ROOT / "data" / "clean" / "orders.csv"
POLICY_DIR = ROOT / "data" / "policies"
MAX_STEPS = 8


def get_order(order_id):
    """Look up an order in the cleaned orders dataset."""
    if not ORDERS_FILE.exists():
        return {"error": "Clean orders dataset not found."}

    with ORDERS_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        for order in csv.DictReader(file):
            if order["order_id"].strip().upper() == order_id.upper():
                return order

    return {"error": "Order not found."}


def search_policy(query):
    """Search local policy documents for relevant information."""
    if not POLICY_DIR.exists():
        return {"error": "Policy folder not found."}

    results = []

    for path in POLICY_DIR.glob("*.txt"):
        content = path.read_text(encoding="utf-8")
        if any(word in content.lower() for word in query.lower().split()):
            results.append({
                "document": path.name,
                "content": content
            })

    return {"results": results}


def calculate_refund(order_amount, delivery_minutes):
    """Calculate refund according to the 45-minute rule."""
    amount = float(order_amount)
    minutes = float(delivery_minutes)

    if minutes > 45:
        return {"refund_inr": round(amount, 2)}

    return {"refund_inr": 0}


def issue_refund(order_id, refund_inr):
    """Simulate an automatic refund; no real payment is made."""
    return {
        "status": "simulated",
        "order_id": order_id,
        "refund_inr": refund_inr,
        "message": "Simulated refund approval. No money was transferred."
    }


def escalate_to_human(order_id, refund_inr):
    """Simulate escalation to a human support lead."""
    return {
        "status": "escalated",
        "order_id": order_id,
        "refund_inr": refund_inr,
        "message": "Sent for simulated human approval."
    }


def execute_tool(name, arguments):
    """Execute a tool requested by the offline agent."""
    try:
        if name == "get_order":
            return get_order(arguments["order_id"])

        if name == "search_policy":
            return search_policy(arguments.get("query", ""))

        if name == "calculate_refund":
            return calculate_refund(
                arguments["order_amount"],
                arguments["delivery_minutes"]
            )

        if name == "issue_refund":
            return issue_refund(
                arguments["order_id"],
                arguments["refund_inr"]
            )

        if name == "escalate_to_human":
            return escalate_to_human(
                arguments["order_id"],
                arguments["refund_inr"]
            )

        return {"error": f"Unknown tool: {name}"}

    except (KeyError, ValueError, TypeError) as error:
        return {"error": str(error)}


def run_agent(user_request):
    """Run the mock LLM agent and its requested tools."""
    messages = [
        {
            "role": "system",
            "content": (
                "AGENT\n"
                "You are an Instamart refund support agent. "
                "Use tools to look up orders, check policies, "
                "calculate refunds, and process eligible requests. "
                "Never claim a real payment was transferred."
            )
        },
        {"role": "user", "content": user_request}
    ]

    mock_llm.reset()

    for step in range(MAX_STEPS):
        try:
            response = mock_llm.chat(messages)
        except mock_llm.TransientLLMError as error:
            return f"Temporary model error: {error}"

        message = response.choices[0].message
        tool_calls = message.tool_calls or []

        if not tool_calls:
            return message.content or "The agent returned no response."

        for tool_call in tool_calls:
            name = tool_call.name
            arguments = tool_call.arguments

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            print(f"\n[Tool {step + 1}] {name}")
            print("Arguments:", arguments)

            result = execute_tool(name, arguments)

            print("Result:", result)

            messages.append({
                "role": "tool",
                "name": name,
                "content": json.dumps(result)
            })

    return "Stopped: maximum tool-call limit reached."


def main():
    if not ORDERS_FILE.exists():
        print("Clean orders.csv not found.")
        print("Run: python src/clean_data.py")
        return

    print("INSTAMART OFFLINE REFUND AGENT")
    print("Enter an order ID such as ORD-123456.")
    print("Type 'exit' to close.\n")

    while True:
        request = input("Customer request: ").strip()

        if request.lower() == "exit":
            print("Refund agent closed.")
            break

        if not request:
            print("Please enter a request.")
            continue

        result = run_agent(request)
        print("\nAgent response:", result)
        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()
