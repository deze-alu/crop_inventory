
# Each function follows the same pattern: ASK the farmer for input 
#(using menu.py's helpers), CALL a method on the Inventory object
#(which handles the database), then SHOW the result. 
#No SQL lives in this file - all database work happens inside inventory.py. This file only ever talks to the Inventory object


import menu
from crop import Crop
from sale import Sale
from inventory import OversoldError


# Menu option 1: View inventory.
def view_inventory(inventory):
    crops = inventory.all_crops()
    if not crops:
        print("No crops recorded yet.")
        return
    print("\nID | Name | Planting date | Harvest date | Status | Quantity")
    for row in crops:
        crop = Crop.from_row(row)
        print(crop)

#  Menu option 2: Add crop.
def add_crop(inventory):
    name = menu.get_text("Crop name: ")
    planting_date = menu.get_text("Planting date (YYYY-MM-DD): ")
    harvest_date = menu.get_text("Expected harvest date (YYYY-MM-DD): ")
    status = menu.get_text("Status (e.g. Planted): ")
    quantity = menu.get_number("Quantity planted: ")

    new_id = inventory.add(name, planting_date, harvest_date, status, quantity)
    print(f"Crop added successfully. Assigned ID: {new_id}")

#  Menu option 3: Update crop.
def update_crop(inventory):
    crop_id = int(menu.get_number("Enter the crop ID to update: "))
    row = inventory.find(crop_id)
    if row is None:
        print(f"No crop found with ID {crop_id}.")
        return

    crop = Crop.from_row(row)
    print("Current details:")
    print(crop)

    field_options = {
        "1": "name", "2": "planting_date", "3": "harvest_date",
        "4": "status", "5": "quantity_planted", "0": "Cancel",
    }
    choice = menu.show_menu("UPDATE WHICH FIELD?", field_options)
    if choice == "0":
        print("Update cancelled.")
        return

    column = field_options[choice]
    new_value = menu.get_text(f"New value for {column}: ")
    inventory.update_field(crop_id, column, new_value)
    print("Crop updated successfully.")

#  Menu option 4: Record sale.
def record_sale(inventory):
    crop_id = int(menu.get_number("Enter the crop ID to sell: "))
    row = inventory.find(crop_id)
    if row is None:
        print(f"No crop found with ID {crop_id}.")
        return

    print(f"Remaining stock: {inventory.remaining(crop_id)}")
    quantity_sold = menu.get_number("Quantity sold: ")

    try:
        sale = inventory.record_sale(crop_id, quantity_sold)
        print(f"Sale recorded. Sale ID: {sale['sale_id']}")
    except OversoldError as e:
        print(f"Cannot complete sale: {e}")
    except ValueError as e:
        print(f"Error: {e}")

#   Menu option 5: Calculate remaining stock.
def calculate_stock(inventory):
    report = inventory.stock_report()
    if not report:
        print("No crops recorded yet.")
        return
    print("\nID | Name | Planted | Sold | Remaining")
    for row in report:
        print(f"{row['crop_id']} | {row['name']} | {row['quantity_planted']} | {row['sold']} | {row['remaining']}")
