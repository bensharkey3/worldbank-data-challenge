import requests
import time
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


URL = 'https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json'
MAX_RETRIES=5
BASE_DELAY=1


def get_total_pages(url):
    data = requests.get(f"{url}&page=1").json()
    return data[0]['pages']


def get_data_with_retry(url, total_pages, max_retries, base_delay):
    gdp_data = []
    all_gdp_data = []
    page = 1

    while (page == 1 or response.status_code == 200) and page <= total_pages:
        for attempt in range(max_retries):
            try:
                response = requests.get(f"{url}&page={page}")
                data = requests.get(f"{url}&page={page}").json()
                gdp_data = data[1]
                all_gdp_data.extend(gdp_data)
                print(f"page {page} successful with {len(gdp_data)} records added - total record count:{len(all_gdp_data)}")
                if page == total_pages:
                    print('data from api completed successfully')
                page += 1
            except requests.exceptions.RequestException as e:
                if attempt == max_retries:
                    raise e
                    
                delay = min(base_delay * (attempt**2))
                time.sleep(delay)

    df = pd.json_normalize(all_gdp_data)
    return df


def connect_to_db():
    conn = psycopg2.connect(
    dbname="postgres", 
    user="postgres", 
    password="mypassword", 
    host="db", 
    port="5432"
    )

    cur = conn.cursor()
    return cur, conn


def execute_drop_and_create_tables(cur):
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


def write_df_to_db(df, conn, cur):
    tuples = [tuple(x) for x in df.to_numpy()]
    
    print("executing import query...")
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
    
    print("closing connection...")
    cur.close()
    conn.close()


if __name__ == '__main__':
    print('getting total pages...')
    total_pages = get_total_pages(URL)
    print(f'total pages: {total_pages}')
    print('getting data from api...')
    df = get_data_with_retry(URL, total_pages, MAX_RETRIES, BASE_DELAY)
    print('connecting to db...')
    cur, conn = connect_to_db()
    print('executing create and drop tables...')
    execute_drop_and_create_tables(cur)
    print('writing df to db...')
    write_df_to_db(df, conn, cur)
    