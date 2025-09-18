CREATE TABLE User (
  user_id INT PRIMARY KEY COMMENT 'Unique ID',
  first_name VARCHAR(100) COMMENT 'First name',
  last_name VARCHAR(100) COMMENT 'Last name',
  phone_number VARCHAR(20) COMMENT 'Phone',
  email VARCHAR(100) COMMENT 'Email',
  user_type VARCHAR(50) COMMENT 'Type'
) COMMENT='Users table';

CREATE TABLE Transaction_Categories (
  category_id INT PRIMARY KEY COMMENT 'Unique ID',
  category_name VARCHAR(100) COMMENT 'Name',
  description TEXT COMMENT 'Details'
) COMMENT='Transaction categories';

CREATE TABLE Transaction (
  transaction_id INT PRIMARY KEY COMMENT 'Unique ID',
  sender_id INT COMMENT 'FK user',
  receiver_id INT COMMENT 'FK user',
  category_id INT COMMENT 'FK category',
  amount DECIMAL(12,2) COMMENT 'Amount',
  transaction_date DATETIME COMMENT 'Date',
  status VARCHAR(50) COMMENT 'Status',
  FOREIGN KEY (sender_id) REFERENCES User(user_id),
  FOREIGN KEY (receiver_id) REFERENCES User(user_id),
  FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id)
) COMMENT='Transactions';

CREATE TABLE User_Transactions (
  user_id INT COMMENT 'FK user',
  transaction_id INT COMMENT 'FK transaction',
  role VARCHAR(50) COMMENT 'Role in TX',
  PRIMARY KEY (user_id, transaction_id),
  FOREIGN KEY (user_id) REFERENCES User(user_id),
  FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id)
) COMMENT='User-Transaction links';

CREATE TABLE System_Logs (
  log_id INT PRIMARY KEY COMMENT 'Unique ID',
  transaction_id INT COMMENT 'FK transaction',
  log_type VARCHAR(50) COMMENT 'Type',
  created_at DATETIME COMMENT 'Created',
  message TEXT COMMENT 'Message',
  FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id)
) COMMENT='Logs';

CREATE INDEX idx_user_userid ON User(user_id);
CREATE INDEX idx_transaction_transactionid ON Transaction(transaction_id);

INSERT INTO User VALUES
 (1,'Alice','Smith','1234','alice@email.com','customer'),
 (2,'Bob','Brown','2345','bob@email.com','customer'),
 (3,'Carol','Jones','3456','carol@email.com','admin'),
 (4,'Dave','Lee','4567','dave@email.com','customer'),
 (5,'Eve','Davis','5678','eve@email.com','customer');

INSERT INTO Transaction_Categories VALUES
 (1,'Airtime','Top up'),
 (2,'Bills','Pay bills'),
 (3,'Transfer','Send money'),
 (4,'Cash Out','Withdraw money'),
 (5,'Merchant','Pay merchant');

INSERT INTO Transaction VALUES
 (1001,1,2,3,5000,'2025-09-17 10:00:00','completed'),
 (1002,2,3,2,2000,'2025-09-17 11:00:00','pending'),
 (1003,3,4,1,10000,'2025-09-17 12:00:00','failed'),
 (1004,4,5,4,1500,'2025-09-17 13:00:00','completed'),
 (1005,5,1,5,7500,'2025-09-17 14:00:00','completed');

INSERT INTO User_Transactions VALUES
 (1,1001,'sender'),
 (2,1001,'receiver'),
 (2,1002,'sender'),
 (3,1002,'receiver'),
 (3,1003,'sender'),
 (4,1003,'receiver'),
 (4,1004,'sender'),
 (5,1004,'receiver'),
 (5,1005,'sender'),
 (1,1005,'receiver');

INSERT INTO System_Logs VALUES
 (501,1001,'INFO','2025-09-17 10:01:00','Done.'),
 (502,1002,'WARN','2025-09-17 11:05:00','Pending.'),
 (503,1003,'ERROR','2025-09-17 12:10:00','Failed.'),
 (504,1004,'INFO','2025-09-17 13:05:00','Done.'),
 (505,1005,'INFO','2025-09-17 14:01:00','Done.');

-- CRUD EXAMPLES
INSERT INTO User VALUES (6,'Frank','Mills','6789','frank@email.com','customer');
SELECT * FROM Transaction WHERE status='completed';
UPDATE User SET phone_number='0000' WHERE user_id=2;
DELETE FROM System_Logs WHERE log_id=505;