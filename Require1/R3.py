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
        required_columns = ['quantity', 'order_date', 'unit_price']
        
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
    print("Exiting Program, Thank you.").strip().lower()
    sys.exit(0)

#Testing the different analysis from the list
def display_menu(data):
        menu_options = (
             ("Show the first n rows of sales data", display_rows),
             ("Total sales by region and order type", sales_by_region),
             ("Exit", exit_program),
        )
        
        print("\nPlease choose from among these options:")
        for index, (description, _) in enumerate(menu_options):
             print(f"{index+1}: {description}")

        num_choices = len(menu_options)
        choice = int(input(f"Select an option between 1 and {num_choices}: "))

        if 1 <= choice <= num_choices:
            action = menu_options[choice-1][1]
            action(data)
        else:
            print("Invalid input. Please re-enter.")


#This following line will represent the totla sales by region and orde type
def sales_by_region(data):
    pivot_table = pd.pivot_table(data, index='sales_region', columns="order_type",
                                 values='quantity', aggfunc='sum', fill_value=0)
    
    print(f"The total sales by region and order type: ")
    print(pivot_table)

#calling the CSV url file
url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
#url = 'sales_data_test.csv'
sales_data = load_csv(url)
    
# Main loop for the user
def main():
    if sales_data is not None: #Chatgbt helped me to properly refernce the main menu
        while True:
            display_menu(sales_data)

#If this is the main program, call main()
if __name__ == "__main__":
    main()