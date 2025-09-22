# Expense Tracker Program
# Handles adding, viewing, summarizing, and filtering expenses with CSV storage.

import csv
import os
from datetime import date, datetime
import time
from tabulate import tabulate

################################################################
# Add a record (expense or category) to CSV
def add_to_csv(record, csv_name):
    try:
        file_exists = os.path.exists(csv_name)
        is_empty = not file_exists or os.path.getsize(csv_name) == 0  # Check if file is empty

        with open(csv_name, 'a', newline='') as f:
            # Decide header fields based on file type
            if "categories" in csv_name:
                fieldnames = ["Category_name"]
            else:
                fieldnames = ["Date", "Expense_name", "Expense_category", "Expense_cost"]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if is_empty:  # Write header only once
                writer.writeheader()
            writer.writerow(record)
            
    except Exception as e:
        print(f"Error writing to file: {e}")

################################################################
# Load all records from a CSV file
def load_from_csv(csv_name):
    records = []
    try:
        if not os.path.exists(csv_name):  # If no file, return empty
            return records
        with open(csv_name, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for line in reader:
                records.append(line)
        return records
    except Exception as e:
        print(f"Error reading from file: {e}")
        return records

################################################################
# View all expenses in a table
def view(csv_name):
    try:
        expenses = load_from_csv(csv_name)
        if expenses:
            print(tabulate(expenses, headers="keys", tablefmt='grid'))
        else:
            print("No expenses found.")
    except Exception as e:
        print(f"Error displaying data: {e}")

################################################################
# Add a new expense record
def new_record(csv_name, categories_csv):
    try:
        print("ADDING A NEW EXPENSE:")

        # Get name and cost
        name = input("Enter Expense Name >>>").strip().lower()
        try:
            cost = int(input("Enter Cost of the Expense >>>"))
        except ValueError:
            print("Invalid cost entered. Please enter a number.")
            return
        
        # Show categories before asking
        category_list = get_categories(categories_csv)
        if category_list:
            print("Choose from the following Categories or add a new category:")
            print(tabulate(category_list, headers="keys", tablefmt='grid'))     
        category_name = input("Enter category name >>>").strip().lower()

        # Auto add category if it doesn’t exist
        add_category_auto(categories_csv, category_name)

        # Date input
        print("\nDate Options:")
        print("1. Use today's date")
        print("2. Enter custom date")
        date_choice = input("Choose date option (1 or 2): ").strip()
        
        if date_choice == '1':
            expense_date = date.today().strftime("%Y-%m-%d")
        elif date_choice == '2':
            while True:
                try:
                    custom_date = input("Enter date (YYYY-MM-DD format): ").strip()
                    datetime.strptime(custom_date, "%Y-%m-%d")  # Validate
                    expense_date = custom_date
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD (e.g., 2024-12-25)")
        else:
            expense_date = date.today().strftime("%Y-%m-%d")

        # Create record
        record = {'Date': expense_date,
                  'Expense_name': name,
                  'Expense_category': category_name,              
                  'Expense_cost': cost}
        
        # Prevent duplicates by checking Date + Expense_name
        old_records = load_from_csv(csv_name)
        duplicate_exists = any(
            r.get('Date') == expense_date and 
            r.get('Expense_name') == name
            for r in old_records
        )
        
        if not duplicate_exists:
            add_to_csv(record, csv_name)
            print("Expense record added successfully!")
        else:
            print(f"Duplicate record! Expense '{name}' already exists on {expense_date}.")

    except Exception as e:
        print(f"Error adding new record: {e}")

################################################################
# Automatically add category if missing
def add_category_auto(categories_csv, new_ctgry):
    try:
        existing = get_categories(categories_csv)
        existing_names = [c.get('Category_name', '').lower() for c in existing if isinstance(c, dict)]
        if new_ctgry not in existing_names:
            category = {'Category_name': new_ctgry.strip().lower()}
            add_to_csv(category, categories_csv)
    except Exception as e:
        print(f"Error adding category automatically: {e}")

################################################################
# Manually add new category
def add_category(categories_csv):
    try:
        new_ctgry = input("Add new category>>").strip().lower()
        existing = get_categories(categories_csv)
        existing_names = [c.get('Category_name', '').lower() for c in existing if isinstance(c, dict)]
        if new_ctgry not in existing_names:
            category = {'Category_name': new_ctgry}
            add_to_csv(category, categories_csv)
            print(f"Category '{new_ctgry}' added.")
        else:
            print(f"Category '{new_ctgry}' already exists.")
    except Exception as e:
        print(f"Error adding category: {e}")

################################################################
# Get all categories
def get_categories(categories_csv):
    try:
        return load_from_csv(categories_csv)
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []

################################################################
# Delete all records (reset file)
def delete_all_records(csv_name):
    try:
        if os.path.exists(csv_name):
            os.remove(csv_name)
            print(f"All records deleted from {csv_name}.")
        else:
            print(f"No records found to delete in {csv_name}.")
    except Exception as e:
        print(f"Error deleting records: {e}")

################################################################
# Clear console after 2 seconds
def clear_screen():
    time.sleep(2)
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS/Linux
        os.system('clear')

################################################################
# Summary of expenses by category
def summary_by_category(csv_name):
    try:
        expenses = load_from_csv(csv_name)
        if not expenses:
            print("No expenses found.")
            return
        
        category_summary = {}
        for exp in expenses:
            category = exp.get('Expense_category', 'Uncategorized')
            cost = int(exp.get('Expense_cost', 0))
            category_summary[category] = category_summary.get(category, 0) + cost        

        summary_list = [{'Category': k, 'Total Expense': v} for k, v in category_summary.items()]
        table = tabulate(summary_list, headers="keys", tablefmt='grid')
        print(table)

        # Ask user if they want to save
        choice = input("Save summary to file? (y/n): ").strip().lower()
        if choice == 'y':
            with open('category_summary.txt', 'w', encoding='utf-8') as f:
                f.write(table)
            print("Summary saved to category_summary.txt")

    except Exception as e:
        print(f"Error generating summary: {e}")

################################################################
# Summary of expenses by month
def summary_by_month(csv_name):
    try:
        expenses = load_from_csv(csv_name)
        if not expenses:
            print("No expenses found.")
            return
        month_summary = {}
        for exp in expenses:
            try:
                dt = datetime.strptime(exp.get('Date', ''), "%Y-%m-%d")
                month = dt.strftime("%Y-%m")
            except ValueError:
                month = "Unknown"
            cost = int(exp.get('Expense_cost', 0))
            month_summary[month] = month_summary.get(month, 0) + cost

        summary_list = [{'Month': k, 'Total Expense': v} for k, v in month_summary.items()]
        table = tabulate(summary_list, headers="keys", tablefmt='grid')
        print(table)

        # Ask to save
        choice = input("Save summary to file? (y/n): ").strip().lower()
        if choice == 'y':
            with open('monthly_summary.txt', 'w', encoding='utf-8') as f:
                f.write(table)
            print("Summary saved to monthly_summary.txt")

    except Exception as e:
        print(f"Error generating summary: {e}")

################################################################
# Show highest expense
def highest_expense(csv_name):
    try:
        expenses = load_from_csv(csv_name)
        if not expenses:
            print("No expenses found.")
            return

        max_exp = expenses[0]  # Start with first record
        max_cost = int(max_exp.get('Expense_cost', 0))

        for exp in expenses[1:]:  # Compare others
            cost = int(exp.get('Expense_cost', 0))
            if cost > max_cost:
                max_cost = cost
                max_exp = exp

        print("\nHighest Single Expense:")
        print(tabulate([max_exp], headers="keys", tablefmt="grid"))

    except Exception as e:
        print(f"Error finding highest expense: {e}")

################################################################
# Filter expenses by a date range
def filter_by_date_range(csv_name):
    try:
        expenses = load_from_csv(csv_name)
        if not expenses:
            print("No expenses found.")
            return
        
        # Get start and end
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")
            return
        
        filtered = []
        for exp in expenses:
            try:
                dt = datetime.strptime(exp.get('Date', ''), "%Y-%m-%d")
                if start_dt <= dt <= end_dt:
                    filtered.append(exp)
            except ValueError:
                continue
        
        if filtered:
            print("\nExpenses in selected date range:")
            print(tabulate(filtered, headers="keys", tablefmt="grid"))
        else:
            print("No expenses found in this range.")

    except Exception as e:
        print(f"Error filtering by date range: {e}")

################################################################
# Main menu
def main():
    csv_name = 'record.csv'
    categories_csv = 'categories.csv'

    print("Welcome to Expense Tracker!")

    while True:
        print("\n" + "="*40)
        print("EXPENSE TRACKER MENU")
        print("="*40)
        print("1. Add new expense")
        print("2. View all expenses")
        print("3. Add new category")
        print("4. View all categories")
        print("5. Delete All records")
        print("6. Summary by Category")
        print("7. Summary by Month")
        print("8. Highest Single Expense")
        print("9. Filter Expenses by Date Range")
        print("10. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == '1':
            new_record(csv_name, categories_csv)
            clear_screen()
        elif choice == '2':
            view(csv_name)
        elif choice == '3':
            add_category(categories_csv)
            clear_screen()
        elif choice == '4':
            categories = get_categories(categories_csv)
            if categories:
                print("Available Categories:")
                print(tabulate(categories, headers="keys", tablefmt='grid'))
                clear_screen()
            else:
                print("No categories found.")
        elif choice == '5':
            confirm = input("Are you sure you want to delete all records? Type 'yes' to confirm: ").strip().lower()
            if confirm == 'yes':
                delete_all_records(csv_name)  
            else:
                print("Deletion cancelled.")
            clear_screen()
        elif choice == '6':
            summary_by_category(csv_name)
        elif choice == '7':
            summary_by_month(csv_name)
        elif choice == '8':
            highest_expense(csv_name)
        elif choice == '9':
            filter_by_date_range(csv_name)
        elif choice == '10':
            print("Thank you for using Expense Tracker! Goodbye!")
            clear_screen()
            break
        else:
            print("Invalid choice. Please enter a number between 1-10.")

# Run program
main()
