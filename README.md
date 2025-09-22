# SOFTDEV - Week 1

Project: Personal Expense Tracker (Command-Line)

# Approach

# 1. Data Representation

- Used dictionaries to represent expense records and categories.

- Saved data into CSVs using `DictWriter` and read it back with `DictReader`.

# 2. Logical Database Design

- Maintained two CSV files:

  - `record.csv` → Stores expense records.

  - `categories.csv` → Stores available categories.

- This separation logically acts as a lightweight database.

- Categories are chosen from `categories.csv`; if a new category is entered, it is added automatically.

# 3. Record Management

- Used a composite key (`Date + Expense Name`) as the primary key to prevent duplicates.

- Each record contains: `Date`, `Expense_name`, `Expense_category`, `Expense_cost`.

# 4. Error Handling & Validation

- Learned and applied exception handling to make the app crash-free.

- Handled invalid cost inputs and incorrect date formats.

# 5. Core Functionality

- Add Expense → with category auto-add and date selection (today or custom).

- View Expenses / Categories → displayed neatly using `tabulate`.

- Summaries:
  - By Category.
  - By Month.
  - Highest Single Expense.
  - Filter by Date Range.

- Delete All Records → removes `record.csv`.

- Export → summaries saved into `.txt` files when the user chooses.

# Modules & Libraries Learned

- CSV Handling → `DictReader`, `DictWriter`.

- Time Handling → `datetime` for parsing/formatting and `time` for delays & clearing screen.

- `tabulate` → for structured output tables.

# Challenges Faced

- Designing the workflow of the project step by step.

- Coordinating between two CSV files (`record.csv` and `categories.csv`).

- Maintaining data consistency when adding new categories automatically.
