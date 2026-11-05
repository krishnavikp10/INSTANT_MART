# InstaMart Copilot

An offline AI-powered retail support and analytics assistant built using Python, SQLite, and a simulated Large Language Model (LLM).

## 1. Project Overview

InstaMart Copilot is designed to simplify retail customer support and business analysis. It combines ticket classification, customer segmentation, lapse-risk analysis, policy assistance, refund processing simulation, and SQL-based business analytics in one application.

The project uses a local mock LLM implementation, so it does not require paid APIs, internet access, or external AI accounts.

## 2. Objectives

- Automate customer support ticket classification.
- Prioritize tickets based on category and urgency.
- Segment customers using purchasing behaviour.
- Identify customers with potential lapse risk.
- Provide answers using locally stored company policies.
- Simulate refund decisions based on business rules.
- Generate useful business insights using SQL analytics.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| SQLite | Database management |
| CSV | Dataset storage |
| SQL | Business analytics |
| Mock LLM | Offline AI workflow simulation |
| Regular Expressions | Text processing and policy retrieval |

The implementation primarily uses Python standard-library modules.

## 4. Project Structure

```text
INSTANT_MART/
│
├── data/
│   ├── raw/
│   ├── clean/
│   ├── policies/
│   └── instamart.db
│
├── output/
│   ├── classified_tickets.csv
│   ├── customer_segments.csv
│   ├── lapse_predictions.csv
│   └── triaged_tickets.csv
│
├── src/
│   ├── clean_data.py
│   ├── database.py
│   ├── sql_queries.py
│   ├── classify.py
│   ├── ticket_triage.py
│   ├── customer_segmentation.py
│   ├── lapse_prediction.py
│   ├── policy_rag.py
│   ├── refund_agent.py
│   └── check_order_status.py
│
├── generate_data.py
├── mock_llm.py
├── check_tickets.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 5. Dataset Description

The project uses generated retail datasets.

| Dataset | Records |
|---|---:|
| Customers | 1,200 |
| Products | 40 |
| Raw Orders | 13,084 |
| Cleaned Orders | 12,309 |
| Raw Tickets | 164 |
| Cleaned Tickets | 160 |

The cleaning process removes duplicate orders and invalid tickets and handles invalid numeric values.

## 6. Main Modules

### 6.1 Data Cleaning
- Removes duplicate order records.
- Handles invalid numeric values.
- Removes records with missing order IDs.
- Removes invalid support tickets.

### 6.2 Database Management
- Creates and manages the SQLite database.
- Imports cleaned customer, product, order, and ticket datasets.

### 6.3 SQL Business Analytics
- Revenue analysis by city.
- Top-selling product analysis.
- Order status distribution.
- Average delivery time.
- Ticket category analysis.

### 6.4 Ticket Classification
- Classifies customer support tickets.
- Uses the offline mock LLM classification workflow.

### 6.5 Ticket Prioritization
- Assigns priority levels to customer tickets.
- Generates categorized and prioritized ticket reports.

### 6.6 Customer Segmentation
Identifies five customer groups:
- High Value
- Loyal Customer
- Potential High Value
- Regular Customer
- New Customer

### 6.7 Customer Lapse Prediction
- Analyses customer purchase history.
- Assigns High, Medium, or Low lapse risk.
- Separately identifies customers with no completed purchases.

This module uses rule-based analysis rather than a trained machine-learning model.

### 6.8 Policy Assistant
- Retrieves relevant information from local policy documents.
- Supports refund, delivery, payment, privacy, and escalation queries.
- Uses the offline mock LLM workflow.
- Returns answers grounded in the stored policy text.

### 6.9 Refund Agent
- Retrieves order details from the database.
- Checks the locally stored refund policy.
- Calculates eligible refund amounts.
- Simulates automatic refund approval for eligible amounts up to INR 1,000.
- Escalates amounts above INR 1,000 to a simulated human approval workflow.

Refund actions are simulations. No actual money is transferred.

## 7. Refund Policy Rules

| Condition | Decision |
|---|---|
| Order is not completed | Refund denied |
| Delivery time is 45 minutes or less | Late-delivery refund denied |
| Delivery time exceeds 45 minutes | Full refund eligible |
| Refund amount up to INR 1,000 | Simulated automatic approval |
| Refund amount above INR 1,000 | Human approval escalation |

Approved refunds are stated to be credited within five working days according to the local policy document.

## 8. Installation and Execution

### Prerequisites
- Python 3.10 or later
- Git
- Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/krishnavikp10/INSTANT_MART.git
cd INSTANT_MART
```

### Step 2: Run Data Generation

```bash
python generate_data.py
```

### Step 3: Clean the Datasets

```bash
python src/clean_data.py
```

### Step 4: Create the Database

```bash
python src/database.py
```

### Step 5: Run SQL Analytics

```bash
python src/sql_queries.py
```

### Step 6: Run Ticket Classification

```bash
python src/classify.py
```

### Step 7: Run Ticket Prioritization

```bash
python src/ticket_triage.py
```

### Step 8: Run Customer Segmentation

```bash
python src/customer_segmentation.py
```

### Step 9: Run Lapse Analysis

```bash
python src/lapse_prediction.py
```

### Step 10: Run the Policy Assistant

```bash
python src/policy_rag.py
```

### Step 11: Run the Refund Agent

```bash
python src/refund_agent.py
```

## 9. Testing and Verified Results

The following results were verified during development:

- Successfully cleaned 1,200 customer records.
- Successfully cleaned 12,309 order records.
- Successfully cleaned 160 support ticket records.
- Created the SQLite database with four tables.
- Generated customer segments for 1,200 customers.
- Generated lapse-risk analysis for 1,200 customers.
- Classified and prioritized 160 support tickets.
- Tested policy responses for refund, cancellation, refund timelines, and fraud.
- Completed four refund-agent test scenarios:
  - Ineligible completed order.
  - Cancelled order.
  - Eligible refund below INR 1,000.
  - Refund above INR 1,000 requiring escalation.

## 10. Limitations

- The mock LLM is an offline simulation and is not a production language model.
- Customer segmentation and lapse-risk analysis are rule-based.
- Policy retrieval uses keyword-based matching rather than embedding-based semantic search.
- Refund processing is simulated and does not transfer money.
- The current order data does not contain sufficient delivery-date and refund-request-date information to enforce the seven-day refund request deadline.

## 11. Future Enhancements

- Integrate a trained machine-learning model for customer lapse prediction.
- Improve policy retrieval using semantic embeddings.
- Add a web-based customer support dashboard.
- Introduce real-time analytics and visualization.
- Integrate secure payment gateway workflows in a production environment.
- Add comprehensive automated unit and integration tests.

## 12. Conclusion

InstaMart Copilot demonstrates how offline AI workflows, database management, business rules, and retail analytics can be combined to support customer service operations. The project provides a modular foundation for intelligent retail support while keeping its current implementation independent of paid external APIs.

---

**Project:** InstaMart Copilot  
**Repository:** https://github.com/krishnavikp10/INSTANT_MART  
**Execution:** Offline / Local Environment