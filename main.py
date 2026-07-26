import mysql.connector

import database as db
import features
import menu
from inventory import Inventory

WELCOME = """
Welcome to the Crop Inventory System.

Track the crops you have planted, record your sales, and see how much of
each crop is still in stock. Your records are saved to the database, so
they are still here the next time you open the program.
"""

MENU_OPTIONS = {
    "1": "View inventory",
    "2": "Add crop",
    "3": "Update crop",
    "4": "Record sale",
    "5": "Calculate remaining stock",
    "0": "Exit",
}

ACTIONS = {
    "1": features.view_inventory,
    "2": features.add_crop,
    "3": features.update_crop,
    "4": features.record_sale,
    "5": features.calculate_stock,
}


def main():
    conn = None
    try:
        conn = db.get_connection()
        db.create_tables(conn)
        inventory = Inventory(conn)
        print(WELCOME)
        while True:
            choice = menu.show_menu("CROP INVENTORY SYSTEM", MENU_OPTIONS)
            if choice == "0":
                print("Goodbye!")
                break
            ACTIONS[choice](inventory)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()
