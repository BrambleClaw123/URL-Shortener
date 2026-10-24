# 🗄️ Thiết Kế Cơ Sở Dữ Liệu (Amazon DynamoDB Schema)

Tài liệu này mô tả cấu trúc bảng dữ liệu trên **Amazon DynamoDB** và cơ chế tự động xóa bản ghi hết hạn (**Time-To-Live - TTL**) của đề tài **Dịch vụ rút gọn URL (URL Shortener) serverless**.

---

## 1. Thông Tin Chung Về Bảng

- **Tên bảng (Table Name):** `UrlShortenerTable`
- **Region triển khai:** `us-east-1`
- **Khóa chính (Partition Key):** `short_id` (`String`)
- **Khóa sắp xếp (Sort Key):** Không sử dụng (mỗi `short_id` là duy nhất, tương ứng với một bản ghi liên kết rút gọn).
- **Thuộc tính TTL (Time-To-Live):** `ttl_expire` (`Number`)
- **Nhãn tài nguyên (Tags):**
  - `Project = URLShortener`
  - `Owner = 24110237_24110169`

---

## 2. Cấu Trúc Thuộc Tính Bản Ghi (Attributes)

Mỗi mục dữ liệu (Item) được lưu trữ trong bảng `UrlShortenerTable` bao gồm các thuộc tính sau:

| Thuộc tính (Attribute) | Kiểu dữ liệu (Data Type) | Vai trò | Mô tả chi tiết |
| :--- | :---: | :---: | :--- |
| `short_id` | `String` (`S`) | **Partition Key** | Mã định danh duy nhất của liên kết rút gọn (ví dụ: `xY7z9`). Dùng để tra cứu trực tiếp khi chuyển hướng hoặc xem thống kê. |
| `long_url` | `String` (`S`) | Attribute | Đường dẫn URL gốc ban đầu của người dùng cần rút gọn (ví dụ: `https://aws.amazon.com/dynamodb/`). |
| `clicks` | `Number` (`N`) | Attribute | Bộ đếm tổng số lượt truy cập vào liên kết rút gọn. Mặc định khi mới tạo bản ghi có giá trị là `0`. |
| `created_at` | `Number` (`N`) | Attribute | Thời điểm khởi tạo liên kết được biểu diễn dưới dạng Unix epoch timestamp tính bằng giây (ví dụ: `1729742400`). |
| `ttl_expire` | `Number` (`N`) | **TTL Attribute** | Thời điểm liên kết hết hạn được biểu diễn dưới dạng Unix epoch timestamp tính bằng giây (ví dụ: `1735689600`). |

---

## 3. Ví Dụ Bản Ghi Thực Tế (Sample Item)

Dưới đây là cấu trúc một bản ghi mẫu lưu trong bảng `UrlShortenerTable`:

```json
{
  "short_id": "xY7z9",
  "long_url": "[https://aws.amazon.com/dynamodb/](https://aws.amazon.com/dynamodb/)",
  "clicks": 42,
  "created_at": 1729742400,
  "ttl_expire": 1735689600
}
```

---

## 4. Cơ Chế Tự Động Xóa Liên Kết Hết Hạn (DynamoDB TTL)

- **Nguyên lý hoạt động:** Tính năng **Time-To-Live (TTL)** của Amazon DynamoDB được kích hoạt trên thuộc tính `ttl_expire`. Khi thời gian hiện tại vượt quá giá trị Unix epoch timestamp lưu trong `ttl_expire`, DynamoDB sẽ tự động đánh dấu và xóa bản ghi đó khỏi bảng mà không tốn chi phí đọc/ghi hay cần hàm Lambda dọn dẹp riêng.
- **Lưu ý xử lý ở tầng ứng dụng (Lambda `RedirectLink`):** Do quá trình xóa bản ghi hết hạn của DynamoDB TTL diễn ra ở chế độ nền (background process) nên có thể có độ trễ nhất định sau thời điểm hết hạn. Khi triển khai hàm `RedirectLink`, hệ thống sẽ kiểm tra thêm điều kiện thời gian hiện tại so với `ttl_expire` trước khi thực hiện chuyển hướng để đảm bảo tính chính xác.

---

## 5. Các Thao Tác Truy Xuất Dữ Liệu Chính (Access Patterns)

| STT | Nghiệp vụ | Hàm Lambda | Thao tác DynamoDB | Chi tiết xử lý |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Tạo short link | `CreateLink` | `PutItem` | Ghi bản ghi mới với khóa `short_id`, gán `clicks = 0`, lưu `long_url`, `created_at` và `ttl_expire`. |
| 2 | Chuyển hướng link | `RedirectLink` | `GetItem` / `UpdateItem` | Tra cứu bản ghi theo `short_id`, cộng nguyên tử (atomic counter) thuộc tính `clicks` thêm `1` và lấy `long_url` để trả về HTTP `301`. |
| 3 | Xem thống kê click | `GetStats` | `GetItem` | Truy vấn bản ghi theo Partition Key `short_id` để lấy toàn bộ thông tin bao gồm `long_url`, thời gian tạo/hết hạn và tổng số `clicks`. |