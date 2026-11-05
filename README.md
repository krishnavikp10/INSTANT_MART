# InstaMart Copilot

An offline AI-powered retail support and business analytics assistant built using Python, SQLite, and a simulated Large Language Model (LLM).

## 1. Project Overview

InstaMart Copilot is designed to simplify retail customer support and business analysis through automated workflows.

The project combines customer support ticket classification, ticket prioritization, customer segmentation, customer lapse-risk analysis, policy assistance, refund processing simulation, and SQL-based business analytics.

It uses a locally provided mock LLM implementation, allowing the application to operate without paid APIs, external AI accounts, or internet connectivity during execution.

## 2. Project Objectives

- Automate customer support ticket classification.
- Prioritize support tickets based on category and urgency.
- Segment customers based on purchasing behaviour.
- Identify customers with potential lapse risk.
- Retrieve relevant information from locally stored policy documents.
- Simulate refund decisions using predefined business rules.
- Generate business insights through SQL analytics.
- Maintain an offline and reproducible execution environment.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11+ | Application development |
| SQLite | Database management |
| CSV | Dataset storage |
| SQL | Business analytics |
| Mock LLM | Offline language-model simulation |
| Regular Expressions | Text processing and matching |
| Git and GitHub | Version control and project hosting |

The implementation primarily uses Python standard-library modules.

## 4. Project Structure

```text
INSTANT_MART/
|
|-- data/
|   |-- raw/
|   |-- clean/
|   |-- policies/
|
|-- output/
|   |-- classified_tickets.csv
|   |-- customer_segments.csv
|   |-- lapse_predictions.csv
|   |-- triaged_tickets.csv
|
|-- src/
|   |-- clean_data.py
|   |-- database.py
|   |-- sql_queries.py
|   |-- classify.py
|   |-- ticket_triage.py
|   |-- customer_segmentation.py
|   |-- lapse_prediction.py
|   |-- policy_rag.py
|   |-- refund_agent.py
|   |-- check_order_status.py
|
|-- generate_data.py
|-- mock_llm.py
|-- check_tickets.py
|-- requirements.txt
|-- .gitignore
|-- README.md
```

The SQLite database is generated locally by the database module and is not required to be committed to the repository.

## 5. Dataset Description

The project uses generated retail datasets.

| Dataset | Raw Records | Cleaned Records |
|---|---:|---:|
| Customers | 1,200 | 1,200 |
| Products | 40 | 40 |
| Orders | 13,084 | 12,309 |
| Support Tickets | 164 | 160 |

### Data Cleaning Operations

- Removes duplicate order records.
- Removes records with missing order IDs.
- Handles invalid numeric values.
- Removes invalid support ticket records.
- Generates cleaned CSV files for database import.

## 6. Main Project Modules

### 6.1 Data Generation

- Generates customer records.
- Generates product information.
- Generates order records.
- Generates support ticket records.
- Creates the input datasets required for the project.

### 6.2 Data Cleaning

- Removes duplicate order records.
- Handles invalid numeric values.
- Removes records with missing order IDs.
- Removes invalid support tickets.
- Saves cleaned datasets in CSV format.

### 6.3 Database Management

- Creates and manages the SQLite database.
- Imports cleaned customer, product, order, and ticket datasets.
- Provides database access for analytics and support workflows.

### 6.4 SQL Business Analytics

Generates business insights through SQL queries, including:

- Revenue analysis by city.
- Top five selling products.
- Order status distribution.
- Average delivery time.
- Support ticket category analysis.
- Database record summary.
- Order status data quality checks.

### 6.5 Ticket Classification

- Classifies customer support tickets.
- Uses the offline mock LLM classification workflow.
- Generates classified ticket records.
- Saves classification results in CSV format.

### 6.6 Ticket Prioritization

- Assigns priority levels to customer support tickets.
- Identifies critical and high-priority issues.
- Categorizes tickets into billing, delivery, fraud, and technical categories.
- Generates a prioritized ticket report.

### 6.7 Customer Segmentation

Identifies five customer groups based on purchasing behaviour:

- High Value
- Loyal Customer
- Potential High Value
- Regular Customer
- New Customer

The module generates customer segment summaries and saves the results in CSV format.

### 6.8 Customer Lapse Prediction

