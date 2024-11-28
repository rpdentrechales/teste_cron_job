import pandas as pd
from datetime import datetime
import requests

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

def query_appointments(current_page, start_date, end_date):
    token = "145418|arQc09gsrcSNJipgDRaM4Ep6rl3aJGkLtDMnxa0u"
    endpoint = "https://open-api.eprocorpo.com.br/graphql"
    headers = {'Content-Type': 'application/json',
               "authorization": f"Bearer {token}"}

    query = """query ($filters: AppointmentFiltersInput, $pagination: PaginationInput) {
                    fetchAppointments(filters: $filters, pagination: $pagination) {
                        meta {
                            lastPage
                        }
                        data {
                            id
                            status {
                                label
                            }
                            store {
                                name
                            }
                            customer {
                                id
                                name
                                telephones {
                                    number
                                }
                            }
                            procedure {
                                name
                            }
                            startDate
                        }
                    }
                }"""

    variables = {
        "filters": {
            "startDateRange": {
                "start": start_date,
                "end": end_date,
            },
        },
        "pagination": {
            "currentPage": current_page,
            "perPage": 1000,
        },
    }

    response = requests.post(endpoint, json={"query": query, "variables": variables}, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        total_pages = response_json["data"]["fetchAppointments"]["meta"]["lastPage"]

        print(f"\rQuerying - {current_page}/{total_pages} pages", end="")

        # Return the data field
        return response_json["data"]["fetchAppointments"]["data"]
    else:
        print(response)
        return "error"

def save_to_csv(data):
    """Save the API result to a CSV file."""
    # Normalize nested JSON and convert to DataFrame
    df = pd.json_normalize(data)
    # Save to CSV with a timestamp
    filename = f"appointments_{datetime.today().strftime('%Y-%m-%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}.")

if __name__ == "__main__":
    # Entry point of the program
    main()
