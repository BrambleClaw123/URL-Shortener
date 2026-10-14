## TUẦN 1: TÌM HIỂU DỊCH VỤ, THIẾT KẾ KIẾN TRÚC & CHUẨN BỊ MÔI TRƯỜNG

- **Thời gian thực hiện:** 05/10/2026 – 11/10/2026
- **Link GitHub Repository (Public):** https://github.com/BrambleClaw123/URL-Shortener
- **Mục tiêu tuần 1:**
  1. Nghiên cứu tài liệu các dịch vụ AWS sử dụng trong đề tài: Amazon API Gateway, AWS Lambda, Amazon DynamoDB, Amazon S3, AWS CloudFormation / SAM, Amazon CloudWatch, IAM LabRole.
  2. Tìm hiểu các giới hạn tài nguyên của môi trường AWS Learner Lab (Region `us-east-1`, `LabRole`, giới hạn Lambda concurrency ≤ 10, đặt reserved concurrency ≤ 5) và thống nhất quy định gắn nhãn (Tagging: `Project = URLShortener`, `Owner = 24110237_24110169`).
  3. Thiết kế mô hình kiến trúc dịch vụ rút gọn URL serverless và vẽ sơ đồ hệ thống trên Draw.io.
  4. Thiết kế cấu trúc cơ sở dữ liệu DynamoDB (`UrlShortenerTable` với Partition Key `short_id` và cơ chế tự động xóa link hết hạn bằng thuộc tính `ttl_expire`).
  5. Thiết kế hợp đồng giao tiếp API (RESTful API Contract) cho 3 endpoint: Tạo short link (`POST /links`), Chuyển hướng (`GET /{short_id}`), Xem thống kê lượt click (`GET /{short_id}/stats`).
  6. Khởi tạo GitHub Repository, phân quyền, thiết lập cấu trúc thư mục dự án và tạo Worklog chung.
  7. Cài đặt môi trường phát triển tại máy cá nhân (Python/NodeJS, Docker, AWS CLI v2, AWS SAM CLI), cấu hình thông tin xác thực và kiểm tra kết nối tới AWS Learner Lab bằng lệnh `aws sts get-caller-identity`.

---

### 1. BẢNG TỔNG HỢP PHÂN CÔNG VÀ GIỜ LÀM VIỆC TUẦN 1

| Sinh viên | MSSV | Vai trò chính | Số giờ cá nhân | Họp nhóm | Tổng số giờ |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Huỳnh Phạm Hoàng Kha** | 24110237 | Khởi tạo Git repository & cấu trúc dự án, Tạo Worklog chung, Thiết kế sơ đồ kiến trúc (Draw.io), Thiết kế RESTful API Contract, Cài đặt môi trường local | 8.5 giờ | 1.0 giờ | **9.5 giờ** |
| **Phạm Vĩ Cận** | 24110169 | Nghiên cứu giới hạn AWS Learner Lab & thống nhất quy ước Tagging, Thiết kế DynamoDB Schema & cơ chế TTL, Lấy ARN `LabRole` & Credentials, Cài đặt môi trường local | 8.0 giờ | 1.0 giờ | **9.0 giờ** |

---

### 2. CHI TIẾT CÔNG VIỆC TỪNG SINH VIÊN

#### Sinh viên 1: Huỳnh Phạm Hoàng Kha (MSSV: 24110237)
- Khởi tạo Git Repository công khai tại [`BrambleClaw123/URL-Shortener`](https://github.com/BrambleClaw123/URL-Shortener), phân quyền cộng tác, thiết lập cấu trúc thư mục dự án và khởi tạo file Worklog chung (1.5 giờ):
  - File cấu trúc / README: [`README.md`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/README.md)
  - File Worklog: [`docs/worklog-week1.md`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/worklog-week1.md)
- Thiết kế và vẽ sơ đồ kiến trúc tổng thể (Architecture Diagram) của hệ thống URL Shortener serverless bằng Draw.io (2.5 giờ):
  - Link Draw.io: [Sơ đồ kiến trúc trên diagrams.net](https://app.diagrams.net/#G1PnCEu8wIO-ms-VwBoF0jS1jJMXiftU-_#%7B%22pageId%22%3A%22XV87qkZuxvu6hrgPSVqJ%22%7D)
  - File sơ đồ lưu trên repo: [`docs/Tuan 1/architecture-diagram.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%201/architecture-diagram.png)
- Thiết kế API Contract theo chuẩn RESTful quy định cấu trúc Request/Response cho 3 endpoint `POST /links`, `GET /{short_id}` (HTTP 301 Redirect) và `GET /{short_id}/stats` (2.0 giờ):
  - File tài liệu API Contract: [`docs/Tuan 1/api-contract.md`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%201/api-contract.md)
- Cài đặt môi trường phát triển local gồm Python/NodeJS, Docker, AWS CLI v2 (`aws-cli/2.37.9`), AWS SAM CLI (`version 1.166.2`) và cấu hình khóa xác thực kết nối với AWS Learner Lab (2.5 giờ).
- Họp nhóm cùng kiểm tra kết nối thông mạng tới AWS bằng lệnh `aws sts get-caller-identity` và chốt kế hoạch triển khai code cho Tuần 2 (1.0 giờ).

---

#### Sinh viên 2: Phạm Vĩ Cận (MSSV: 24110169)
- Nghiên cứu tài liệu giới hạn tài nguyên của AWS Learner Lab và thống nhất quy định gắn nhãn Tagging với `Project = URLShortener`, `Owner = 24110237_24110169` để quản lý tài nguyên và phân loại chi phí trên AWS Billing (1.5 giờ):
  - File quy ước cấu hình & Tagging: [`docs/Tuan 1/tagging-and-limits.md`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%201/tagging-and-limits.md)
- Thiết kế cấu trúc cơ sở dữ liệu DynamoDB (`UrlShortenerTable`), xác định Partition Key `short_id` (String), các thuộc tính `long_url`, `clicks`, `created_at` và thuộc tính `ttl_expire` (Number - Unix epoch) phục vụ cơ chế TTL tự động xóa link hết hạn (2.5 giờ):
  - File thiết kế DynamoDB Schema: [`docs/Tuan 1/dynamodb-schema.md`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%201/dynamodb-schema.md)
- Truy cập AWS Management Console, cố định Region `us-east-1`, khảo sát quyền và trích xuất ARN của `LabRole` (`arn:aws:iam::487906062447:role/LabRole`), lấy thông tin AWS CLI Credentials cho nhóm (1.5 giờ).
- Cài đặt môi trường phát triển local gồm Python/NodeJS, Docker, AWS CLI v2, AWS SAM CLI và cấu hình khóa xác thực trên máy cá nhân (2.5 giờ).
- Họp nhóm kiểm tra kết nối AWS CLI bằng lệnh `aws sts get-caller-identity` và thống nhất phân chia công việc viết hàm Lambda cho Tuần 2 (1.0 giờ).