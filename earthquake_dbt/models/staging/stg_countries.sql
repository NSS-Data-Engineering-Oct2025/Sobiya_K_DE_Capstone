with source as (
    select * from raw_countries
),

renamed as (
    select
        name  as country_name,
        region,
        subregion,
        continents,
        population,
        capital,
        latitude,
        longitude
    from source
)

select * from renamed