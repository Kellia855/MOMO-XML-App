# SQL-to-JSON Mapping

This document explains how the relational database entities are represented in JSON format for serialization and API responses.

---

### User → JSON
- **SQL Table:** `Users`
- **Primary Key:** `user_id`
- **JSON Representation:** Appears as a nested `sender` or `receiver` object in transactions.

---

### Transaction_Categories → JSON
- **SQL Table:** `Transaction_Categories`
- **Primary Key:** `category_id`
- **JSON Representation:** Appears as a nested `category` object inside each transaction.

---

### Transactions → JSON
- **SQL Table:** `Transactions`
- **Primary Key:** `transaction_id`
- **Foreign Keys:** `sender_id`, `receiver_id`, `category_id`
- **JSON Representation:** Main `transaction` object, which nests `sender`, `receiver`, `category`, and `logs`.

---

### System_Logs → JSON
- **SQL Table:** `System_Logs`
- **Primary Key:** `log_id`
- **Foreign Key:** `transaction_id`
- **JSON Representation:** Appears as an array `logs` within the transaction.

---

### User_Transactions (junction) → JSON
- **SQL Table:** `User_Transactions`
- **Composite PK:** `(user_id, transaction_id)`
- **JSON Representation:** Can be serialized as a `participants` array with user roles.

---

### Notes
- **Timestamps**: Stored as `DATETIME` in SQL, converted to ISO 8601 in JSON (e.g., `2025-09-18T18:30:00Z`).
- **Amounts**: Stored as `DECIMAL` in SQL, serialized as numeric in JSON (not strings).
- **Metadata**: Extra attributes (e.g., provider, original XML) stored as JSON field in SQL and passed through in API responses.

