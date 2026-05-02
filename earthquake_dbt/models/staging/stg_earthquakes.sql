with source as (
    select * from raw_earthquakes
),

renamed as (
    select
        id as earthquake_id,
        magnitude,
        place,
        to_timestamp(earthquake_time / 1000) as earthquake_timestamp,  --The raw time looks like 1776907831662 (millisecs)We divide by 1000 to get secs, then convert to a readable date like 2026-04-29 20:50:20
        case when tsunami = 1 then true -- Raw data stores tsunami as 0 or 1, convert it to true or false
             else false end as is_tsunami,
        significance,
        latitude,
        longitude,
        depth
    from source
)

select * from renamed