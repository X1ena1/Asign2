import pandas as pd
import pyarrow
import ssl
import time
import sys

ssl._create_default_https_context = ssl._create_unverified_context
pd.set_option("display.max_columns", None)

#loading the CSV file
def load_csv(file_path):
    #attempting to read CSV file
    try:
        print(f"Reading CSV file...")
        start_time = time.time()
        sales_data = pd.read_csv(file_path, dtype_backend='pyarrow', on_bad_lines="skip")
        load_time = time.time() - start_time  #Calculating time it takes to load
        print(f"file loaded in {load_time:.2f} seconds")
        print(f"Number of rows: {len(sales_data)}")  #calculating the length of rows and returning the info
        print(f"Available columns: {sales_data.columns.to_list()}")

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


#calling the CSV url file
#url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
local_file = "sales_data_test.csv"
sales_data = load_csv(local_file)

#This is going to make sure that sales_data is aligned with None
if sales_data is not None:
    print(sales_data.head())
else:
    print(f"failed to load the CSV file {local_file}")