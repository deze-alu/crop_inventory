import database
from inventory import Inventory, OversoldError

passed = 0
failed = 0


def check(label, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}")


def main():
    conn = database.get_connection()
    print(f"Connected to {database.DB_NAME} on {database.SERVER_CONFIG['host']}")

    database.create_tables(conn)
    inventory = Inventory(conn)

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = []
    for row in cursor.fetchall():
        tables.append(row[0])
    cursor.close()

    print("\nD1 - database and tables")
    check("crops table exists", "crops" in tables)
    check("sales table exists", "sales" in tables)

    print("\nD2 - Inventory class")
    crop_id = inventory.add("CHECK Maize", "2026-03-01", "2026-06-15", "Growing", 500)
    check("add returns a new crop id", isinstance(crop_id, int) and crop_id > 0)
    check("find returns the crop", inventory.find(crop_id).name == "CHECK Maize")
    check("find returns None for a missing crop", inventory.find(999999) is None)
    check("remaining starts at quantity planted", inventory.remaining(crop_id) == 500)

    inventory.record_sale(crop_id, 200)
    check("a sale reduces remaining", inventory.remaining(crop_id) == 300)
    check("sales_for returns the sale", len(inventory.sales_for(crop_id)) == 1)

    rejected = False
    try:
        inventory.record_sale(crop_id, 400)
    except OversoldError:
        rejected = True
    check("a sale larger than remaining is rejected", rejected)
    check("the rejected sale was not written", len(inventory.sales_for(crop_id)) == 1)
    check("remaining is unchanged after a rejection", inventory.remaining(crop_id) == 300)

    inventory.record_sale(crop_id, 300)
    check("selling the exact remaining amount is allowed", inventory.remaining(crop_id) == 0)

    inventory.update_field(crop_id, "status", "Harvested")
    check("update_field changes the column", inventory.find(crop_id).status == "Harvested")

    guarded = False
    try:
        inventory.update_field(crop_id, "crop_id; DROP TABLE crops", "x")
    except ValueError:
        guarded = True
    check("update_field rejects an unknown column", guarded)

    unsold_id = inventory.add("CHECK Beans", "2026-04-01", "2026-07-10", "Planted", 200)
    found = False
    for row in inventory.stock_report():
        if row[0] == unsold_id:
            found = row[3] == 0 and row[4] == 200
    check("stock report includes crops with no sales", found)

    inventory.run_statement(database.DELETE_SALES_FOR_CROP, (crop_id,))
    inventory.run_statement(database.DELETE_CROP, (crop_id,))
    inventory.run_statement(database.DELETE_CROP, (unsold_id,))
    check("check rows cleaned up", inventory.find(crop_id) is None)

    conn.close()
    print(f"\n{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
