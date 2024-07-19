WITH
source AS (
    SELECT * FROM {{ source('worldbank_data_challenge', 'gdp_alldata') }}
),

renamed AS (
    SELECT
        country_value AS country,
        date AS year,
        value AS gdp
    FROM source
)

SELECT * FROM renamed
