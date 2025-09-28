# MoMo Transactions API Documentation

Version: 1.0
Framework: FastAPI
File: `main.py`

## Overview
This API allows clients to perform CRUD operations on Mobile Money (MoMo) transactions. All endpoints are protected with HTTP Basic Authentication. Unauthorized requests receive `401 Unauthorized` with the `WWW-Authenticate: Basic` header.

Base URL (local): `http://127.0.0.1:8000`

## Authentication
- Scheme: HTTP Basic Auth
- Header: `Authorization: Basic <base64(username:password)>`
- Demo credentials (development only):
  - Username: `apiuser`
  - Password: `apipass`

Note: In production, never hardcode credentials. Use environment variables or a secure user store.

### Example: Setting Authorization header
```bash
# username: apiuser, password: apipass
# echo -n "apiuser:apipass" | base64  # Linux/macOS to see encoded value
```

## Data Model
Transaction object fields:
- `transaction_id` (int)
- `sender_id` (int)
- `receiver_id` (int)
- `category_id` (int)
- `amount` (float)
- `transaction_date` (string, e.g., "2024-05-12T13:45:00")
- `status` (string)

All endpoints use this schema for request/response bodies where applicable.

## Endpoints

### 1) GET `/transactions`
Returns a list of all transactions.

- Auth: Required (Basic)
- Response: `200 OK`, body: `Transaction[]`

Curl examples:
```bash
# Valid auth
curl -i -u apiuser:apipass \
  http://127.0.0.1:8000/transactions

# Invalid auth (expect 401)
curl -i -u wrong:creds \
  http://127.0.0.1:8000/transactions
```

Example response (200):
```json
[
  {
    "transaction_id": 1,
    "sender_id": 100,
    "receiver_id": 200,
    "category_id": 10,
    "amount": 1500.5,
    "transaction_date": "2024-05-12T13:45:00",
    "status": "SUCCESS"
  }
]
```

### 2) GET `/transactions/{transaction_id}`
Returns a single transaction by ID.

- Auth: Required (Basic)
- Path params: `transaction_id` (int)
- Responses:
  - `200 OK` with `Transaction`
  - `404 Not Found` if no transaction with the given ID

Curl examples:
```bash
# Existing id
curl -i -u apiuser:apipass \
  http://127.0.0.1:8000/transactions/1

# Non-existing id (expect 404)
curl -i -u apiuser:apipass \
  http://127.0.0.1:8000/transactions/9999
```

### 3) POST `/transactions`
Creates a new transaction.

- Auth: Required (Basic)
- Body: `Transaction`
- Responses:
  - `201 Created` with created `Transaction`
  - `422 Unprocessable Entity` for invalid body shape

Curl example:
```bash
curl -i -u apiuser:apipass \
  -H "Content-Type: application/json" \
  -d '{
        "transaction_id": 2,
        "sender_id": 101,
        "receiver_id": 202,
        "category_id": 11,
        "amount": 250.75,
        "transaction_date": "2024-06-01T10:00:00",
        "status": "PENDING"
      }' \
  http://127.0.0.1:8000/transactions
```

### 4) PUT `/transactions/{transaction_id}`
Updates an existing transaction by ID.

- Auth: Required (Basic)
- Path params: `transaction_id` (int)
- Body: `Transaction` (full updated object)
- Responses:
  - `200 OK` with updated `Transaction`
  - `404 Not Found` if id does not exist

Curl example:
```bash
curl -i -u apiuser:apipass \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
        "transaction_id": 2,
        "sender_id": 101,
        "receiver_id": 202,
        "category_id": 11,
        "amount": 300.00,
        "transaction_date": "2024-06-02T12:00:00",
        "status": "SUCCESS"
      }' \
  http://127.0.0.1:8000/transactions/2
```

### 5) DELETE `/transactions/{transaction_id}`
Deletes a transaction by ID.

- Auth: Required (Basic)
- Path params: `transaction_id` (int)
- Responses:
  - `204 No Content` on success
  - `404 Not Found` if id does not exist

Curl example:
```bash
curl -i -u apiuser:apipass \
  -X DELETE \
  http://127.0.0.1:8000/transactions/2
```

