import boto3
import json

# Initialize the AWS clients outside the handler for better performance
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

# Replace with your actual DynamoDB table name
TABLE_NAME = 'YourImageLabelsTable'
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    import boto3
import json

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourImageLabelsTable')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    image_name = event['Records'][0]['s3']['object']['key']
    
    # 1. Generate a Presigned URL that lasts for 1 hour (3600 seconds)
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': image_name},
        ExpiresIn=3600 
    )

    # 2. Call Rekognition (same as before)
    response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
        MaxLabels=10
    )
    labels = [label['Name'] for label in response['Labels']]
    
    # 3. Save to DynamoDB including the new URL
    table.put_item(
        Item={
            'ImageName': image_name,
            'Labels': labels,
            'ViewLink': presigned_url # This is your clickable link!
        }
    )
    return {'statusCode': 200}
    
    try:
        # 2. Call Amazon Rekognition to detect labels
        # MaxLabels=10 finds the top 10 things in the image
        # MinConfidence=75 ensures we only get results AWS is sure about
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': image_name
                }
            },
            MaxLabels=10,
            MinConfidence=75
        )
        
        # 3. Extract just the label names into a list
        labels = [label['Name'] for label in response['Labels']]
        print(f"Detected labels for {image_name}: {labels}")
        
        # 4. Save the results to DynamoDB
        table.put_item(
            Item={
                'ImageName': image_name,
                'Bucket': bucket,
                'Labels': labels,
                'LabelCount': len(labels)
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {image_name}')
        }

    except Exception as e:
        print(f"Error processing image {image_name}: {str(e)}")
        raise e
