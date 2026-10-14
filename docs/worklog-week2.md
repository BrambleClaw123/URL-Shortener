## TUẦN 2: TRIỂN KHAI CHỨC NĂNG LÕI TRÊN AWS & KIỂM THỬ HỆ THỐNG

- **Thời gian thực hiện:** 12/10/2026 – 18/10/2026
- **Link GitHub Repository (Public):** https://github.com/BrambleClaw123/URL-Shortener
- **Mục tiêu tuần 2:**
  1. Viết template hạ tầng dưới dạng mã (IaC) bằng AWS SAM (`template.yaml`) cấu hình API Gateway, Lambda, DynamoDB với `Reserved Concurrency = 5` và sử dụng `LabRole`.
  2. Khởi tạo bảng DynamoDB `UrlShortenerTable` và bật cơ chế Time to Live (TTL) tự động xóa link.
  3. Lập trình mã nguồn Python (boto3) cho 3 hàm Lambda: tạo link (`CreateLink`), chuyển hướng (`RedirectLink`), và xem thống kê (`GetStats`).
  4. Đóng gói và triển khai tự động hạ tầng lên AWS Learner Lab (Region `us-east-1`) qua lệnh `sam build` và `sam deploy --guided`.
  5. Phát hành giao diện người dùng (HTML/JS) trên Amazon S3 Static Website Hosting và cấp quyền đọc công khai (Public Read).
  6. Kiểm thử luồng hệ thống: thao tác tạo link, redirect, ghi nhận bộ đếm Atomic Counter trên DynamoDB tăng tự động và hiển thị thống kê.

---

### 1. BẢNG TỔNG HỢP PHÂN CÔNG VÀ GIỜ LÀM VIỆC TUẦN 2

| Sinh viên | MSSV | Vai trò chính | Số giờ cá nhân | Kiểm thử / Họp nhóm | Tổng số giờ |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Huỳnh Phạm Hoàng Kha** | 24110237 | Viết mã nguồn Python 3 hàm Lambda, Thiết kế giao diện HTML/JS, Deploy S3 Static Website, Cấu hình Bucket Policy | 6.0 giờ | 2.5 giờ | **8.5 giờ** |
| **Phạm Vĩ Cận** | 24110169 | Viết code IaC (`template.yaml`), Cấu hình API Gateway/DynamoDB, Đóng gói & Triển khai SAM (`sam deploy`) | 6.0 giờ | 2.5 giờ | **8.5 giờ** |

---

### 2. CHI TIẾT CÔNG VIỆC TỪNG SINH VIÊN

#### Sinh viên 1: Huỳnh Phạm Hoàng Kha (MSSV: 24110237)
- Lập trình mã nguồn Python (boto3) xử lý logic cho 3 hàm Lambda: tạo link, redirect 301 và truy xuất thống kê click (3.0 giờ):
  - Mã nguồn tạo link: [`backend/create.py`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/backend/create.py) 
  - Mã nguồn redirect: [`backend/redirect.py`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/backend/redirect.py) 
  - Mã nguồn thống kê: [`backend/stats.py`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/backend/stats.py) 
- Tích hợp API Endpoint, thiết kế giao diện HTML/JS và deploy lên S3 Static Website Hosting. Thiết lập bucket policy cấp quyền đọc công khai (Public Read) (3.0 giờ):
  - File giao diện: [`frontend/index.html`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/frontend/index.html) 
  - Ảnh minh chứng thiết lập bucket S3: [`docs/Tuan 2/bucket.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/bucket.png) 
- Phối hợp kiểm thử luồng hệ thống (Functional Testing): thực hiện thao tác tạo link, redirect, xem thống kê trên web thành công (2.5 giờ):
  - Ảnh minh chứng giao diện hoạt động: [`docs/Tuan 2/giaodien.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/giaodien.png) 

---

#### Sinh viên 2: Phạm Vĩ Cận (MSSV: 24110169)
- Viết code IaC cấu hình hạ tầng AWS SAM (API Gateway, Lambda, DynamoDB) với `Reserved Concurrency = 5` và sử dụng `LabRole` (3.0 giờ):
  - File cấu hình SAM Template: [`template.yaml`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/template.yaml) 
  - Ảnh cấu hình Concurrency = 5: [`docs/Tuan 2/concurrency5.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/concurrency5.png) 
  - Ảnh cấu hình LabRole: [`docs/Tuan 2/exerole.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/exerole.png) 
  - Ảnh kiểm chứng bảng DynamoDB & cấu hình TTL: [`docs/Tuan 2/urltable.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/urltable.png), [`docs/Tuan 2/ttlon.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/ttlon.png) 
- Đóng gói và triển khai tự động hạ tầng lên AWS Learner Lab (Region `us-east-1`) bằng lệnh `sam build` và `sam deploy --guided` (3.0 giờ):
  - File cấu hình tham số deploy: [`samconfig.toml`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/samconfig.toml) 
  - Ảnh minh chứng Terminal deploy thành công: [`docs/Tuan 2/samdeploy.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/samdeploy.png) 
  - Ảnh minh chứng Stack & API Gateway: [`docs/Tuan 2/stackurl.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/stackurl.png), [`docs/Tuan 2/apigateway.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%202/apigateway.png) 
- Phối hợp kiểm thử luồng hệ thống toàn diện, đối chiếu Atomic Counter trên DynamoDB tự động tăng khi có lượt truy cập (2.5 giờ).

---

### 3. GHI CHÚ CÔNG VIỆC & KHÓ KHĂN CẦN GIẢI QUYẾT Ở TUẦN 3

- **Tagging:** Bảng DynamoDB sinh ra từ SAM Template hiện tại chưa có Tag (đang báo `Tags (0)` trên Console). Nhóm sẽ cập nhật Tagging trực tiếp vào file `template.yaml` trong Tuần 3.
- **Tài liệu vs Thực tế:** Thuộc tính `created_at` đang được Lambda ghi vào DB dưới dạng Unix epoch. Cần cập nhật lại tài liệu thiết kế (Data Schema Tuần 1) vốn đang ghi là định dạng chuỗi ISO 8601 để đồng bộ với mã nguồn thực tế.
- **Bảo mật:** Giao diện S3 tĩnh hiện đang dùng giao thức HTTP nên bị trình duyệt cảnh báo "Không bảo mật".