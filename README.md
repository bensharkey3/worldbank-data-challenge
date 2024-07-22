# Data Engineering Challenge - World Bank Dataset

### Overview
This challenge utilises a 'modern data stack' approach that combines various data engineering aspects to ingest, store and transform a dataset.

Steps involved include:
* Creating a Postges database on local using Docker, and running a Python ETL script within Docker
* Accessing a public API using Python
* Reading paginated API records using Python
* Converting JSON records to a relational form using Pandas
* Connecting to and writing to a Postgres db using Python
* Setting up a new dbt project
* Creating views and tables as dbt data models
* Performing dbt data tests
* Implementing Continuous Integration (CI) using Github Actions
* Creating a branch and then a Pull Request to trigger a CI build before merging into main branch

### Description
The thought process behind my approach was to build a solution that was modular and reusable, hence utilising Docker for the database creation and ETL script. I wanted to minimise the amount of custom code and leverage existing tools and packages as much as possible, however the ETL script needed to be custom Python code. Using dbt I wanted to ensure I was following established dbt conventions, by settind up the postgres db as a dbt 'source', also using a stg_ view to clean source data before use in the model containing logic, also aligning with dbt SQL code formatting standards. I used sqlfluff on my local to ensure the code was formatted correctly.

### Assumptions
To be able to run this project yourself, you will need:
* Windows machine
* Docker installed
* dbt installed with dbt-postgres adapter

### Build Steps
* Clone this repository to your local Windows machine
* Running `cd datasource && create_datasource.bat` will build a Postges db, and run a Python script to populate it with World Bank data. Takes approx. 5min to complete. You can monitor progress within Docker desktop
* Run `cd dbt && dbt build` to change into the dbt directory, and build the dbt models and run dbt tests
* When completed run `cd datasource && docker compose down` to terminate the database
* Refer to gdp_by_country.csv for the output of the gdp_by_country dbt data model

### Limitations
Given the approx. 4hrs of total time spent developing, there are a number of limitations with the project, including:
* Limited error handling and logging
* Secrets hardcoded rather than contained within env variables
* dbt setup locally, rather than on Docker
* CI parses the dbt project, but does not connect to the database and create models or run data tests
* Code linting not setup as part of the CI process 
* CD not implemented
