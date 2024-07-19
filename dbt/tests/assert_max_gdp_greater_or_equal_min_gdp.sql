SELECT *
FROM {{ ref("gdp_by_country") }}
WHERE min_gdp_growth_since_2000 > max_gdp_growth_since_2000
