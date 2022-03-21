# Overview

The aim of this project was to create an API which returns data from the EU MRV Emissions online database: https://mrv.emsa.europa.eu/#public/emission-report

I built a data pipeline which:

- Cleans the data in its raw form
- Models this data in a JSON
- Writes the data to a DynamoDB table

I also built an API endpoint that lets you get data for a vessel given the reporting period and the IMO number.

https://8d12si93v8.execute-api.eu-west-2.amazonaws.com/dev/vessels?reporting_period={reporting_period}&imo_number={imo_number}

# Data Architecture

View the diagram in this Miro board: https://miro.com/app/board/uXjVOFww1cg=/

## S3 Bucket

### shipping-api-495700631743

S3 bucket where raw CSV files are uploaded.

The CSV files are in `data/raw_csv_files`

## Lambdas

### data-ingestion

This lambda is triggered when the CSV files are uploaded, at which point it:

- Cleans the data in its raw form
- Models this data in a JSON
- Writes the data to the shipping-data DynamoDB table

### rest-api

This lambda is triggered by a HTTP GET request event from API Gateway.Whenever a consumer of the REST API makes a request, it triggers this lambda, at which point it:

- Reads the vessel data from DynamoDB based on parameters passed into the request
- Returns a single vessel item with data on that vessel

## DynamoDB

### shipping-data

This table is where all the data in the EU MRV Emissions online database is stored.

It has been designed using single table design, so that other datasets from other sources can be stored in the same table. The partition key refers to the data set, and the sort key is used to query a specific item in the table.

In the shipping-data DynamoDB table, the primary key is made up of the following partition key and sort key:

`PK: "EU_MRV_EMISSIONS_DATA"`

`SK: "REPORTING_PERIOD#{reporting_period}#IMO_NUMBER#{imo_number}"`

## API Gateway

API Gateway manages this API endpoint, it acts as a trigger for the rest-api lambda, which fulfills the request and returns the data to the consumer of the API.

# Infrastructure as Code

All infrastructure is managed using Terraform. This project is reproducible on another AWS account, and all Terraform configuration files are stored in the `infra` folder. Deploying infrastructure is part of the CI/CD pipeline.

# Serverless

This project uses the Serverless framework to manage AWS Lambdas and deploy Lambda infrastructure. The configuration for the lambdas in this project is in the `serverless.yml` file.

# CI/CD

I use GitHub Actions to deploy infrastructure, and Git pre-commit hooks to run tests and format/lint/type check the code before pushing changes to remote. The GitHub Actions config file is in the `.github` folder, and the pre-commit hooks are in the `.pre-commit-config.yaml` file.
