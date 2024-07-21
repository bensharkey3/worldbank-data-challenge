{{ config(materialized = 'able') }}

WITH
add_prev_gdp AS (
    SELECT
        country,
        year,
        gdp,
        LAG(
            gdp
        ) OVER(PARTITION BY country ORDER BY year ASC) AS prev_gdp
    FROM {{ ref('stg_gdp_alldata') }}
    WHERE country != ''
        AND gdp != 'NaN'
        AND year::int >= 2000
    ORDER BY country, year
),

add_gdp_growth AS (
    SELECT
        *,
        (gdp::float / prev_gdp::float) - 1 AS gdp_growth
    FROM add_prev_gdp
),

find_min_max_growths AS (
    SELECT
        country,
        MIN(gdp_growth) AS min_gdp_growth_since_2000,
        MAX(gdp_growth) AS max_gdp_growth_since_2000
    FROM add_gdp_growth
    GROUP BY
        country
),

final AS (
    SELECT
        add_gdp_growth.country,
        add_gdp_growth.year,
        add_gdp_growth.gdp,
        find_min_max_growths.min_gdp_growth_since_2000,
        find_min_max_growths.max_gdp_growth_since_2000
    FROM add_gdp_growth
    INNER JOIN
        find_min_max_growths ON
            find_min_max_growths.country = add_gdp_growth.country
)

SELECT * FROM final
