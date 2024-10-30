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

    except Exception as e:
        print(f"An error has occured: {e}")

# Function to display a user-choosable number of rows
def display_rows(data):
    while True:
        numRows = len(data) - 1
        print("\nEnter number of rows to display:")
        print(f"- Enter a number between 1 and {numRows}")
        print("- To see all rows enter 'all'")
        print("- To skip, press Enter")
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

#This line will help us exit out of our options and code

#calling the CSV url file
#url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
url = 'sales_data_test.csv'
sales_data = load_csv(url)

# Main loop for the user
def main():
     while True:
          display_rows(sales_data)

#If this is the main program, call main()
if __name__ == "__main__":
     main()