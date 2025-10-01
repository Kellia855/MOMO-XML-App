# MoMo SMS Data Processing & Dashboard

## Team Info
**Team Name:** Your Team Name Here  
**Team Members:**  
  - Member 1 :Kellia Kamikazi.(https://github.com/Kellia855)  
  - Member 2 :Tumugane Rolande.(https://github.com/TRolande)  
  - Member 3 :Aurore Umumararungu.(https://github.com/Aurore5-U)  
  
---

## Project Description
This project processes **MoMo SMS transaction data** in XML format.  
It includes:  
1. **ETL pipeline** – Extract, clean, normalize, and categorize MoMo XML.  
2. **Database storage** – Save structured data in SQLite.  
3. **Frontend dashboard** – Visualize transactions with charts & tables.  

---

## Project Structure

```
MOMO-XML-App/
├── data/
│   ├── raw/
│   ├── processed/
|
|── database/
│       └── database_setup.sql
├── docs/
│   ├── erd_diagram.png
│   └── database_design_document.pdf
├── examples/
│   └── json_schemas.json
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── utils/
├── tests/
│   └── test_etl.py
├── web/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── .gitignore
├── README.md
└── requirements.txt
```
---

## System Architecture
 
 **High-level system design:** [View on Miro](https://miro.com/app/board/uXjVJK_IoDI=/)

---

## Scrum Board
We are using Trello to manage tasks with Scrum methodology.  

 **Trello Board Link:** [MOMO-XML Project - scrum board](https://trello.com/b/p4gLWs1S/momo-sms-project-scrum-board)

___

## Setup Instructions

### Prerequisites
- **Python 3.8+** installed on your system
- **Git** for version control
- **Text editor** (VS Code, PyCharm, etc.)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd MOMO-XML-App
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare Data Directory Structure
The following directories should exist (they'll be created automatically if missing):
```
data/
├── raw/          
└── processed/   
```

### 5. Start the API Server
```bash
# Navigate to api directory
cd api

# Start the REST API server
python server.py
```
The server will start on `http://localhost:8000`

### 6. API Authentication
The REST API uses Basic Authentication:
- **Username:** `apiuser`
- **Password:** `apipass`

### 7. Test the API
```bash
# Test GET endpoint
curl -u apiuser:apipass http://localhost:8000/transactions

# Test POST endpoint
curl -u apiuser:apipass -H "Content-Type: application/json" -X POST http://localhost:8000/transactions -d '{"message":"Test transaction","amount":100}'
```

---

## API Endpoints

### Available Endpoints
- **GET** `/transactions` - List all transactions
- **GET** `/transactions/{id}` - Get specific transaction
- **POST** `/transactions` - Create new transaction
- **PUT** `/transactions/{id}` - Update existing transaction
- **DELETE** `/transactions/{id}` - Delete transaction

### Example API Usage
```bash
# Get all transactions
curl -u apiuser:apipass http://localhost:8000/transactions

# Get specific transaction
curl -u apiuser:apipass http://localhost:8000/transactions/1

# Create new transaction
curl -u apiuser:apipass -H "Content-Type: application/json" -X POST \
  http://localhost:8000/transactions \
  -d '{"message":"Payment received","amount":5000,"type":"credit"}'

# Update transaction
curl -u apiuser:apipass -H "Content-Type: application/json" -X PUT \
  http://localhost:8000/transactions/1 \
  -d '{"message":"Updated payment","amount":6000,"type":"credit"}'

# Delete transaction
curl -u apiuser:apipass -X DELETE http://localhost:8000/transactions/1
```

---

## Environment Configuration

### Optional Environment Variables
You can customize the API server by setting these environment variables:

```bash
# API Authentication (optional, defaults shown)
export API_USER=apiuser
export API_PASS=apipass

# Server Port (optional, default is 8000)
export PORT=8000
```

### Data File Location
The API server uses the JSON file at:
`data/processed/sms_records.json`


---

## Troubleshooting

### Common Issues

1. **Server won't start**
   - Check if port 8000 is already in use: `netstat -an | findstr :8000`
   - Try a different port by setting the `PORT` environment variable

2. **Authentication fails**
   - Ensure you're using Basic Auth with `apiuser:apipass`
   - Include the `-u` flag in curl commands

3. **POST/PUT requests fail**
   - Always include the `Content-Type: application/json` header
   - Ensure request body is valid JSON

4. **Data file not found**
   - Make sure `data/processed/sms_records.json` exists
   - The server will create an empty file if it doesn't exist

5. **CORS issues (web dashboard)**
   - Use a proper HTTP server instead of opening HTML files directly
   - The API server includes CORS headers for cross-origin requests

---

## Database Design
The MoMo SMS data processing system database is designed to efficiently handle transactions, users, categories, and system logs while ensuring scalability and data integrity.  
- Full ERD, documentation, and rationale are available in [docs/database_design_document.pdf](./docs/database_design_document.pdf).

