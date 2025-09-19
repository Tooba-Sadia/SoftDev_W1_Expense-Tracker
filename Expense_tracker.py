# Allow users to record, view, search, and analyze expenses
from tabulate import tabulate
def record(expenses, category_list):
    #add date

    print("Kindly enter your Expense details")
    print("Enter number to Choose Expense Category:", category_list)
    category_index = int(input())-1
    name = input("Enter Expense Name")
    cost = int(input("Enter Cost of the Expense")) #cost is int cuz we are counting in pakistani rupees

    expenses.append({'Expense_name':name,
                     'Expense_category':category_list[category_index].split('. ')[-1],
                     'Expense_cost':cost})
   

def view(expenses):
    
    print(tabulate(expenses,headers="keys",tablefmt='grid'))
    

def search(expenses,category_list):
    print("Select the key you want to search with")
    choice = int(input("Choose a number from the following \n1. Date 2. Category 3. Name "))
    match choice:
        case 1:
            pass
        case 2:
            category_i = int(input(f'Enter a number from the following to choose a category\n {category_list}'))-1
            for exp in expenses:
                if exp.get('Expense_category') == category_list[category_i]:
                    print(exp)
                    print(tabulate(exp,headers = 'keys',tablefmt = 'grid'))

        case 3:
            pass
    

def analyze():
    pass

'''def all_categories(new_category=''):
    category_list = ['Rent','Entertainment','Shopping','','Groceries','Travel','healthcare']
    if new_category:
        category_list.append()
    return category_list'''


import os
def menu():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux (POSIX systems)
    else:
        os.system('clear')
    print("Choose one of the following options:")
    print("1. Record an expense \n2. View Monthly Records \n3. Search for an expense{based on category,date}")
    print("4. Analyze your expenses based on categories")
def choose(expenses,category_list):
    choice = int(input())

    match choice:
        case 1:
            record(expenses,category_list)
        case 2:
            view(expenses)
        case 3:
            search(expenses,category_list)
        case 4:
            analyze()




expenses = [] #i'll use 2d lists for storage of items in the order [id, category, name, cost]
category_list = ['1. Rent','2. Entertainment','3. Shopping','4. Groceries','5. Travel','6. healthcare']




print("WELCOME TO MONTHLY EXPENSE TRACKER")
cont= ''
while cont != '0':
    menu()
    choose(expenses,category_list)
    cont = input("Enter any key to continue, Enter 0 to exit").strip().lower()




