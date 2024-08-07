import mysql.connector

# MySQLへの接続
conn = mysql.connector.connect(
    host='0.0.0.0',
    user='nerv',
    password='nervDatabase',
    database='nerv_database'
)
cursor = conn.cursor()

# テーブルの作成
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
)
""")

conn.commit()
cursor.close()
conn.close()
