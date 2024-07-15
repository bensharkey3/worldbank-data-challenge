import requests
import pandas as pd
import psycopg2


url = 'https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json'

gdp_data = ['placeholder']
all_gdp_data = []
page = 1

response = requests.get(f"{url}&page={page}")

while response.status_code == 200 and len(gdp_data) > 0:
    response = requests.get(f"{url}&page={page}")
    data = requests.get(f"{url}&page={page}").json()
    gdp_data = data[1]
    all_gdp_data.extend(gdp_data)
    print(f"page {page} successful with {len(gdp_data)} records added - total record count:{len(all_gdp_data)}")
    page += 1
else:
    print(f"page {page} failed - total record count:{len(all_gdp_data)}")

df = pd.json_normalize(all_gdp_data)
