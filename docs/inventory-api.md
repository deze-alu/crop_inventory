# The Inventory class — what you can call

**For:** whoever picks task C (the five screen features) or task D (main wiring).
**Status:** done and checked. You can write against this now.

You do not need to understand the database, SQL, or MySQL to use this. You need this page.

## Getting one

`main.py` (task D) makes it once at startup and hands the same one to every feature:

```python
import database
from inventory import Inventory

conn = database.get_connection()
database.create_tables(conn)
inventory = Inventory(conn)
```

Every feature function takes that object as its only argument:

```python
def view_inventory(inventory):
    crops = inventory.all_crops()
```

## The methods

### `all_crops()`

Every crop, oldest first. Gives back a list of `Crop` objects. An empty list if there are
none — not `None`, so `if not crops:` is the check for "nothing recorded yet".

### `find(crop_id)`

One `Crop`, or `None` if no crop has that ID. **Always check for `None`** — this is how
you print `Crop not found.` instead of crashing.

```python
crop = inventory.find(crop_id)
if crop is None:
    print("Crop not found.")
    return
```

### `add(name, planting_date, harvest_date, status, quantity_planted)`

Saves a new crop. Gives back the ID number the database assigned. Tell the farmer that
number — they need it to update or sell that crop later.

```python
crop_id = inventory.add("Maize", "2026-03-01", "2026-06-15", "Growing", 500)
print(f"Added Maize with crop ID {crop_id}.")
```

### `update_field(crop_id, column, value)`

Changes one column on one crop. Gives back nothing.

`column` must be one of exactly these five spellings:

```
name    planting_date    harvest_date    status    quantity_planted
```

Anything else raises `ValueError`. That is deliberate — it stops a typo from reaching the
database.

### `remaining(crop_id)`

How much of that crop is still in stock: everything planted minus everything sold. A crop
that has never been sold gives back its full quantity.

### `sales_for(crop_id)`

Every sale of that crop, oldest first. A list of `Sale` objects, empty if it has never
been sold.

### `record_sale(crop_id, quantity_sold)`

Logs a sale and gives back the new `Sale`.

**It refuses a sale bigger than what is in stock** by raising `OversoldError`. You must
catch it:

```python
from inventory import OversoldError

try:
    sale = inventory.record_sale(crop_id, quantity_sold)
except OversoldError as err:
    print(f"Sale rejected. {err}")
    return

print(f"Sale {sale.sale_id} recorded on {sale.sale_date}.")
```

`err` already reads *"Only 300.00 of Maize is in stock."* so printing it directly is
enough. If you want to build your own wording, `err.crop_name` and `err.remaining` are
there.

### `stock_report()`

The data for the "Calculate remaining stock" screen. A list of plain tuples, one per crop:

```python
for crop_id, name, planted, sold, remaining in inventory.stock_report():
    print(f"{crop_id}  {name}  {planted}  {sold}  {remaining}")
```

Crops with no sales appear with `sold` as `0`, not blank.

## What the objects hold

```
Crop                        Sale
----                        ----
crop.crop_id                sale.sale_id
crop.name                   sale.crop_id
crop.planting_date          sale.quantity_sold
crop.harvest_date           sale.sale_date
crop.status
crop.quantity_planted
```

Printing a `Crop` or a `Sale` directly is **task B** and is not written yet. Until it is,
reach for the values by name as above.

## Two rules

1. **No SQL in `features.py` or `main.py`.** If you find yourself wanting to write a query,
   the method you need is missing — ask Daniel to add it rather than writing SQL in the
   screen layer.
2. **Every method can raise `mysql.connector.Error`** if the internet drops or Aiven is
   unreachable. Task D catches that once around the whole menu loop, so individual
   features do not need to.
