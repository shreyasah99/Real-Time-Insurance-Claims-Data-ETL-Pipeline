# Real-Time Insurance Data ETL Pipeline with Snowflake

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Tools and Services Used](#tools-and-services-used)
4. [ETL Workflow](#etl-workflow)
5. [Setup Instructions](#setup-instructions)
6. [Running the Project](#running-the-project)
7. [Data Visualization](#data-visualization)
8. [Contributing](#contributing)
9. [License](#license)

## Project Overview
This project involves creating a real-time ETL (Extract, Transform, Load) data pipeline to process insurance data from Kaggle and load it into Snowflake. The data pipeline is managed using Apache Airflow and involves several steps to clean, normalize, and transform the data before loading it into Snowflake for further processing. AWS S3 is used as a data lake for storing raw and transformed data.

After developing this project, we can schedule the Airflow DAG to run based on our requirements, ensuring the ETL process is executed at the desired frequency. The final cleaned, normalized, and transformed data will be available for real-time visualization in Tableau, allowing for up-to-date insights and reporting.

## Architecture Diagram

![architecture_diagram](https://github.com/user-attachments/assets/ae965ace-b02f-4e46-8d7c-71b530ff3014)


## Tools and Services Used
- **Python**: For scripting and data processing.
- **Pandas**: For data manipulation and analysis.
- **AWS S3**: As a data lake for storing raw and transformed data.
- **Snowflake**: For data modeling and storage.
- **Apache Airflow**: For orchestrating the ETL workflow.
- **EC2**: For hosting the Airflow environment.
- **Kaggle API**: For extracting data from Kaggle.
- **Tableau**: For data visualization.

## ETL Workflow
1. **Data Extraction**
    - Create an Airflow DAG script to extract a random number of rows from the Kaggle insurance dataset using the Kaggle API.
    - Clean, normalize, and transform the data into four tables:
        - `policy_data`
        - `customers_data`
        - `vehicles_data`
        - `claims_data`

2. **Data Storage**
    - Store the transformed data in S3 buckets, organized into different folders for each type of normalized data (`policy_data`, `customers_data`, `vehicles_data`, `claims_data`).

3. **Data Processing in Snowflake**
    - Create Snowflake SQL worksheets to define database schemas.
    - Create staging tables in Snowflake for each type of normalized data.
    - Define Snowpipes to automate data ingestion from the S3 buckets to the staging tables.
    - Create stream objects for each staging table to capture changes.
    - Create final tables to merge new data from the stream objects, ensuring only distinct or new rows are inserted.

4. **Change Data Capture with Snowflake Streams and Tasks**
    - Create tasks in Snowflake to automate change data capture.
    - Each task is triggered when new data is available in the stream objects to load the data into the final tables.

5. **Airflow DAG Tasks**
    - **Task 1**: Check if the Kaggle API is available.
    - **Task 2**: Upload the transformed data to the S3 bucket.

## Setup Instructions
### EC2 Instance Setup
1. **Create an EC2 Ubuntu t2.small instance to host the Airflow environment.**
   - Immediately after creating the instance, **change inbound rules in the EC2 instance's security group** to allow TCP traffic on port 8080. This allows access to the Airflow webserver.
2. SSH into the EC2 instance and install dependencies as detailed in [how_to_run.docx](https://github.com/ravishankar324/Real-Time-Insurance-claims-Data-ETL-Pipeline/blob/master/how_to_run.docx).
3. Set up Python environment and install Airflow along with necessary dependencies.
4. Configuration: Insert `kaggle.json` and the DAG script as specified in [how_to_run.docx](https://github.com/ravishankar324/Real-Time-Insurance-claims-Data-ETL-Pipeline/blob/master/how_to_run.docx).
5. Start Airflow components and access the Airflow webserver at `<EC2 public IPV4 DNS>:8080`.
6. Update Airflow connections and trigger the DAG as outlined in [how_to_run.docx](https://github.com/ravishankar324/Real-Time-Insurance-claims-Data-ETL-Pipeline/blob/master/how_to_run.docx).

## Running the Project
- Once the cleaned data is stored in S3, it triggers other objects in Snowflake for further preprocessing to establish change data capture.
- Access the Airflow webserver at `<EC2 public IPV4 DNS>:8080` and trigger the DAG to start the ETL process.

## Data Visualization
- Install the ODBC Snowflake driver to connect Tableau to Snowflake. Instructions for installing the driver can be found on the [Snowflake documentation page](https://docs.snowflake.com/en/user-guide/odbc-download).
- Set up a live data visualization connection in Tableau to the final tables in Snowflake.
- Use Tableau to analyze and visualize the final transformed data for insights and reporting.

## Dashboard
[![Auto _Animation](https://github.com/user-attachments/assets/77c2131f-3fd6-4738-8043-6ccbb2e5775b)
](https://public.tableau.com/app/profile/ravi.shankar.p.r/viz/Auto_Insurance_claims_data_dashboard/final_dashboard)

> ### Checkout Tableau data visualization at [Insurance claims data| Tableau Public](https://public.tableau.com/app/profile/ravi.shankar.p.r/viz/Auto_Insurance_claims_data_dashboard/final_dashboard)

> ### Checkout [how_to_run.docx](https://github.com/ravishankar324/Real-Time-Insurance-claims-Data-ETL-Pipeline/blob/master/how_to_run.docx) file for detailed steps to run this project.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with any improvements.


