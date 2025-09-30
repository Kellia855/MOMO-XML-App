# MOMO-XML-App API Documentation

## Overview

The MOMO-XML-App API provides a RESTful interface for managing mobile money transaction data. It supports full CRUD (Create, Read, Update, Delete) operations on transaction records.

**Base URL:** http://localhost:8000  
**Authentication:** Basic Authentication required for all endpoints  
**Data Format:** JSON  

## Authentication

All endpoints require Basic Authentication with the following credentials:

**Username:** apiuser
**Password:** apipass

### Example Authentication Header:
Authorization: Basic YXBpdXNlcjphcGlwYXNz

## Endpoints

### 1. Get All Transactions

Retrieve a list of all transactions.

**Endpoint:** GET /transactions

**Response:**
json
{
  "data": [
    {
      "id": 1,
      "address": "M-Money",
      "date": "1715351458724",
      "type": "1",
      "body": "You have received 2000 RWF from Jane Smith (*********013) on your mobile money account...",
      "readable_date": "10 May 2024 4:30:58 PM",
      "contact_name": "Jane Smith",
      "service_center": "+250788110381",
      "transaction_id": "76662021700"
    }
  ],
  "count": 1,
  "message": "Transactions retrieved successfully"
}

**Status Codes:**
200 OK - Success
401 Unauthorized - Authentication required

---

### 2. Get Transaction by ID

Retrieve a specific transaction by its ID.

**Endpoint:** GET /transactions/{id}

**Parameters:**
id (integer, required) - The transaction ID

**Response:**
json
{
  "data": {
    "id": 1,
    "address": "M-Money",
    "date": "1715351458724",
    "type": "1",
    "body": "You have received 2000 RWF from Jane Smith (*********013) on your mobile money account...",
    "readable_date": "10 May 2024 4:30:58 PM",
    "contact_name": "Jane Smith",
    "service_center": "+250788110381",
    "transaction_id": "76662021700"
  },
  "message": "Transaction retrieved successfully"
}

**Status Codes:**
200 OK - Success
400 Bad Request - Invalid ID format
401 Unauthorized - Authentication required
404 Not Found - Transaction not found

---

### 3. Create New Transaction

Create a new transaction record.

**Endpoint:** POST /transactions

**Request Body:**
json
{
  "address": "M-Money",
  "date": "1715351458724",
  "type": "2",
  "body": "You have sent 1500 RWF to John Doe (*********456) from your mobile money account...",
  "readable_date": "10 May 2024 5:15:30 PM",
  "contact_name": "John Doe",
  "service_center": "+250788110381",
  "transaction_id": "76662021701"
}

**Response:**
json
{
  "data": {
    "id": 2,
    "address": "M-Money",
    "date": "1715351458724",
    "type": "2",
    "body": "You have sent 1500 RWF to John Doe (*********456) from your mobile money account...",
    "readable_date": "10 May 2024 5:15:30 PM",
    "contact_name": "John Doe",
    "service_center": "+250788110381",
    "transaction_id": "76662021701",
    "timestamp": "2025-09-30T12:34:56"
  },
  "message": "Transaction created successfully with ID 2"
}

**Status Codes:**
201 Created - Transaction created successfully
400 Bad Request - Invalid request body
401 Unauthorized - Authentication required
500 Internal Server Error - Server error

---

### 4. Update Transaction

Update an existing transaction by ID.

**Endpoint:** PUT /transactions/{id}

**Parameters:**
id (integer, required) - The transaction ID to update

**Request Body:**
json
{
  "address": "M-Money",
  "date": "1715351458724",
  "type": "2",
  "body": "Updated transaction message",
  "readable_date": "10 May 2024 5:15:30 PM",
  "contact_name": "John Doe Updated",
  "service_center": "+250788110381",
  "transaction_id": "76662021701"
}

**Response:**
json
{
  "data": {
    "id": 2,
    "address": "M-Money",
    "date": "1715351458724",
    "type": "2",
    "body": "Updated transaction message",
    "readable_date": "10 May 2024 5:15:30 PM",
    "contact_name": "John Doe Updated",
    "service_center": "+250788110381",
    "transaction_id": "76662021701",
    "updated_at": "2025-09-30T12:45:10"
  },
  "message": "Transaction 2 updated successfully"
}