- Analyses customer purchase history.
- Assigns High, Medium, and Low lapse-risk levels.
- Separately identifies customers with no completed purchases.
- Generates a customer lapse-risk report.

This module uses rule-based analysis rather than a trained machine-learning model.

### 6.9 Policy Assistant

- Retrieves relevant information from local policy documents.
- Supports refund, delivery, payment, privacy, and escalation queries.
- Uses the offline mock LLM workflow.
- Provides answers based on stored policy information.

### 6.10 Refund Agent

- Retrieves order details from the SQLite database.
- Searches locally stored refund policies.
- Calculates eligible refund amounts.
- Simulates automatic refund approval for eligible amounts up to INR 1,000.
- Escalates refund amounts above INR 1,000 to a simulated human approval workflow.
- Provides responses based on order information and refund rules.

All refund actions are simulations. No actual money is transferred.

## 7. Refund Policy Rules

The refund agent follows the locally stored refund policy.

| Condition | Decision |
|---|---|
| Order status is not completed | Refund denied |
| Delivery time is 45 minutes or less | Late-delivery refund denied |
| Delivery time exceeds 45 minutes | Full refund eligible |
| Refund amount up to INR 1,000 | Simulated automatic approval |
| Refund amount above INR 1,000 | Human approval escalation |

Additional policy conditions:

- Approved refunds are credited to the original payment method within five working days.
- Refund requests must be raised within seven days of the delivery date.

The current dataset does not contain sufficient delivery-date and refund-request-date information to enforce the seven-day deadline.

## 8. Installation and Reproduction

### 8.1 Prerequisites

- Python 3.11 or newer
- Git
- Visual Studio Code (recommended)
- Windows, Linux, or macOS

### 8.2 Clone the Repository

```bash
git clone https://github.com/krishnavikp10/INSTANT_MART.git
cd INSTANT_MART
```

### 8.3 Create a Virtual Environment

