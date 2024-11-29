import pandas as pd
from datetime import datetime
import requests
from aux import *

def main():
    start_date = datetime.today().strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    current_page = 1
    results = query_appointments(current_page, start_date, end_date)
    
    if results != "error":
        save_to_csv(results)
    else:
        print("Error in fetching data.")
    return

if __name__ == "__main__":
    # Entry point of the program
    main()