## Error Codes and Responses
- `401 Unauthorized`: Missing or invalid Basic auth; includes `WWW-Authenticate: Basic` header
- `404 Not Found`: Transaction not found
- `422 Unprocessable Entity`: Invalid request body structure

Example 401 response:
```json
{
  "detail": "Unauthorized"
}
```

## Testing with Postman
1. Create a new Collection: "MoMo Transactions API".
2. In the Collection Authorization tab, set:
   - Type: Basic Auth
   - Username: `apiuser`
   - Password: `apipass`
   - Save and choose "Inherit auth from parent" for requests.
3. Create requests for each endpoint:
   - GET `/transactions`
   - GET `/transactions/{id}` (e.g., 1)
   - POST `/transactions` with the JSON body example above
   - PUT `/transactions/{id}` with the JSON body example above
   - DELETE `/transactions/{id}`
4. For negative tests, override Authorization at the request level with wrong credentials and verify `401`.
5. Capture screenshots of both successful and error responses for the report.

## Running the API Locally
Start the FastAPI app with Uvicorn:
```bash
uvicorn api.server:app --reload
```
Then open interactive docs at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Testing & Validation

The following steps validate all CRUD operations with both valid and invalid authentication using curl and Postman. Capture screenshots of successful responses and error cases for your report.

### Prerequisites
- Server running locally: `uvicorn api.server:app --reload`
- Base URL: `http://127.0.0.1:8000`
- Basic Auth credentials (development): `apiuser` / `apipass`

### A) Test with curl

1) GET `/transactions`
```bash
# Valid auth → expect 200
curl -i -u apiuser:apipass \
  http://127.0.0.1:8000/transactions

# Invalid auth → expect 401
curl -i -u wrong:creds \
  http://127.0.0.1:8000/transactions
```

2) GET `/transactions/{id}`
```bash
# Existing id (1) → expect 200
curl -i -u apiuser:apipass \
  http://127.0.0.1:8000/transactions/1

# Non-existing id (9999) → expect 404
curl -i -u apiuser:apipass \
  http://127.0.0.1:8000/transactions/9999
```

3) POST `/transactions`
```bash
curl -i -u apiuser:apipass \
  -H "Content-Type: application/json" \
  -d '{
        "transaction_id": 2,
        "sender_id": 101,
        "receiver_id": 202,
        "category_id": 11,
        "amount": 250.75,
        "transaction_date": "2024-06-01T10:00:00",
        "status": "PENDING"
      }' \
  http://127.0.0.1:8000/transactions
```

4) PUT `/transactions/{id}`
```bash
curl -i -u apiuser:apipass \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
        "transaction_id": 2,
        "sender_id": 101,
        "receiver_id": 202,
        "category_id": 11,
        "amount": 300.00,
        "transaction_date": "2024-06-02T12:00:00",
        "status": "SUCCESS"
      }' \
  http://127.0.0.1:8000/transactions/2
```

5) DELETE `/transactions/{id}`
```bash
curl -i -u apiuser:apipass \
  -X DELETE \
  http://127.0.0.1:8000/transactions/2
```

Tip: The server prints minimal access logs for `/transactions*` in the terminal, which you can also screenshot.

### B) Test with Postman
1. Create a Collection named "MoMo Transactions API".
2. Collection Authorization:
   - Type: Basic Auth
   - Username: `apiuser`
   - Password: `apipass`
   - Save and enable "Inherit auth from parent" on requests.
3. Create requests:
   - GET `/transactions`
   - GET `/transactions/{id}` (e.g., 1 and 9999)
   - POST `/transactions` with the JSON in the curl example above
   - PUT `/transactions/{id}` with the JSON in the curl example above
   - DELETE `/transactions/{id}`
4. Negative test: override Authorization with wrong credentials and verify `401`.
5. Capture screenshots of both successful and error responses (including status code and body). 

Alternatively, import the provided Postman collection JSON at `docs/MoMo_Transactions_API.postman_collection.json` and run the requests directly.

## Notes and Best Practices
- Development credentials are hardcoded in `main.py` for demo purposes only. Replace with environment variables or integrate with a user store for production use.
- The current data store is an in-memory list; it resets on server restart. Integrate a real database to persist data.
