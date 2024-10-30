#Read a file from a URL and write a local file "sales_data_test.csv"
# containing just the first 10 rows of data
from math import e
import pandas as pd
import pyarrow # not needed here
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Import the data file. this needs to be downloaded to be used by pandas. 
# It is in CSV format

url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"

# Attempt to read the CSV filel
try:
    print("Reading CSV file...")
    sales_data = pd.read_csv(url, dtype_backend='pyarrow', on_bad_lines="skip")

    # Ask pandas to parse the order_date field into a standard repressetantion
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], format="mixed")

    #Save the first 10 rows of the data in sales_data.test
    print(sales_data.head(10))
    sales_data.head(10).to_csv('sales_data_test.csv')

except Exception as e:
    print(f"An error has occured: {e}")