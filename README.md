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

Given the approx. 4hrs of total time spent developing, there are a number of limitations with the project, including:
* Limited error handling and logging
* Secrets hardcoded rather than contained within env variables
* dbt setup locally, rather than on Docker
* CI parses the dbt project, but does not connect to the database and create models or run data tests
* CD not implemented

### Assumptions
* Windows machine
* Docker installed
* dbt installed with dbt-postgres adapter

### Build Steps
* Clone this repository to your local Windows machine
* Running datasource/create_datasource.bat will build a Postges db, and run a Python script to populate it with World Bank data
* Run `cd dbt && dbt build` to change into the dbt directory, and build the dbt models and run dbt tests
* When completed run `docker compose down` to terminate the database
* Refer to gdp_by_country.csv for the output of the gdp_by_country dbt data model
