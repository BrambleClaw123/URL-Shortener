import unittest
import os

# 1. Cấp sẵn biến môi trường giả lập cho Local (Phải đặt TRƯỚC khi import create)
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['TABLE_NAME'] = 'UrlShortenerTable'

# 2. Import hàm handler sau khi đã có biến môi trường
from create import handler

class TestCreateLink(unittest.TestCase):
    def test_missing_url(self):
        # Giả lập request người dùng không gửi thuộc tính long_url
        event = {"body": "{}"} 
        response = handler(event, None)
        
        # Mong đợi hệ thống chặn lại và trả về mã lỗi 400 (Bad Request)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn("error", response['body'])

    def test_invalid_url_format(self):
        # Giả lập request gửi link thiếu http:// hoặc https://
        event = {"body": '{"long_url": "www.hcmute.edu.vn"}'} 
        response = handler(event, None)
        
        # Mong đợi hệ thống chặn lại và trả về mã lỗi 400
        self.assertEqual(response['statusCode'], 400)

if __name__ == '__main__':
    unittest.main()