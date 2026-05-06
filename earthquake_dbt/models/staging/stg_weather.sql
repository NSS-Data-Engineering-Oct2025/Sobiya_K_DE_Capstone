with source as (
    select * from raw_weather
),

renamed as (
    select
        earthquake_id,
        temperature,
        windspeed,
        winddirection,
        weathercode
    from source
)

select * from renamed