import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch') # Khởi tạo client CloudWatch
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    short_id = event['pathParameters']['short_id']
    try:
        response = table.update_item(
            Key={'short_id': short_id},
            UpdateExpression='ADD clicks :inc',
            ConditionExpression='attribute_exists(short_id)',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='ALL_NEW'
        )
        long_url = response['Attributes']['long_url']
        
        # Đẩy Custom Metric lên CloudWatch
        cloudwatch.put_metric_data(
            Namespace='URLShortener/Metrics',
            MetricData=[{
                'MetricName': 'TotalLinkClicks',
                'Dimensions': [{'Name': 'Action', 'Value': 'Redirect'}],
                'Value': 1,
                'Unit': 'Count'
            }]
        )

        return {
            'statusCode': 301,
            'headers': {
                'Location': long_url,
                'Cache-Control': 'no-cache'
            }
        }
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}