WITH
stg_gdp_alldata as (
	select
        country_value AS country,
        date AS year,
        value AS gdp
	from gdp_alldata
),

add_prev_gdp AS (
    SELECT
        country,
        year,
        gdp,
        LAG(
            gdp
        ) OVER(PARTITION BY country ORDER BY year ASC) AS prev_gdp
    FROM stg_gdp_alldata
    WHERE country != ''
	and gdp != 'NaN'
    ORDER BY country, year
),

add_gdp_growth as (
	SELECT
		*,
		(gdp::float / prev_gdp::float) -1 as gdp_growth
	FROM add_prev_gdp
),

find_min_max_growths as (
	select
		country,
		min(gdp_growth) as min_gdp_growth_since_2000,
		max(gdp_growth) as max_gdp_growth_since_2000
	from add_gdp_growth
	where year::int >= 2000
	group by
		country
),

final as (
	select
		a.country,
		a.year,
		a.gdp,
		b.min_gdp_growth_since_2000,
		b.max_gdp_growth_since_2000
	from add_gdp_growth as a
	join find_min_max_growths as b on b.country = a.country
)

select * from final
