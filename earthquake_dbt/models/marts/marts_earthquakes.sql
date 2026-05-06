with earthquakes as (
    select * from {{ ref('stg_earthquakes') }}
),

weather as (
    select * from {{ ref('stg_weather') }}
),

countries as (
    select * from {{ ref('stg_countries') }}
),

final as (
    select
        e.earthquake_id,
        e.magnitude,
        e.place,
        e.earthquake_timestamp,
        e.is_tsunami,
        e.significance,
        e.latitude,
        e.longitude,
        e.depth,
        w.temperature,
        w.windspeed,
        w.winddirection,
        w.weathercode,
        c.country_name,
        c.region,
        c.subregion,
        c.continents,
        c.population
    from earthquakes e
    left join weather w on e.earthquake_id = w.earthquake_id
    left join countries c on e.place ilike '%' || c.country_name || '%'
)

select * from final