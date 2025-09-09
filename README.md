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

├── README.md

├── .env.example

├── requirements.txt

├── index.html

├── web/

│   ├── styles.css

│   ├── chart_handler.js

│   └── assets/

├── data/

│   ├── raw/

│   │   └── momo.xml

│   ├── processed/

│   │   └── dashboard.json

│   ├── db.sqlite3

│   └── logs/

│       ├── etl.log

│       └── dead_letter/  

├── etl/

│   ├── __init__.py

│   ├── config.py

│   ├── parse_xml.py

│   ├── clean_normalize.py

│   ├── categorize.py

│   ├── load_db.py

│   └── run.py

├── api/

│   ├── __init__.py

│   ├── app.py

│   ├── db.py

│   └── schemas.py

├── scripts/

│   ├── run_etl.sh

│   ├── export_json.sh

│   └── serve_frontend.sh

└── tests/
    ├── test_parse_xml.py
    
    ├── test_clean_normalize.py
    
    └── test_categorize.py
    

---

## System Architecture
 
 **High-level system design:** [View on Miro](https://miro.com/app/board/uXjVJK_IoDI=/)

---

## Scrum Board
We are using Trello to manage tasks with Scrum methodology.  

 **Trello Board Link:** [MOMO-XML Project - scrum board](https://trello.com/b/p4gLWs1S/momo-sms-project-scrum-board)
