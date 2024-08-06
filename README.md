# NYC-Citibike-Data-Pipeline
This project implements a batch data pipeline for NYC's Citibike data. It extracts raw data, stores it in Google Cloud Storage and BigQuery, transforms it using DBT, and visualizes insights with Google Looker Data Studio. The pipeline showcases the end-to-end data engineering process.



#set up commands

```
python3 -m venv .venv

```

source .venv/bin/activate


1. Verify Current Account and Project
Check Current Account:

Verify which account is currently authenticated by running:
bash
Copy code
gcloud auth list
This will show you the active account and any other accounts associated with your gcloud configuration.
Check Current Project:

To see the active project in your gcloud configuration, run:
bash
Copy code
gcloud config get-value project
2. Authenticate with the Correct Account
Log In with the Desired Account:

If you need to authenticate with shreyajaiswal0416@gmail.com, you can use the following command:
bash
Copy code
gcloud auth login
Follow the prompts to log in with your Google account. Ensure you are using the correct email address.
Set the Project for Your Account:

If you need to set a specific project, use the following command:
bash
Copy code
gcloud config set project YOUR_PROJECT_ID
Replace YOUR_PROJECT_ID with the ID of the project you want to work with. If you don't have a project, you can create one in the Google Cloud Console.

Addressing the Quota Project Discrepancy
Here's how you can resolve the issue:

Verify the Active Project

You've successfully set the active project with:

bash
Copy code
gcloud config set project nyc-citibike-data-pipeline
Ensure this is the project you intend to work with.

Update the Quota Project for Application Default Credentials

To align your ADC with the active project, you need to update the quota project using the following command:

bash
Copy code
gcloud auth application-default set-quota-project nyc-citibike-data-pipeline
This command sets the quota project for your ADC to match the active project.

Verify the Update

After running the command, verify that the quota project has been updated successfully. You can check the current quota project setting by running:

bash
Copy code
gcloud config list


#terraform commands
terraform init
terraform validate

terraform plan -var="project=nyc-citibike-data-pipeline"

terraform apply -var="project=nyc-citibike-data-pipeline"



#API's enabled
1. Service Usage API
2. BigQuery API



Notes on Terraform Configuration and Resources
1. Terraform Initialization
Version Requirement: Specifies that the Terraform version must be at least 1.0.
Backend Configuration:
Default backend is set to local for storing the state file locally.
Can be changed to gcs (Google Cloud Storage) or s3 (Amazon S3) for remote state storage.
Required Providers:
Uses the Google provider from HashiCorp.
2. Provider Configuration
Google Provider:
project: The GCP project ID is set using a variable.
region: The region for deploying resources is set using a variable.
credentials: Path to the service account JSON key file is specified for authentication.
Example: file("../nyc-citibike-data-pipeline-ba0b5a6983ed.json").
3. Resources Created
a. Google Cloud Storage Bucket (Data Lake)
Resource Type: google_storage_bucket

Purpose: Creates a data lake storage bucket.

Key Attributes:

name: Unique bucket name combining a local variable and project name.
location: Specifies the region for the bucket.
storage_class: Defines the storage class (e.g., STANDARD).
uniform_bucket_level_access: Enables uniform access control.
versioning: Turns on object versioning.
lifecycle_rule: Sets a rule to delete objects older than 30 days.
force_destroy: Allows bucket deletion even with objects inside.
Documentation: Google Storage Bucket

b. Google BigQuery Dataset
Resource Type: google_bigquery_dataset

Purpose: Creates a dataset in BigQuery for loading raw data from GCS.

Key Attributes:

dataset_id: Specifies the dataset ID using a variable.
project: Sets the GCP project ID.
location: Defines the dataset's region.
Documentation: Google BigQuery Dataset

# PREFECT - FRAMEWORK
cd to prefect folder

prefect --version
prefect server start

# Tranformation - dbt
Transformation happening within the datawarehouse itself
Example: Keeping dbt_project.yml in the dbt Subdirectory
Keep dbt_project.yml in the dbt Subdirectory:

Ensure your project structure is:
Copy code
your_project/
├── dbt/
│   ├── dbt_project.yml
│   ├── models/
Adjust the Project Subdirectory in dbt Cloud:

In dbt Cloud, set the project subdirectory to dbt.

ow the schema.yml configuration you provided relates specifically to BigQuery:

version: 2: This indicates the schema file version, which is the same across different data warehouses, including BigQuery.

sources:: In BigQuery, sources refer to tables or views that exist in your BigQuery datasets.

- name: staging: This is the name you’ve given to the source. In BigQuery, this name will be used to reference the source data within your dbt models. It does not correspond to a physical table but is a logical name for grouping related sources.

database: charged-state-382320: In BigQuery, the term "database" is equivalent to "project." So, charged-state-382320 represents your BigQuery project ID where your data is stored.

schema: nyc_citibike_data: In BigQuery, the term "schema" corresponds to "dataset." So, nyc_citibike_data is the name of the dataset within the BigQuery project that contains your source tables.

tables:: This section lists the tables within the dataset that dbt will use as sources.

- name: citibike_tripsdata: This specifies a table named citibike_tripsdata in the dataset nyc_citibike_data. This table exists in your BigQuery dataset, and dbt will use this table as a source for your models.

In summary, for BigQuery:

The staging source refers to a logical grouping of tables.
charged-state-382320 is your BigQuery project ID.
nyc_citibike_data is the dataset within that project.
citibike_tripsdata is the table within that dataset.
You use this configuration in dbt to pull data from the citibike_tripsdata table in BigQuery into your dbt models.

Run dbt Seed Command:

To load the data from citibike_stations.csv into BigQuery, you would use the dbt seed command:
sh

dbt seed

