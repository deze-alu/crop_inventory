# Crop Inventory System — Work Breakdown

**Team:** Daniel Eze, Portia Mbiya Kamuala (Star), Taiwo Adedotun, Ntwali Brian, Eunice Iriza

## What we are building

A terminal program in Python that lets a farmer record the crops they have planted, log
the sales they make, and see how much of each crop is still in stock. Everything is saved
to a database file so the records are still there the next time the program is opened.

The farmer never types a command. They see a numbered menu, type a number, and the program
does that one job and brings them back to the menu.

```
========= CROP INVENTORY SYSTEM =========
1. View inventory
2. Add crop
3. Update crop
4. Record sale
5. Calculate remaining stock
0. Exit
=========================================
Choose an option:
```

## Ground rules

These apply to everyone, so nobody has to guess:

- **Python only.** One package needs installing — `pip install -r requirements.txt` gets
  the MySQL driver. Nothing else.
- **You need internet to run the program.** The database lives on Aiven Cloud, not on your
  laptop. Check this before the demo.
- **Terminal only.** No windows, no buttons, no web page.
- **No comments in the code.** Name things clearly instead. If a line needs a comment to be
  understood, rewrite the line.
- **One file per person where possible.** Two people editing the same file at the same time
  causes painful Git conflicts.
- **Small commits, pushed often.** A commit at the end of every work session, minimum.

## How the work splits

The program is built in three layers. This matters because it decides who can start when.

| Layer | What it does | Rule it follows |
|-------|--------------|-----------------|
| **Storage** | Talks to the database | Never uses `print()` or `input()` |
| **Screen** | Talks to the farmer | Never writes SQL |
| **Wiring** | Starts the program, runs the menu | Just connects the two |

Keeping `print()` out of the storage layer is not a style preference. It is what lets the
storage layer be checked automatically, and it is what stops two people's work from
colliding.

## What is in the repository right now

| File | State | Whose task |
|------|-------|-----------|
| `database.py` | **done** | D1 |
| `inventory.py` | **done** | D2 |
| `check_database.py` | **done** — run it to prove D1 and D2 still work | D1 / D2 |
| `docs/inventory-api.md` | **done** — read this before starting C or D | D3 |
| `crop.py`, `sale.py` | values done, `__str__` left to write | B |
| `menu.py` | empty, functions raise `NotImplementedError` | A |
| `features.py` | empty, functions raise `NotImplementedError` | C |
| `main.py` | empty, raises `NotImplementedError` | D |
| `README.md` | does not exist yet | H |

Every unwritten function raises `NotImplementedError` with the task letter in the message.
So if you run something and see that error, it is telling you which task still needs
doing — it is a signpost, not a bug.

---

## Assigned: Daniel Eze

These two are fixed. Everything else in the project depends on them, so they go to the
person who can move fastest on them. **Both are finished** — the rest of this section is
here so the team can see what was built and defend it in the report.

### D1 — Database connection and tables

Create `database.py`. It is the only file in the project that holds the connection details,
and it holds **every SQL query the program will ever run**, each one as a named constant.
No other file writes SQL text.

The database is MySQL on Aiven Cloud, in a database called `crop_db`.

- A function that connects to the Aiven server, creates `crop_db` if it does not exist
  yet, and returns a connection to it. Creating it automatically means nobody else on the
  team has to set anything up by hand.
- A function that creates the two tables if they do not already exist, so it is safe to
  call every single time the program starts.

Two tables:

```
crops                             sales
-----                             -----
crop_id           (auto number)   sale_id        (auto number)
name                              crop_id        (which crop was sold)
planting_date                     quantity_sold
harvest_date                      sale_date
status
quantity_planted
```

Sales live in their own table rather than just subtracting from a `quantity` column. That
keeps the history of every sale, so we can always answer "what did we sell and when".

**Done when:** connecting creates `crop_db` with both tables, and connecting a second time
does not fail or wipe anything.

### D2 — The Inventory class

Create `inventory.py`. This is the heart of the project. Every database query in the whole
program lives in this one file, and no other file writes SQL.

The class holds the connection and offers these methods:

| Method | Gives back |
|--------|-----------|
| `all_crops()` | every crop |
| `find(crop_id)` | one crop, or nothing if that ID does not exist |
| `add(name, planting_date, harvest_date, status, quantity)` | the ID the database assigned |
| `update_field(crop_id, column, value)` | nothing — changes one column |
| `remaining(crop_id)` | how much of that crop is still in stock |
| `sales_for(crop_id)` | every sale of that crop |
| `record_sale(crop_id, quantity)` | the new sale — **refuses if it is more than remaining stock** |
| `stock_report()` | planted / sold / remaining for every crop |

