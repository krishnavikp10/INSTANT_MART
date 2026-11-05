
"""Offline policy RAG assistant using mock_llm.py."""

import sys
import re
from pathlib import Path
from difflib import SequenceMatcher

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mock_llm

POLICY_DIR = ROOT / "data" / "policies"


def load_policies():
    documents = []

    if not POLICY_DIR.exists():
        print("Policy folder not found:", POLICY_DIR)
        return documents

    for path in POLICY_DIR.glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        sentences = re.split(r"(?<=[.!?])\s+", text)

        for sentence in sentences:
            sentence = sentence.strip()

            if sentence:
                documents.append({
                    "source": path.name,
                    "text": sentence
                })

    return documents


def normalize(text):
    text = text.lower()
    text = text.replace("₹", " inr ")
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def detect_intent(question):
    q = normalize(question)

    # Specific intents must be checked before general refund.
    if any(word in q for word in [
        "fraud", "fraudulent", "unauthorized",
        "suspicious transaction", "scam",
        "stolen payment", "unknown transaction"
    ]):
        return "fraud"

    if any(word in q for word in [
        "cancelled", "canceled", "cancellation",
        "cancel order"
    ]):
        return "cancelled"

    if (
        "how many days" in q
        or "deadline" in q
        or "request period" in q
        or "within how many" in q
        or "last date" in q
        or ("days" in q and "request" in q)
    ):
        return "deadline"

    if any(word in q for word in [
        "credited", "credit", "receive my refund",
        "refund arrive", "refund timeline",
        "how long", "processing time",
        "original payment method"
    ]):
        return "credit"

    if (
        re.search(r"\babov\w*", q)
        or "over 1000" in q
        or "more than 1000" in q
        or "above 1000" in q
        or "human approval" in q
        or "approval limit" in q
    ):
        return "approval"

    if any(word in q for word in [
        "late delivery", "delivery late",
        "delayed", "delivery delay",
        "more than 45", "45 minutes"
    ]):
        return "late_delivery"

    if any(word in q for word in [
        "refund", "reubd", "refubd", "reimbursement"
    ]):
        return "refund"

    if "delivery" in q:
        return "delivery"

    if any(word in q for word in [
        "privacy", "personal data", "data protection"
    ]):
        return "privacy"

    if any(word in q for word in [
        "payment", "upi", "debit card",
        "credit card", "cash on delivery"
    ]):
        return "payment"

    return "general"


def retrieve_relevant_sentences(question, documents):
    intent = detect_intent(question)

    patterns = {
        "cancelled": [
            r"orders with status cancelled"
        ],

        "fraud": [
            r"fraud",
            r"unauthorized",
            r"suspicious",
            r"report.*transaction",
            r"escalat"
        ],

        "deadline": [
            r"refund request must be raised within 7 days"
        ],

        "credit": [
            r"approved refunds are credited to the original payment method within 5 working days"
        ],

        "approval": [
            r"a refund above INR 1000 must be approved by a human support lead",
            r"refunds up to INR 1000"
        ],

        "late_delivery": [
            r"if a completed order is delivered in more than 45 minutes",
            r"if a completed order is delivered in 45 minutes or less"
        ],

        "refund": [
            r"a refund can be requested only for orders",
            r"orders with status cancelled",
            r"if a completed order is delivered in more than 45 minutes",
            r"if a completed order is delivered in 45 minutes or less",
            r"refunds up to INR 1000",
            r"a refund above INR 1000",
            r"approved refunds are credited",
            r"a refund request must be raised"
        ],

        "delivery": [
            r"standard delivery",
            r"delivery fee",
            r"delivery is free"
        ],

        "payment": [
            r"customers can pay",
            r"cash on delivery",
            r"wallet balance"
        ],

        "privacy": [
            r"privacy",
            r"personal data",
            r"data protection",
            r"deleted from active systems"
        ],

        "general": [
            r"refund",
            r"delivery",
            r"payment",
            r"privacy",
            r"fraud"
        ]
    }

    selected = []

    for document in documents:
        sentence = document["text"]

        for pattern in patterns[intent]:
            if re.search(pattern, sentence, re.IGNORECASE):
                selected.append(document)
                break

    # If fraud-specific wording was not found, search the fraud
    # and escalation policy files for relevant content.
    if intent == "fraud" and not selected:
        selected = [
            doc for doc in documents
            if "fraud" in doc["source"].lower()
            or "escalation" in doc["source"].lower()
        ]

    return selected


def answer_question(question, documents):
    if not documents:
        return "No policy documents are available."

    retrieved = retrieve_relevant_sentences(question, documents)

    if not retrieved:
        return "I could not find an answer in the available policy documents."

    context = "\n".join(
        f"[{item['source']}] {item['text']}"
        for item in retrieved
    )

    messages = [
        {
            "role": "system",
            "content": (
                "POLICY ASSISTANT\n"
                "Answer only from the supplied policy context. "
                "Do not invent or change policy rules."
            )
        },
        {
            "role": "user",
            "content": (
                f"POLICY CONTEXT:\n{context}\n\n"
                f"QUESTION:\n{question}"
            )
        }
    ]

    mock_llm.chat(messages)

    return "\n".join(
        f"- {item['text']}"
        for item in retrieved
    )


def main():
    documents = load_policies()

    if not documents:
        return

    print(f"Loaded {len(documents)} policy sections.")
    print("Instamart Policy Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Your question: ").strip()

        if question.lower() == "exit":
            print("Policy assistant closed.")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer = answer_question(question, documents)
            print("\nAnswer:", answer, "\n")
        except Exception as error:
            print("Could not generate an answer:", error)


if __name__ == "__main__":
    main()
