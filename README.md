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


MOMO-XML-App/
│
├── data/ 
│ ├── raw/ 
│ └── processed/ 
│
├── database/ # 
│ └── database_setup.sql
│
├── docs/ 
│ └── erd_diagram.png
  |__ database_design_document.pdf
│
├── examples/ 
│ └── json_schemas.json
│
├── scripts/ 
│ ├── extract.py
│ ├── transform.py
│ ├── load.py
│ └── utils.py
│
├── tests/ 
│ └── test_etl.py
│
├── web/ 
│ ├── index.html
│ ├── style.css
│ └── app.js
│
├── .gitignore 
├── README.md 
└── requirements.txt 


---

## System Architecture
 
 **High-level system design:** [View on Miro](https://miro.com/app/board/uXjVJK_IoDI=/)

---

## Scrum Board
We are using Trello to manage tasks with Scrum methodology.  

 **Trello Board Link:** [MOMO-XML Project - scrum board](https://trello.com/b/p4gLWs1S/momo-sms-project-scrum-board)

___

## Database Design
The MoMo SMS data processing system database is designed to efficiently handle transactions, users, categories, and system logs while ensuring scalability and data integrity.  
- Full ERD, documentation, and rationale are available in [docs/database_design_document.pdf](./docs/database_design_document.pdf).

