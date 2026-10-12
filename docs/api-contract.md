# 🔌 Tài Liệu Thiết Kế Giao Tiếp API (RESTful API Contract)

Tài liệu này quy định hợp đồng giao tiếp (API Contract) giữa giao diện web tĩnh trên Amazon S3 và hệ thống xử lý phía sau qua Amazon API Gateway & AWS Lambda của đề tài **Dịch vụ rút gọn URL (URL Shortener) serverless**.

---

## 1. Thông Tin Chung

- **Cửa ngõ giao tiếp:** Amazon API Gateway (đã kích hoạt CORS).
- **Định dạng dữ liệu trao đổi:** `application/json` (trừ API chuyển hướng sử dụng HTTP Header).
- **Region triển khai:** `us-east-1`.

### Bảng tổng hợp các Endpoint

| STT | Method | Endpoint | Hàm Lambda xử lý | Chức năng | Phản hồi thành công |
| :-: | :---: | :--- | :--- | :--- | :--- |
| 1 | `POST` | `/links` | `CreateLink` | Tạo liên kết rút gọn mới | `200 OK` (JSON) |
| 2 | `GET` | `/{short_id}` | `RedirectLink` | Chuyển hướng về URL gốc | `301 Moved Permanently` (Header `Location`) |
| 3 | `GET` | `/{short_id}/stats` | `GetStats` | Xem thống kê lượt click | `200 OK` (JSON) |

---

## 2. Chi Tiết Các Endpoint

### API 1: Tạo short link (`CreateLink`)

Tiếp nhận URL gốc từ người dùng, sinh mã định danh `short_id`, lưu bản ghi mới vào bảng DynamoDB `UrlShortenerTable` (với `clicks = 0`, `created_at` và `ttl_expire`) và trả về đường dẫn rút gọn.

- **Method:** `POST`
- **Endpoint:** `/links`
- **Request Headers:**
  - `Content-Type: application/json`
- **Body Request (từ Frontend gửi lên):**

        {
          "long_url": "https://aws.amazon.com/dynamodb/"
        }

- **Response Thành Công (`200 OK`):**

        {
          "short_id": "xY7z9",
          "short_url": "https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/xY7z9",
          "expires_at": 1735689600
        }

- **Ý nghĩa các trường phản hồi:**
  - `short_id` (`String`): Mã định danh của liên kết rút gọn vừa được tạo.
  - `short_url` (`String`): Đường dẫn rút gọn hoàn chỉnh dùng để chia sẻ và truy cập.
  - `expires_at` (`Number`): Thời điểm liên kết hết hạn theo chuẩn Unix epoch tính bằng giây (tương ứng với thuộc tính `ttl_expire` trong DynamoDB).

---

### API 2: Chuyển hướng (`RedirectLink`)

Tra cứu bản ghi theo `short_id` trong bảng `UrlShortenerTable`, tăng bộ đếm `clicks` thêm `1` và điều hướng trình duyệt của người dùng về địa chỉ gốc.

- **Method:** `GET`
- **Endpoint:** `/{short_id}` *(Ví dụ: `/xY7z9`)*
- **Path Parameters:**
  - `short_id` (`String` - bắt buộc): Mã định danh của liên kết rút gọn.
- **Response Thành Công (`301 Moved Permanently`):**
  - **Body:** Không trả về JSON.
  - **HTTP Headers:**

        Location: https://aws.amazon.com/dynamodb/

  - **Hành vi:** Trình duyệt nhận mã `301` cùng header `Location` sẽ tự động chuyển hướng sang trang đích (`long_url`).

---

### API 3: Xem thống kê lượt click (`GetStats`)

Truy vấn thông tin từ bảng `UrlShortenerTable` theo `short_id` và trả về địa chỉ gốc kèm tổng số lượt truy cập hiện tại.

- **Method:** `GET`
- **Endpoint:** `/{short_id}/stats` *(Ví dụ: `/xY7z9/stats`)*
- **Path Parameters:**
  - `short_id` (`String` - bắt buộc): Mã định danh của liên kết rút gọn cần tra cứu thống kê.
- **Response Thành Công (`200 OK`):**

        {
          "short_id": "xY7z9",
          "long_url": "https://aws.amazon.com/dynamodb/",
          "clicks": 42
        }

- **Ý nghĩa các trường phản hồi:**
  - `short_id` (`String`): Mã định danh của liên kết rút gọn.
  - `long_url` (`String`): Đường dẫn URL gốc ban đầu của người dùng.
  - `clicks` (`Number`): Tổng số lượt truy cập vào liên kết rút gọn.