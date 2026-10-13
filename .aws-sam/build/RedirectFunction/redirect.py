import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    short_id = event['pathParameters']['short_id']

    try:
        # Kiểm tra tồn tại và tăng bộ đếm clicks lên 1 nguyên tử (Atomic)
        response = table.update_item(
            Key={'short_id': short_id},
            UpdateExpression='ADD clicks :inc',
            ConditionExpression='attribute_exists(short_id)',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='ALL_NEW'
        )
        long_url = response['Attributes']['long_url']

        return {
            'statusCode': 301,
            'headers': {
                'Location': long_url,
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Access-Control-Allow-Origin': '*'
            },
            'body': ''
        }
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': 'Liên kết không tồn tại hoặc đã hết hạn (TTL)!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }