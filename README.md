# NYC-Citibike-Data-Pipeline <img src="https://github.com/ShreyaJaiswal1604/NYC-Citibike-Data-Pipeline/blob/main/images/logos/nyc-citibike-logo.png" alt="Citi Bike Logo" style="width: 50px; vertical-align: right;" />



## 1. Project Description

This project implements a batch data pipeline for NYC's Citibike data. It extracts raw data, stores it in Google Cloud Storage and BigQuery, transforms it using DBT, and visualizes insights with Google Looker Data Studio. The pipeline showcases the end-to-end data engineering process.

## 2. Dataset

The Citi Bike dataset offers detailed information about bike rides in New York City, including insights into usage patterns, ride durations, and station popularity. You can download the dataset from the following link: [Citi Bike Dataset](https://s3.amazonaws.com/tripdata/index.html).

## 3. Tools and Technologies

- **Google Cloud Platform (GCP)**: A suite of cloud computing services that runs on the same infrastructure that Google uses internally for its end-user products.
  - **[Google Cloud Storage](https://cloud.google.com/storage)**: A scalable, fully-managed object storage service that allows you to store and retrieve any amount of data at any time.
  - **[BigQuery](https://cloud.google.com/bigquery)**: A fully-managed, serverless data warehouse that enables scalable analysis over petabytes of data.
  - **[Google Looker Data Studio](https://lookerstudio.google.com/)**: A business intelligence tool that helps you turn your data into informative dashboards and reports that are easy to read, easy to share, and fully customizable.
  
- **[DBT (Data Build Tool)](https://www.getdbt.com/)**: A command-line tool that enables data analysts and engineers to transform data in their warehouse more effectively by allowing them to write data transformation code in SQL.

- **[Terraform](https://www.terraform.io/)**: An open-source infrastructure as code software tool that provides a consistent CLI workflow to manage hundreds of cloud services.

- **[Prefect](https://www.prefect.io/)**: A workflow management system that allows you to build, run, and monitor data pipelines at scale.

## 4. Citibike Pipeline Architecture


![Citibike Pipeline Architecture](https://github.com/ShreyaJaiswal1604/NYC-Citibike-Data-Pipeline/blob/main/images/architecture/nyc-citibike-pipeline.png)


### Data Flow

1. **Extraction**: Raw data is extracted and stored in Google Cloud Storage.
2. **Loading**: Data is loaded into BigQuery for further processing.
3. **Transformation**: DBT (Data Build Tool) is used to transform and model the data within BigQuery.
4. **Visualization**: Insights are visualized using Google Looker Data Studio.



## 5. Steps to Execute
To successfully execute this project, follow the steps outlined below to set up the necessary environments and tools:

<details>
  <summary><h4>💻 Code Setup</h4></summary>
  
  #### 1. Clone the git repo to your system

  ```
  git clone <your-repo-url>

  ```

#### 2. Python Environment Setup

```
python3 -m venv .venv
source .venv/bin/activate
```
#### 3. Install necessary packaged and libraries

```
  pip install -r requirements.txt
```
</details>


<details>
  <summary><h4>🌐 Google Cloud Environment Setup</h4></summary>

#### 1. Log In with the Desired Google Account and Create a Project 
- Access Google Cloud at [Google Cloud Console](https://console.cloud.google.com/cloud-resource-manager).

#### 2. Configure Identity and Access Management (IAM) for the Service Account
- Assign the following roles:
  - BigQuery Admin
  - Storage Admin
  - Storage Object Admin

#### 3. Authenticate Your Google Account
- To authenticate with your Google account, use the following command:
    ```sh
    gcloud auth login
    ```
- Set the project for your account:
    ```sh
    gcloud config set project YOUR_PROJECT_ID
    ```
</details>

<details>
  <summary><h4>🛠️  Terraform Setup</h4></summary>

#### 1. Installing Terraform and Adding it to Your PATH
- If you don't have Terraform installed, you can download it from [here](https://www.terraform.io/downloads) and then add it to your PATH.


#### 2. Configure Identity and Access Management (IAM) for the Service Account
- Assign the following roles:
  - BigQuery Admin
  - Storage Admin
  - Storage Object Admin

#### 3. After step 1 and 2 navigate to the terraform folder 
- command to navigate to the terraform folder
    ```sh
     cd terraform/
    ```

#### 4. Run the Following Commands to Create Your Project Infrastructure
- Terraform commands:
    ```sh
     terraform init
     terraform validate
     terraform plan -var="project=nyc-citibike-data-pipeline"
     terraform apply -var="project=nyc-citibike-data-pipeline"

    ```
    
</details>

<details>
  <summary><h4>🧩 Prefect Framework Setup</h4></summary>

#### 1. Confirm Prefect Installation in your virtual Environment
- command to check the current version of the Prefect CLI
    ```sh
     prefect --version
    ```
#### 2. Start Prefect server
- Command to initiate the Prefect server to begin managing and orchestrating your workflows
    ```sh
     prefect server start
    ```
    
#### 3. Accessing and Configuring Blocks in the Prefect UI
- Access the UI at http://127.0.0.1:4200/.
- Update the blocks to register them with your credentials for Google Cloud Storage (GCS) and BigQuery. This can be done in the Blocks options.
- You can either keep the block names as they appear in the code or rename them. If you choose to rename them, ensure that you update the code to reference the new block names.

#### 4. Running the Prefect Data Pipeline
- Return to the terminal and navigate to the prefect/ directory:
    ```sh
     cd prefect/
    ```
- Execute the data pipeline script:
    ```sh
     python citibike_data_pipeline.py
    ```
- The Python script will then store the Citibike data in both your GCS bucket and BigQuery.

    
</details>

<details>
  
<summary><h4>🔍  Running the dbt Flow</h4></summary>

#### 1. Confirm Prefect Installation in your virtual Environment
- - Create a dbt account and log in using [dbt Cloud](https://cloud.getdbt.com).
  - 
#### 2. Clone the Repository
  - Once logged in, clone the repository for use.
    
#### 3. Run the dbt Command
  - In the CLI at the bottom, execute the following command:
    ```sh
    dbt run
    ```
 - This command will run all the models and create the final dataset called `fact_citibike`.


#### 4. Verify Successful Execution
- Upon a successful run, the lineage of `fact_citibike` will be displayed as shown below:
    
</details>

<details>
  
<summary><h4>📊 Visualization in Looker Studio</h4></summary>

#### 1. Utilize the Dataset
  - You can now use the fact_citibike dataset within Looker Studio for creating visualizations.
    
#### 2. Access the Report
  - You can find the report for the half-year Citibike analysis [Report-2024](https://lookerstudio.google.com/reporting/7772f82f-5d07-4cfd-b1e9-e2c409147608).
 </details>

## 5. Citibike Dashboard 2024
Access the NYC Citibike Dashboard - [Report-2024](https://lookerstudio.google.com/reporting/7772f82f-5d07-4cfd-b1e9-e2c409147608)
- #### **Half-Yearly Report NYC Citi Bike User Analysis (Jan - Jul 2024)**
  ---
  ![NYC Citi Bike User Analysis](https://github.com/ShreyaJaiswal1604/NYC-Citibike-Data-Pipeline/blob/main/images/dashboard/2024-citibike-user-analysis.png)

- #### **Half-Yearly Report: NYC Citi Bike Monthly Ride Analysis (Jan - Jul 2024)**
  ---
  ![NYC Citi Bike Monthly Ride Analysis](https://github.com/ShreyaJaiswal1604/NYC-Citibike-Data-Pipeline/blob/main/images/dashboard/2024-citibike-bike-ride-analysis.png)

