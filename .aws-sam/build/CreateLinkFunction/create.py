import json
import os
import time
import random
import string
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        long_url = body.get('long_url')

        if not long_url or not long_url.startswith(('http://', 'https://')):
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Vui lòng nhập URL hợp lệ (bắt đầu bằng http:// hoặc https://)'})
            }

        short_id = generate_short_id()
        now = int(time.time())
        # Thiết lập TTL tự động xóa sau 7 ngày (7 * 24 * 3600 giây)
        ttl_expire = now + (7 * 24 * 3600)

        table.put_item(
            Item={
                'short_id': short_id,
                'long_url': long_url,
                'clicks': 0,
                'created_at': now,
                'ttl_expire': ttl_expire
            }
        )

        domain = event['requestContext']['domainName']
        stage = event['requestContext']['stage']
        short_url = f"https://{domain}/{stage}/{short_id}"

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'short_id': short_id,
                'short_url': short_url,
                'long_url': long_url,
                'ttl_expire': ttl_expire
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }