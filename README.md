# aws-image-rekognition-pipeline
# Serverless Image Rekognition Pipeline

## Project Overview
I built this project to demonstrate event-driven architecture using AWS. When an image is uploaded to an S3 bucket, a Lambda function is triggered to analyze the image using Amazon Rekognition and store the metadata in a DynamoDB table.

## Architecture
- **Amazon S3**: Hosts the original image files.
- **AWS Lambda**: Processes the event and runs the Python logic.
- **Amazon Rekognition**: AI/ML service used to identify objects/labels in the images.
- **Amazon DynamoDB**: NoSQL database used to store image names and detected labels.

## Skills Demonstrated
- Cloud Infrastructure (AWS)
- Python (Boto3 SDK)
- Identity and Access Management (IAM)
- Serverless Computing
