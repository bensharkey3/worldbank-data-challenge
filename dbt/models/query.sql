with
temp1 as (
    select
        country_value as country,
        date as year,
        value as gdp,
        lag(
            value
        ) over(partition by countryiso3code order by date asc) as prev_gdp
    from public.gdp_alldata
    where country_value != ''
    order by country_value, date
)

select * from temp1
