# AWS S3 and Lambda ETL Pipeline

## Overview
This project implements an ETL pipeline using AWS Lambda and S3 to process cafe sales data, clean it, generate visualizations, and save outputs to S3. The Lambda function reads `dirty_cafe_sales.csv`, handles missing values, maps items, converts data types, and saves results to `output-bucket`.

## Project Structure
- `lambda_function.py`: Lambda function code for ETL and visualization.
- `sample_data/`: Sample input (`dirty_cafe_sales.csv`) and outputs (`processed_cafe_sales.csv`).
- `README.md`: Project documentation.

## AWS Setup
1. **Create S3 Buckets**:
   - `input-bucket-ps924`: For `dirty_cafe_sales.csv`.
   - `output-bucket-ps924`: For processed CSV and visualizations.
2. **Create IAM Role** (`LambdaETLRole`):
   - Attach `AWSLambdaBasicExecutionRole`.
   - Custom policy (`LambdaS3AccessPolicy`):
     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
                 "Resource": [
                     "arn:aws:s3:::input-bucket-ps924/*",
                     "arn:aws:s3:::output-bucket-ps924/*",
                     "arn:aws:s3:::input-bucket-ps924",
                     "arn:aws:s3:::output-bucket-ps924"
                 ]
             },
             {
                 "Effect": "Allow",
                 "Action": "s3:GetObject",
                 "Resource": "arn:aws:s3:::layer-bucket/layer.zip"
             }
         ]
     }
