import mysql.connector

SERVER_CONFIG = {
    "host": "learning-mysql-alustudent-a25f.i.aivencloud.com",
    "port": 23599,
    "user": "avnadmin",
    "password": "AVNS_mxriphi9vjw-b6LFuw6",
    "ssl_disabled": False,
}

DB_NAME = "crop_db"

CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS crop_db"

CREATE_CROPS_TABLE = """
    CREATE TABLE IF NOT EXISTS crops (
        crop_id          INT AUTO_INCREMENT PRIMARY KEY,
        name             VARCHAR(100) NOT NULL,
        planting_date    VARCHAR(20),
        harvest_date     VARCHAR(20),
        status           VARCHAR(50),
        quantity_planted DOUBLE
    )
"""

CREATE_SALES_TABLE = """
    CREATE TABLE IF NOT EXISTS sales (
        sale_id       INT AUTO_INCREMENT PRIMARY KEY,
        crop_id       INT NOT NULL,
        quantity_sold DOUBLE NOT NULL,
        sale_date     VARCHAR(20),
        FOREIGN KEY (crop_id) REFERENCES crops (crop_id)
    )
"""

SELECT_ALL_CROPS = """
    SELECT crop_id, name, planting_date, harvest_date, status, quantity_planted
    FROM crops
    ORDER BY crop_id
"""

SELECT_CROP_BY_ID = """
    SELECT crop_id, name, planting_date, harvest_date, status, quantity_planted
    FROM crops
    WHERE crop_id = %s
"""

INSERT_CROP = """
    INSERT INTO crops (name, planting_date, harvest_date, status, quantity_planted)
    VALUES (%s, %s, %s, %s, %s)
"""

UPDATE_CROP_FIELD = """
    UPDATE crops
    SET {column} = %s
    WHERE crop_id = %s
"""

DELETE_CROP = """
    DELETE FROM crops
    WHERE crop_id = %s
"""

SELECT_REMAINING_FOR_CROP = """
    SELECT c.quantity_planted - COALESCE(SUM(s.quantity_sold), 0) AS remaining
    FROM crops c
    LEFT JOIN sales s ON c.crop_id = s.crop_id
    WHERE c.crop_id = %s
    GROUP BY c.crop_id
"""

SELECT_SALES_FOR_CROP = """
    SELECT sale_id, crop_id, quantity_sold, sale_date
    FROM sales
    WHERE crop_id = %s
    ORDER BY sale_id
"""

INSERT_SALE = """
    INSERT INTO sales (crop_id, quantity_sold, sale_date)
    VALUES (%s, %s, %s)
"""

DELETE_SALES_FOR_CROP = """
    DELETE FROM sales
    WHERE crop_id = %s
"""

SELECT_STOCK_REPORT = """
    SELECT c.crop_id,
           c.name,
           c.quantity_planted,
           COALESCE(SUM(s.quantity_sold), 0) AS sold,
           c.quantity_planted - COALESCE(SUM(s.quantity_sold), 0) AS remaining
    FROM crops c
    LEFT JOIN sales s ON c.crop_id = s.crop_id
    GROUP BY c.crop_id, c.name, c.quantity_planted
    ORDER BY c.crop_id
"""


def get_connection():
    server = mysql.connector.connect(**SERVER_CONFIG)
    cursor = server.cursor()
    cursor.execute(CREATE_DATABASE)
    cursor.close()
    server.close()
    return mysql.connector.connect(database=DB_NAME, **SERVER_CONFIG)


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(CREATE_CROPS_TABLE)
    cursor.execute(CREATE_SALES_TABLE)
    conn.commit()
    cursor.close()