Two things to get right:

1. **Remaining stock is calculated, never stored.** It is the quantity planted minus
   everything sold. A crop that has never been sold must report its full quantity, not a
   blank.
2. **A sale bigger than remaining stock is rejected.** Nothing gets written, and the caller
   is told why. Selling 400kg of a crop with 300kg left is a typing mistake, and recording
   it would make every later number wrong.

**Done when:** the methods work and the oversell rule holds.

### D3 — Publish the method list on day one *(do this first)*

Before writing any of D2, write the method names and what each one takes and gives back,
and post it in the group chat.

This unblocks everybody. Whoever takes the screen tasks can write their code against that
list while D2 is still being built. Without it, three people sit idle waiting for you.

**Done:** it is written up in `docs/inventory-api.md`. Anyone taking task C or D should
read that page and can start immediately — you do not need to understand SQL or MySQL to
use the Inventory class.

---

## Open for anyone to pick

**Nothing below is assigned.** Read them, pick what you want, then put your name in the
Taken by column and say so in the group chat so two people do not start the same thing.

Take one to start. When it is done, come back and take another. It is completely fine to
pick a starred-once task first and build up.

| # | Task | Difficulty | Taken by |
|---|------|-----------|----------|
| A | Menu and input helpers | ★★ | |
| B | The Crop and Sale classes | ★ | |
| C | The five screen features | ★★★ | |
| D | Main program wiring | ★★ | |
| E | Test the finished program | ★ (no coding) | |
| F | Workflow diagram | ★ (no coding) | |
| G | GitHub repository setup | ★ | |
| H | README and user guide | ★ (no coding) | |

### A — Menu and input helpers ★★

Create `menu.py`. Three small functions, and none of them mention crops at all — this file
would work just as well in a hospital booking program.

- **Show a menu and get a valid answer.** Print a title, print each numbered option, ask
  the farmer to choose. If they type something that is not on the menu, say
  `Invalid option, please try again.` and ask again. Do not give up, do not crash.
- **Ask for text.** Keep asking until they type something that is not blank.
- **Ask for a number.** Keep asking until they type something that really is a number.
  Typing `abc` where a quantity belongs must not crash the program.

You are mostly writing `print()`, `input()`, `if`, and `while`. The one idea to get
comfortable with is a loop that only ends when the answer is acceptable.

**Why it matters:** this is the file that stops the program crashing when a farmer
mistypes. Every other feature depends on it. It is also reused by the update submenu, so
you write the menu logic once and it serves two menus.

**Done when:** a bad menu choice, a blank name, and the word `abc` typed at a quantity
prompt all re-ask instead of crashing.

### B — The Crop and Sale classes ★

`crop.py` and `sale.py` already exist and already hold the values, because the Inventory
class needs them to work. What is missing in both is the `__str__` method — right now it
raises `NotImplementedError` and tells you to read this page.

Your job is to replace that with the line of text that appears in the table:

- `Crop` should print as: ID, name, planting date, harvest date, status, quantity.
- `Sale` should print as: sale ID, date, quantity sold.

The trick is making the columns line up no matter how long the crop name is. Python does
this for you with a width in the placeholder — `f"{name:<18}"` pads to 18 characters on
the left, `f"{quantity:>10.2f}"` pads to 10 on the right with 2 decimal places. Play with
the numbers until a few rows look tidy underneath each other.

**Why it matters:** every table in the program prints one of these per row, so getting it
right once makes three different screens look correct. It is also a real requirement from
our project definition document (*"a class that describes the farmer's produce"*).

**Done when:** printing several crops one after another gives neat columns, and the same
for sales.

### C — The five screen features ★★★

Create `features.py`. One function per menu option. Each one asks the farmer for what it
needs, calls the Inventory class, and prints the result. **No SQL in this file.**

1. **View inventory** — print every crop as a table. If there are none, say
   `No crops recorded yet.`
2. **Add crop** — ask for the five details, save it, tell the farmer what ID it got.
3. **Update crop** — ask which crop, show it, then show a *second small menu* asking which
   field to change. Change just that one. Include a Cancel option.
4. **Record sale** — ask which crop, show how much is left, ask how much was sold. If the
   Inventory class rejects it, print why and go back to the menu.
5. **Calculate remaining stock** — print planted, sold, and remaining for every crop.

