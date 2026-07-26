Crop Inventory System
What this program does

This program helps a farmer keep track of the crops they've planted, the sales they've made, and how much stock of each crop remains. All records are saved to a database, so nothing is lost when the program is closed and reopened later.

How to run it

Make sure Python 3 is installed, and that the required database library is installed by running this once:

pip install mysql-connector-python

Then, from the project folder, start the program with:

python3 main.py

A menu will appear. The farmer never needs to type a command — they just type the number of the option they want and press Enter.

Note: this program stores its data in an online MySQL database (not a local SQLite file), so an internet connection is required to run it.

The menu
========= CROP INVENTORY SYSTEM =========
1. View inventory
2. Add crop
3. Update crop
4. Record sale
5. Calculate remaining stock
0. Exit
=========================================

1. View inventory — Shows every crop that has been recorded: its ID, name, planting date, harvest date, status, and quantity planted. If no crops have been added yet, it says so instead of showing an empty table.

2. Add crop — Asks for a crop's name, planting date, expected harvest date, status, and quantity planted. Once saved, it tells you the ID number the crop was given — this ID is needed later to update the crop or record a sale against it.

3. Update crop — Asks which crop (by ID) to change, shows its current details, then asks which single field to update (name, planting date, harvest date, status, or quantity). A Cancel option is available if you change your mind.

4. Record sale — Asks which crop was sold and how much. It first shows how much stock remains, so the farmer knows what's available. If the amount entered is more than what's in stock, the sale is refused and the farmer is told exactly how much is actually available — nothing incorrect gets saved.

5. Calculate remaining stock — Shows a summary for every crop: how much was planted, how much has been sold in total, and how much remains.

0. Exit — Closes the program.

Worked example
Choose 2. Add crop, and enter:
Name: Maize
Planting date: 2026-03-01
Harvest date: 2026-06-15
Status: Planted
Quantity planted: 500
The program confirms the crop was added and gives it an ID, e.g. 1.
Choose 4. Record sale, enter crop ID 1, and sell 150. The program records the sale.
Choose 5. Calculate remaining stock. The report shows Maize with 500 planted, 150 sold, and 350 remaining.
A note on the project's written plan

The project document mentions being able to remove crop records and search for specific crops, but these aren't in the current menu. This should be resolved as a team so the report and the running program agree — either by updating that section of the document, adding Delete/Search as menu options, or noting in the report that they're planned for a later version.
