import pandas as pd
from prefect import flow , task
#from prefect_gcp.cloud_storage import GcsBucket
#from prefect_gcp import GcpCredentials, GcsBucket
#from prefect_gcp import GcsBucket

from prefect_gcp.cloud_storage import GcsBucket
import pyarrow.parquet as pq
from zipfile import ZipFile
from io import BytesIO
import requests
import os
from pathlib import Path
from prefect.tasks import task_input_hash
from datetime import timedelta
#from prefect_gcp import GcpCredentials
from google.cloud import bigquery

from prefect_gcp import GcpCredentials


PROJECT_ID ="nyc-citibike-data-pipeline"
BQ_DATASET ="nyc_citibike_data"
BQ_TABLENAME ="citibike_tripsdata_raw"
PARTITIONED_TABLE ="citibike_tripsdata"
PARTITION_COL ="started_at"

         
              
# @task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
# def fetch(dataset_url: str) -> pd.DataFrame:
#     """ Reads citi bike data from web to pandas dataframe"""
#     resp = requests.get(dataset_url)
#     zipfile = ZipFile(BytesIO(resp.content))
#     for file_name in zipfile.namelist():
#         print(file_name)
#         file = zipfile.open(file_name)
#         df = pd.read_csv(file)
#         return df

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """ Reads citi bike data from web to pandas dataframe"""
    resp = requests.get(dataset_url)
    zipfile = ZipFile(BytesIO(resp.content))
    df_list = []
    for file_name in zipfile.namelist():
        print(file_name)  # Print each filename to validate
        if file_name.endswith('.csv'):
            file = zipfile.open(file_name)
            df_list.append(pd.read_csv(file))
    df = pd.concat(df_list, ignore_index=True)
    return df
  

@task(log_prints=True)
def clean(df=pd.DataFrame)-> pd.DataFrame:
    """ Fix dtype issues"""
    df["ride_id"] = df["ride_id"].astype('str')
    df["rideable_type"] = df["rideable_type"].astype('str')
    df["started_at"] = df["started_at"].astype('datetime64[ns]')
    df["ended_at"] = df["ended_at"].astype('datetime64[ns]')
    df["start_station_name"] = df["start_station_name"].astype('str')
    df["start_station_id"] = df["start_station_id"].astype('str')
    df["end_station_name"] = df["end_station_name"].astype('str')
    df["end_station_id"] = df["end_station_id"].astype('str')
    df["start_lat"] = df["start_lat"].astype('float')
    df["start_lng"] = df["start_lng"].astype('float')
    df["end_lat"] = df["end_lat"].astype('float')
    df["end_lng"] = df["end_lng"].astype('float')
    df["member_casual"] = df["member_casual"].astype('str')
    return df



@task(log_prints=True)
def write_local(df: pd.DataFrame , year:int, dataset_file:str) -> Path:
    """ writes data locally as parquet file"""
    path =f"{dataset_file}.parquet"
    df.to_parquet(path,compression='gzip')
    return path



@task(log_prints = True)
def write_to_gcs(file,dest_file) -> None :
    """ write to gcs bucket"""
    gcp_credentials = GcpCredentials.load("nyc-citibike-gcp-block")
    gcs_bucket = GcsBucket(
    bucket="citibike_data_lake_nyc-citibike-data-pipeline",
    gcp_credentials=gcp_credentials
    )
    #gcs_block = GcsBucket.load("de-bucket-gcs")
    gcs_bucket_path = gcs_bucket.upload_from_path(file)
    #gcs_block.upload_from_path(from_path=file,to_path=dest_file)
    return




# gcs_bucket = GcsBucket.load("my-bucket")
# gcs_bucket.upload_from_path("notes.txt", "my_folder/notes.txt")



@task(log_prints = True)
def write_gbq(df):
    """ write dataframe to BigQuery"""
    #gcp_credentials_block = GcpCredentials.load("gcp-creds")
    gcp_credentials_block = GcpCredentials.load("nyc-citibike-gcp-block")
    table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLENAME}"
    df.to_gbq(
        destination_table= f"{BQ_DATASET}.{BQ_TABLENAME}",
        project_id = PROJECT_ID,
        credentials =gcp_credentials_block.get_credentials_from_service_account(),
        chunksize =500000,
        if_exists = "append"
    )

  

@task(log_prints=True)
def remove_file(local_path):
    if os.path.isfile(local_path):
        os.remove(local_path)
    else:
        print("Error: %s file not found" %local_path )



@flow()
def etl_web_to_gcs(year: int , month: int) -> None :
   """ this is main ETL function"""
   dataset_file = f"{year}{month:02}-citibike-tripdata"
   dest_file = f"{dataset_file}.parquet"
   print(dataset_file)
   if(month == 5 or month == 6):
       dataset_url = f"https://s3.amazonaws.com/tripdata/{dataset_file}.zip"
   else:
       dataset_url = f"https://s3.amazonaws.com/tripdata/{dataset_file}.csv.zip"   
   
   print(dataset_url)

   df = fetch(dataset_url)
   clean_df = clean(df)
   local_path = write_local(clean_df,year,dataset_file)
   print("====================================================================================================")
   print(f"local path --> {local_path}")
   print("====================================================================================================")
   print("====================================================================================================")
   print(f"dest path --> {dest_file}")
   print("====================================================================================================")
   write_to_gcs(local_path,dest_file)
   write_gbq(clean_df)
   remove_file(local_path)
   

@flow()
def etl_parent_flow(year: int = 2021, months: list[int] = [2,3]):
    for month in months:
        etl_web_to_gcs(year,month)
    

@flow()
def create_BQpartitioned_table():
    """ create a partitioned table in BigQuery"""
    gcp_credentials_block = GcpCredentials.load("nyc-citibike-gcp-block")
    credentials =gcp_credentials_block.get_credentials_from_service_account()
    client = bigquery.Client(credentials=credentials)

    sql =f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{BQ_DATASET}.{PARTITIONED_TABLE}`
    PARTITION BY DATE({PARTITION_COL}) AS
    SELECT * FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLENAME}`;
    """
    query_job = client.query(sql)
    print("created the partitioned table")


if __name__ =='__main__':
    """ Passing different years and mnths seperately , as all months the data is not published"""
    # year1= 2021
    # months_2021= [2,3,4,5,6,7,8,9,10,11,12]

    # year2= 2022
    # months_2022= [1,2,3,4,5,8,9,10,11,12]
    
    
    # year3= 2023
    # months_2023= [1,2]

    year4= 2024
    months_2024= [1,2,3,4,5,6]

    etl_parent_flow(year4,months_2024)
    # etl_parent_flow(year2,months_2022)
    # etl_parent_flow(year3,months_2023)
    create_BQpartitioned_table()