This is the biggest task, and it depends on tasks A, B, and D2. Take it if you want the
most Python practice, and expect to pair with whoever took A.

**Done when:** all five work and none of them crash on a bad crop ID.

### D — Main program wiring ★★

Create `main.py`. It should be short — around 60 lines — and reading it top to bottom
should explain the whole program.

- The welcome message the farmer sees on startup.
- The menu options as a list.
- A dictionary that connects each menu number to its feature function.
- The main loop: show the menu, do the chosen thing, come back, repeat until they pick 0.
- Close the database connection cleanly on the way out, even if something went wrong.

**Why a dictionary instead of a long `if`/`elif` chain:** adding a seventh menu option later
becomes one new line instead of a new branch, and the numbers cannot get out of step with
what actually runs.

**Done when:** the program runs start to finish, and choosing 0 closes it politely.

### E — Test the finished program ★ *(no coding)*

Write a test plan, run it, and record what actually happened. This is a real
deliverable — our report needs evidence that we tested, not a claim that we did.

Build a table: what you did, what you expected, what happened. Include the awkward cases,
because those are the ones that find bugs:

- Choose an option that is not on the menu.
- View the inventory when it is completely empty.
- Ask to update a crop ID that does not exist.
- **Try to sell more than is in stock.** This must be refused.
- Type letters where a number belongs.
- Close the program, open it again, and check the crops are still there.

That last one is the one that proves the database is actually working. Report anything
that fails to the person who wrote that file — finding a bug is the job, not a problem.

**Done when:** the table is filled in with real observed results and pasted into the report.

### F — Workflow diagram ★ *(no coding)*

Our Section 3 needs an architectural/workflow diagram, and right now we do not have one.

Draw the path through the program: launch → connect to database → welcome screen → main
menu → each of the six options → back to the menu → exit. Show the update submenu branching
off option 3, and show the rejected-sale path branching off option 4.

Draw.io, Figma, Google Slides, or clear handwriting and a photo are all fine. Export it as
an image and put it in the report.

**Done when:** someone who has never seen the code can follow the diagram and predict what
the program does.

### G — GitHub repository setup ★

We are listing Git and GitHub as project resources and we do not have a repository yet.

- Create the repository and add all five of us as collaborators.
- Add a `.gitignore` that ignores `__pycache__/`. It is generated by running the program,
  and committing it causes constant pointless conflicts.
- Write a short note in the group chat on how to clone, pull before starting, and push when
  done — most of the team has not used Git on a shared project before.

**Done when:** everyone has cloned it and pushed at least one commit successfully.

### H — README and user guide ★ *(no coding)*

Write the `README.md` that sits at the top of the repository. Assume the reader is a farmer
or a marker, not a programmer.

- What the program does, in three sentences.
- How to run it: `pip install -r requirements.txt` once, then `python3 main.py`. Say plainly
  that internet is required, because the database is on Aiven Cloud.
- What each menu option does, one short paragraph each.
- A worked example: add a crop, record a sale, check the remaining stock.

**Done when:** someone outside the team can run the program using only the README.

---

## Order of work

```
Day 1   D3  method list posted  ────────────┐
        G   repository set up               │  everyone can start
        F   diagram (independent)           │
                                            ▼
Day 2   D1  database  ──►  D2  Inventory
        A   menu helpers        B   classes
                    │           │
                    └─────┬─────┘
Day 3                     ▼
                    C   features  ──►  D   wiring
                                            │
Day 4                                       ▼
                                    E   testing  ──►  H  README
```

Tasks F, G, and H depend on nothing and can be done at any point. Whoever finishes early
should pick one of those up rather than waiting.

## One decision we still need to make

Our submitted project document says users will be able to *"remove crop records that are no
longer needed"* and *"search for specific crops"*. Our menu has six options and neither of
those is on it. The two documents contradict each other and a marker reading both will
notice.

Three ways out, and we should agree before we write the report:

1. Keep the six-option menu and edit that paragraph of the document to match.
2. Add Delete and Search as options 6 and 7. Delete needs a decision first: what happens to
   the sales records attached to a crop that gets deleted?
3. Leave both and say in the report that Delete and Search are planned for a later version.

Option 1 is the least work and the easiest to defend.

## Definition of done for the whole project

- The program runs with `python3 main.py` on a machine that has only plain Python.
- All six menu options work.
- Bad input never crashes it.
- A sale larger than remaining stock is refused.
- Closing and reopening the program keeps all the data.
- Everything is pushed to GitHub, with commits from all five of us.
- The report has the diagram, the test results table, and everyone's contribution recorded.
