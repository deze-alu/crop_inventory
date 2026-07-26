import menu
from crop import Crop
from sales import Sale
from inventory import OversoldError


def view_inventory(inventory):
    crops = inventory.all_crops()
    if not crops:
        print("No crops recorded yet.")
        return
    print("\nID | Name | Planting date | Harvest date | Status | Quantity")
    for row in crops:
        crop = Crop.from_row(row)
        print(crop)


def add_crop(inventory):
    name = menu.get_text("Crop name: ")
    planting_date = menu.get_text("Planting date (YYYY-MM-DD): ")
    harvest_date = menu.get_text("Expected harvest date (YYYY-MM-DD): ")
    status = menu.get_text("Status (e.g. Planted): ")
    quantity = menu.get_number("Quantity planted: ")

    new_id = inventory.add(name, planting_date, harvest_date, status, quantity)
    print(f"Crop added successfully. Assigned ID: {new_id}")

