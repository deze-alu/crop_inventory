from datetime import date

import db

CROP_COLUMNS = ("name", "planting_date", "harvest_date", "status", "quantity_planted")


class OversoldError(Exception):
    def __init__(self, crop_name, remaining):
        super().__init__(f"Only {remaining:.2f} of {crop_name} is in stock.")
        self.crop_name = crop_name
        self.remaining = remaining


class Inventory:
    def __init__(self, conn):
        self.conn = conn

    def run_query(self, sql, params=()):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def run_statement(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return new_id

    def all_crops(self):
        return self.run_query(db.SELECT_ALL_CROPS)

    def find(self, crop_id):
        rows = self.run_query(db.SELECT_CROP_BY_ID, (crop_id,))
        if not rows:
            return None
        return rows[0]

    def add(self, name, planting_date, harvest_date, status, quantity_planted):
        return self.run_statement(
            db.INSERT_CROP,
            (name, planting_date, harvest_date, status, quantity_planted),
        )

    def update_field(self, crop_id, column, value):
        if column not in CROP_COLUMNS:
            raise ValueError(f"Unknown crop column: {column}")
        self.run_statement(
            db.UPDATE_CROP_FIELD.format(column=column), (value, crop_id)
        )

    def remaining(self, crop_id):
        rows = self.run_query(db.SELECT_REMAINING_FOR_CROP, (crop_id,))
        if not rows:
            return 0
        return rows[0]["remaining"]

    def sales_for(self, crop_id):
        return self.run_query(db.SELECT_SALES_FOR_CROP, (crop_id,))

    def record_sale(self, crop_id, quantity_sold):
        crop = self.find(crop_id)
        if crop is None:
            raise ValueError(f"No crop with ID {crop_id}")
        remaining = self.remaining(crop_id)
        if quantity_sold > remaining:
            raise OversoldError(crop["name"], remaining)
        sale_date = date.today().isoformat()
        sale_id = self.run_statement(
            db.INSERT_SALE, (crop_id, quantity_sold, sale_date)
        )
        return {
            "sale_id": sale_id,
            "crop_id": crop_id,
            "quantity_sold": quantity_sold,
            "sale_date": sale_date,
        }

    def stock_report(self):
        return self.run_query(db.SELECT_STOCK_REPORT)