```bash
python -m venv .venv
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

For Linux or macOS:

```bash
source .venv/bin/activate
```

### 8.4 Install Dependencies

The project primarily uses Python standard-library modules and does not require external Python packages.

```bash
python -m pip install -r requirements.txt
```

### 8.5 Generate the Datasets

```bash
python generate_data.py
```

Expected dataset counts:

```text
customers: 1200
products: 40
orders_raw: 13084
tickets: 164
```

### 8.6 Clean the Datasets

```bash
python src/clean_data.py
```

Expected cleaned record counts:

```text
customers: 1200
products: 40
orders: 12309
tickets: 160
```

### 8.7 Create the SQLite Database

```bash
python src/database.py
```

Expected database tables:

```text
customers: 1200 records
products: 40 records
orders: 12309 records
tickets: 160 records
```

### 8.8 Run SQL Business Analytics

```bash
python src/sql_queries.py
```

This executes the SQL analytics queries and displays the business analysis results.

### 8.9 Run Customer Segmentation

```bash
python src/customer_segmentation.py
```

Output:

```text
output/customer_segments.csv
```

### 8.10 Run Customer Lapse Analysis

```bash
python src/lapse_prediction.py
```

Output:

```text
output/lapse_predictions.csv
```

### 8.11 Run Ticket Classification

```bash
python src/classify.py
```

Output:

```text
output/classified_tickets.csv
```

### 8.12 Run Ticket Prioritization

```bash
python src/ticket_triage.py
```

Output:

```text
output/triaged_tickets.csv
```

### 8.13 Run the Policy Assistant

```bash
python src/policy_rag.py
```

The assistant accepts customer policy questions interactively.

Example questions:

```text
Can I get a refund if my order is cancelled?
How long does a refund take?
What happens if my order is late?
What happens if fraud is detected?
```

Enter `exit` to close the assistant.

### 8.14 Run the Refund Agent

```bash
python src/refund_agent.py
```

The refund agent accepts customer requests and order IDs interactively.

Example order IDs for testing:

```text
ORD-108250
ORD-101136
ORD-110227
ORD-107301
```

Enter `exit` to close the agent.

## 9. Testing and Verified Results

The following results were verified during project execution.

### 9.1 Data Cleaning Results

| Operation | Result |
|---|---:|
| Customers saved | 1,200 |
| Products saved | 40 |
| Orders saved | 12,309 |
| Duplicate orders removed | 775 |
| Invalid numeric values handled | 112 |
| Tickets saved | 160 |
| Invalid tickets removed | 4 |

### 9.2 SQL Analytics Results

**Revenue by city**

| City | Total Revenue |
|---|---:|
| Hyderabad | 512,679.60 |
| Bengaluru | 500,115.65 |
| Delhi | 489,229.00 |
| Pune | 480,627.40 |
| Mumbai | 461,487.05 |
| Chennai | 448,805.15 |

**Order status distribution**

| Order Status | Total Orders |
|---|---:|
| Completed | 10,812 |
| Cancelled | 1,169 |
| Pending | 328 |

**Average delivery time:** 25.56 minutes.

**Database record summary**

| Table | Records |
|---|---:|
| Customers | 1,200 |
| Products | 40 |
| Orders | 12,309 |
| Tickets | 160 |

The SQL analysis completed successfully, including the order status data quality check.

### 9.3 Customer Segmentation Results

| Segment | Customers |
|---|---:|
| High Value | 179 |
| Loyal Customer | 538 |
| New Customer | 18 |
| Potential High Value | 47 |
| Regular Customer | 418 |
| **Total** | **1,200** |

### 9.4 Customer Lapse Analysis Results

| Lapse Risk | Customers |
|---|---:|
| High | 230 |
| Medium | 217 |
| Low | 725 |
| No Purchase | 28 |
| **Total** | **1,200** |

### 9.5 Ticket Classification and Prioritization Results

- Successfully classified 160 support tickets.
- Successfully prioritized 160 support tickets.

**Priority distribution**

| Priority | Tickets |
|---|---:|
| Critical | 39 |
| High | 9 |
| Medium | 75 |
| Normal | 37 |
| **Total** | **160** |

**Category distribution**

| Category | Tickets |
|---|---:|
| Billing | 58 |
| Delivery | 37 |
| Fraud | 20 |
| Technical | 45 |
| **Total** | **160** |

### 9.6 Policy Assistant Testing

Tested policy questions covering:

- Refund eligibility for cancelled orders.
- Refund processing timelines.
- Late delivery policies.
- Fraud escalation procedures.

The assistant returned policy-based responses using local policy documents.

### 9.7 Refund Agent Testing

Four test scenarios were completed.

| Order ID | Scenario | Result |
|---|---|---|
| ORD-108250 | Completed order, delivery in 17 minutes | Refund denied |
| ORD-101136 | Cancelled order | Refund denied |
| ORD-110227 | Completed order, delivery in 49 minutes | INR 75.60 simulated refund |
| ORD-107301 | Completed order, refund amount INR 1,098 | Escalated to human approval |

The refund agent successfully retrieved order information, checked policies, calculated refund amounts, and executed the corresponding simulated decisions.

No actual financial transactions were performed.

## 10. Project Limitations

- The mock LLM is an offline simulation and is not a production language model.
- Customer segmentation uses rule-based analysis.
- Customer lapse-risk analysis uses predefined business rules rather than a trained machine-learning model.
- Policy retrieval uses keyword-based matching rather than embedding-based semantic search.
- Refund processing is simulated and does not transfer money.
- The current order dataset does not contain sufficient delivery-date and refund-request-date information to enforce the seven-day refund request deadline.
- The system is designed as a local prototype rather than a production retail application.

## 11. Future Enhancements

- Integrate trained machine-learning models for customer lapse prediction.
- Improve policy retrieval using semantic embeddings.
- Develop a web-based customer support dashboard.
- Introduce real-time business analytics and visualization.
- Add comprehensive automated unit and integration tests.
- Integrate secure payment workflows in a production environment.

## 12. Conclusion

InstaMart Copilot demonstrates how offline AI workflows, database management, customer analytics, policy retrieval, and business rules can be combined to support retail customer service operations.

The project provides a modular and reproducible foundation for intelligent retail support while maintaining independence from paid external APIs and online AI services.

---

**Project:** InstaMart Copilot  
**Repository:** https://github.com/krishnavikp10/INSTANT_MART  
**Branch:** main  
**Execution:** Offline / Local Environment  
**Python Requirement:** Python 3.11 or newer
