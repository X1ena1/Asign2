import pandas as pd
import pyarrow
import ssl
import time
import sys

ssl._create_default_https_context = ssl._create_unverified_context

#Set to display the max columns
pd.set_option("display.max_columns", None)

#loading the CSV file
def load_csv(file_path):
    #attempting to read CSV file
    try:
        print(f"Reading CSV file: {file_path}")
        start_time = time.time()
        sales_data = pd.read_csv(file_path, dtype_backend='pyarrow', on_bad_lines="skip")
        load_time = time.time() - start_time  #Calculating time it takes to load
        print(f"file loaded in {load_time:.2f} seconds")
        print(f"Number of rows: {len(sales_data)}")  #calculating the length of rows and returning the info
        #print(f"Available columns: {sales_data.columns.to_list()}")
        
        #list of required columns
        required_columns = ['quantity', 'order_date', 'unit_price', 'sale_price']
        
        #Check for missing columns
        missing_columns = [col for col in required_columns if col not in sales_data.columns]

        if missing_columns:
            print(f"\nWarning: The following enquired columns are missing: {missing_columns}")
        else:
            print(f"\nALL required columns are present")

        #replacing any missing data with 0's (ChatGbt Helped)
        sales_data.fillna(0, inplace=True)

        return sales_data
    
    except FileNotFoundError:
        print(f"Error: the file {file_path} was not found.")
    except pd.errors.EmptyDataError as e:
        print(f"Error: the file {file_path} was empty.")
    except pd.errors.ParserError as e:
        print(f"Error: there was a problem parsing {file_path}.")
    except Exception as e:
        print(f"An error has occured: {e}")

# Function to display a user-choosable number of rows
def display_rows(data):
    while True:
        numRows = len(data) - 1
        print("\nEnter number of rows to display:")
        print(f"- Enter a number between 1 and {numRows}")
        print("- To see all rows enter 'all'")
        print("- To skip preview, press Enter")
        user_choice = input("Your choice: ").strip().lower()

        if user_choice == '':
            print("Skipping preview")
            break
        elif user_choice == 'all':
            print(data)
            break
        elif user_choice.isdigit() and 1 <= int(user_choice) <= numRows:
            print(data.head(int(user_choice)))
            break
        else:
            print("Invalid input. Please re-enter.")

#Cleanly Exit the Program
def exit_program(data):
    print("Exiting Program, Thank you.")
    sys.exit(0)

#Testing the different analysis from the list
def display_menu(data):
        menu_options = (
             ("Show the first n rows of sales data", display_rows),
             ("Total sales by region and order type", sales_by_region),
             ("Average sales by region with average sales by state and sale type", sales_state_region),
             ("Sales by customer type and order type by state", customer_state),
             ("Total sales quantity and price by region and product", sales_region_product),
             ("Total sales quantity and price customer type", sales_quantity_type),
             ("Max and min sales price of sales by category", max_min_sales),
             ("Number of unique employees by region", unique_employees),
             ("Exit", exit_program),
        )
        
        print("\nSales Data Dashboard:")
        for index, (description, _) in enumerate(menu_options):
             print(f"{index+1}: {description}")

        num_choices = len(menu_options)

        while True:
            try:
                choice = int(input(f"Select an option between 1 and {num_choices}: "))
                if 1 <= choice <= num_choices:
                    action = menu_options[choice-1][1]
                    action(data)
                else:
                    print("Invalid input. Please re-enter.")
            except ValueError:
                print(f"Invalid Input. Please enter a number")


#This following line will represent the totla sales by region and order type
def sales_by_region(data):
    pivot_table = pd.pivot_table(data, index='sales_region', columns="order_type",
                                 values='quantity', aggfunc='sum', fill_value=0)
    
    print("\nThe total sales by region and order type: ")
    print(pivot_table)

#The following line will represent how to create a pivot for sales by region
def sales_state_region(data):
    pivot_table = pd.pivot_table(data, index='sales_region', columns=['customer_state', 'order_type'],
                                 values='quantity', aggfunc='mean', fill_value=0)
    
    print("\nThe average sales by region with average sales by state and sale type:")
    print(pivot_table)

#The following code will make a pivot from customers by their order type by state
def customer_state(data):
    pivot_table = pd.pivot_table(data, index=['customer_type', 'customer_state'], columns='order_type',
                                 values='quantity', aggfunc='sum', fill_value=0)
    
    print("\nSales by customer type and order type by state:")
    print(pivot_table)

#The following is going to create a pivot that sums the quantity and sales per row,
#  by order & customer
def sales_region_product(data):
    pivot_table = pd.pivot_table(data, index='sales_region', columns='product_category', values=['order_type', 'sale_price'],
                                 aggfunc='sum', fill_value=0)
    
    print("\nSales by region and product:")
    print(pivot_table)

#The following line will create a pivot thar shows slaes by order, product, and sum the quantity and sales
def sales_quantity_type(data):
    pivot_table = pd.pivot_table(data, index=['order_type', 'customer_type'], values=['quantity', 'sale_price'],
                                 aggfunc='sum', fill_value=0)
    
    print("\nTotal sales quantity and price by customer type:")
    print(pivot_table)

#The following line will make a pivot finding the max and min from sales category
def max_min_sales(data):
    pivot_table = pd.pivot_table(data, index='product_category', values='sale_price',
                                 aggfunc=['max', 'min'], fill_value=0)
    
    print("\nMax and min sales price of sales by category")
    print(pivot_table)

#The following line will create a pivot to show employees by region and count the unique
def unique_employees(data):
    pivot_table = pd.pivot_table(data, index='sales_region', values='employee_id',
                                 aggfunc=pd.Series.nunique, fill_value=0)
    
    print("\nNumber of unique employees by region")
    print(pivot_table)

#calling the CSV url file
#url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
url = 'sales_data.csv'
sales_data = load_csv(url)
    
# Main loop for the user
def main():
    if sales_data is not None: #Chatgbt helped me to properly refernce the main menu
        while True:
            display_menu(sales_data)

#If this is the main program, call main()
if __name__ == "__main__":
    main()