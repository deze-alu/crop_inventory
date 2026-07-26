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