**Status Codes:**
200 OK - Transaction updated successfully
400 Bad Request - Invalid ID format or request body
401 Unauthorized - Authentication required
404 Not Found - Transaction not found
500 Internal Server Error - Server error

---

### 5. Delete Transaction

Delete a transaction by ID.

**Endpoint:** DELETE /transactions/{id}

**Parameters:**
id (integer, required) - The transaction ID to delete

**Response:**
json
{
  "message": "Transaction 2 deleted successfully",
  "deleted_id": 2
}

**Status Codes:**
200 OK - Transaction deleted successfully
400 Bad Request - Invalid ID format
401 Unauthorized - Authentication required
404 Not Found - Transaction not found
500 Internal Server Error - Server error

---

## Data Schema

### Transaction Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | Auto-generated | Unique transaction identifier |
| address | string | Optional | Transaction address/source |
| date | string | Optional | Transaction date (timestamp) |
| type | string | Optional | Transaction type (1=received, 2=sent) |
| body | string | Optional | Full transaction message |
| readable_date | string | Optional | Human-readable date format |
| contact_name | string | Optional | Contact name involved in transaction |
| service_center | string | Optional | Service center number |
| transaction_id | string | Optional | External transaction identifier |
| timestamp | string | Auto-generated | Creation timestamp (ISO format) |
| updated_at | string | Auto-generated | Last update timestamp (ISO format) |

---

## Example Usage

### Using cURL

#### Get all transactions:
bash
curl -u apiuser:apipass http://localhost:8000/transactions

#### Get specific transaction:
bash
curl -u apiuser:apipass http://localhost:8000/transactions/1

#### Create new transaction:
bash
curl -u apiuser:apipass -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "address": "M-Money",
    "type": "2",
    "body": "Test transaction message",
    "contact_name": "Test User"
  }'

#### Update transaction:
bash
curl -u apiuser:apipass -X PUT http://localhost:8000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "address": "M-Money",
    "type": "1",
    "body": "Updated transaction message",
    "contact_name": "Updated User"
  }'

#### Delete transaction:
bash
curl -u apiuser:apipass -X DELETE http://localhost:8000/transactions/1

---

## Error Handling

### Error Response Format

All error responses follow this format:

json
{
  "error": "error_type",
  "message": "Human-readable error description"
}

### Common Error Types

| Error Type | Description | HTTP Status |
|------------|-------------|-------------|
| unauthorized | Authentication required or invalid credentials | 401 |
| invalid_id | ID parameter is not a valid integer | 400 |
| invalid_body | Request body is missing or invalid JSON | 400 |
| invalid_path | Endpoint path is incorrect | 400 |
| not_found | Requested resource not found | 404 |
| server_error | Internal server error occurred | 500 |

---

## CORS Support

The API includes CORS headers to support browser-based requests:

Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
---

## Security Notes

1. **Authentication:** Basic Authentication is used. For production, consider implementing OAuth2 or JWT tokens.
2. **HTTPS:** The server currently runs on HTTP. Use HTTPS in production.
3. **Input Validation:** Basic validation is performed. Consider adding more comprehensive input sanitization.
4. **File Access:** The API directly accesses JSON files. Consider using a proper database for production.

---

## Server Information

**Server:** Python HTTP Server (BaseHTTPRequestHandler)
**Data Storage:** JSON file (data/processed/sms_records.json)
**Thread Safety:** Uses threading locks for concurrent access
**Backup:** Automatic backup and restore on file operations

---

## Environment Variables

You can customize the API credentials using environment variables:

API_USER - API username (default: "apiuser")
API_PASS - API password (default: "apipass")

Example:
bash
export API_USER=myuser
export API_PASS=mypassword
python3 api/server.py

---

## Development

### Starting the Server

bash
cd MOMO-XML-App
python3 api/server.py

The server will start on http://localhost:8000

### Project Structure

MOMO-XML-App/
├── api/
│   └── server.py          # Main API server
├── data/
│   └── processed/
│       └── sms_records.json  # Data storage
└── docs/
    └── api_documentation.md  # This documentation
