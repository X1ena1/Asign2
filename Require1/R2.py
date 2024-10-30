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
        print(f"Reading CSV file: {file_path}")
        start_time = time.time()
        sales_data = pd.read_csv(file_path, dtype_backend='pyarrow', on_bad_lines="skip")
        load_time = time.time() - start_time
        print(f"file loaded in {load_time:.2f} seconds")
        print(f"Number of rows: {len(sales_data)}")
        
        #We are displaying the available columns from the DATA
        print(f"Available columns: {sales_data.columns.to_list()}")

        #Inputting the columns we are wanting to require I'm going to put 
        #only 3 for future work
        required_columns = ['order_type', 'quantity', 'unit_price']

        #This line is going to fill in our missing data as 0's 
        sales_data = sales_data.fillna(0)

        #Showing the first n rows of data I am going to use the first 10
        sales_data.head(10).to_csv('sales_data_test.csv')

        return sales_data

    except Exception as e:
        print(f"An error has occured: {e}")


#calling the CSV url file
url = "https://drive.google.com/file/d/1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA/view"
sales_data = load_csv(url)