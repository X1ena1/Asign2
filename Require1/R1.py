import pandas as pd
import pyarrow
import ssl
import time
import sys

ssl._create_default_https_context = ssl._create_unverified_context

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
        
    except Exception as e:
        print(f"An error has occured: {e}")


#calling the CSV url file
url = "https://drive.google.com/file/d/1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA/view"
sales_data = load_csv(url)