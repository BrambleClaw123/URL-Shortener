import urllib.request
import concurrent.futures
import json

# THAY LINK NÀY BẰNG LINK API GATEWAY CỦA BẠN (thêm /links ở cuối)
API_URL = "https://hfbustcxrb.execute-api.us-east-1.amazonaws.com/Prod/links"

payload = json.dumps({"long_url": "https://hcmute.edu.vn"}).encode('utf-8')
headers = {'Content-Type': 'application/json'}

def send_request(req_id):
    req = urllib.request.Request(API_URL, data=payload, headers=headers, method='POST')
    try:
        response = urllib.request.urlopen(req)
        return f"Req {req_id}: Thành công - Status: {response.getcode()}"
    except urllib.error.HTTPError as e:
        return f"Req {req_id}: BỊ CHẶN (Throttling) - Status: {e.code} - Lỗi: {e.reason}"

# Bắn 50 request cùng lúc (đa luồng)
print("Bắt đầu bắn 50 requests cùng lúc để test Throttling...")
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(send_request, range(50))

for res in results:
    print(res)