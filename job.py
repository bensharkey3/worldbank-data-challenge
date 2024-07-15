import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


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

conn = psycopg2.connect(
    dbname="postgres", 
    user="postgres", 
    password="mypassword", 
    host="localhost", 
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    drop table if exists gdp_alldata
    ;
    
    CREATE TABLE gdp_alldata (
        countryiso3code varchar(3),
        date varchar(4),
        value varchar,
        unit varchar,
        obs_status varchar,
        decimal varchar,
        indicator_id varchar,
        indicator_value varchar,
        country_id varchar(2),
        country_value varchar
    )
    """
)

tuples = [tuple(x) for x in df.to_numpy()]

insert_query = """
    insert into gdp_alldata (
        countryiso3code,
        date,
        value,
        unit,
        obs_status,
        decimal,
        indicator_id,
        indicator_value,
        country_id,
        country_value
    )
    values %s
"""

execute_values(cur, insert_query, tuples)
conn.commit()
cur.close()
conn.close()
