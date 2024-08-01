
{{ config(materialized='table') }}

with citibike_data as (
    select * 
    from {{ ref ('staging_citibike_data')}}
),

dim_citibike_stations as (
    select *
    from {{ ref('dim_citibike_stations')}}
)
select 
    ride_data.ride_id,			
    ride_data.rideable_type,	
    ride_data.member_casual,				
    ride_data.started_at ,			
    ride_data.ended_at ,
    TIMESTAMP_DIFF(ride_data.ended_at,ride_data.started_at,MINUTE) as ride_duration,	
    ride_data.start_station_name,			
    start_station.station_id_int as start_station_id,			
    ride_data.end_station_name,				
    end_station.station_id_int as end_station_id,
    ride_data.start_lat,		
    ride_data.start_lng,			
    ride_data.end_lat,				
    ride_data.end_lng

from citibike_data as ride_data
inner join dim_citibike_stations as start_station
on ride_data.start_station_name = start_station.name
inner join dim_citibike_stations as end_station
on ride_data.end_station_name = end_station.name