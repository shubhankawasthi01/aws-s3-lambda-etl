import boto3
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def clean_data(df):
    # Replace 'ERROR' and 'UNKNOWN' with NaN
    df.replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)

    # Convert numeric columns
    columns_num = ['Quantity', 'Price Per Unit', 'Total Spent']
    for col in columns_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df[columns_num] = df[columns_num].astype('float')

    # Handle null values in numeric columns
    df['Price Per Unit'] = df['Price Per Unit'].fillna(df['Total Spent'] / df['Quantity'])
    df['Total Spent'] = df['Total Spent'].fillna(df['Quantity'] * df['Price Per Unit'])
    df['Quantity'] = df['Quantity'].fillna(df['Total Spent'] / df['Price Per Unit'])

    # Map Item based on Price Per Unit
    dict_item_price = {2.0: 'Coffee', 1.0: 'Cookie', 5.0: 'Salad', 1.5: 'Tea'}
    df['Item'] = df.apply(
        lambda row: dict_item_price[row['Price Per Unit']]
        if (pd.isna(row['Item']) and row['Price Per Unit'] in dict_item_price)
        else row['Item'], axis=1)

    # Fill remaining nulls with mean for numeric columns
    df['Price Per Unit'] = df['Price Per Unit'].fillna(df['Price Per Unit'].mean())
    df['Total Spent'] = df['Total Spent'].fillna(df['Total Spent'].mean())
    df['Quantity'] = df['Quantity'].fillna(df['Quantity'].mean())

    # Convert Transaction Date to datetime
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce').dt.date

    # Fill remaining nulls in categorical columns
    remaining_columns = ['Item', 'Payment Method', 'Transaction Date', 'Location']
    df[remaining_columns] = df[remaining_columns].fillna('UNKNOWN')

    return df

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    input_bucket = 'input-bucket'
    output_bucket = 'output-bucket'
    input_key = 'dirty_cafe_sales.csv'
    output_key = 'processed_cafe_sales.csv'

    # Extract: Read CSV from S3
    obj = s3.get_object(Bucket=input_bucket, Key=input_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    # Transform: Apply cleaning logic
    df = clean_data(df)

    # Load: Save processed data to S3
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=output_bucket, Key=output_key, Body=csv_buffer.getvalue())

    return {'statusCode': 200, 'message': 'ETL and visualization completed'}