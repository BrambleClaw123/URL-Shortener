## TUẦN 3: TỰ ĐỘNG HÓA HẠ TẦNG VÀ GIÁM SÁT HỆ THỐNG

- **Thời gian thực hiện:** 19/10/2026 – 25/10/2026
- **Link GitHub Repository (Public):** https://github.com/BrambleClaw123/URL-Shortener
- **Mục tiêu tuần 3:**
  1. Cập nhật template SAM (`template.yaml`) để tự động hóa tạo Amazon S3 Bucket (Frontend) và mở quyền Public Read trực tiếp qua mã IaC.
  2. Giải quyết vấn đề thiếu Tags ở tuần 2: Bổ sung Tag `Project=URLShortener` và `Owner=2411023724110169` vào các tài nguyên DynamoDB và S3 qua template.
  3. Đồng bộ lại tài liệu API Contract và DynamoDB Schema sang định dạng thời gian chuẩn *Unix Epoch Time (kiểu Number)* cho khớp với dữ liệu code thực tế.
  4. Upload giao diện web lên S3 tĩnh mới tạo, chạy kịch bản click mô phỏng lưu lượng (generate traffic).
  5. Giám sát hệ thống thông qua Amazon CloudWatch Metrics (Invocations) và CloudWatch Logs (RequestId, Duration, Billed Duration).
  6. Đánh giá bảng Cost Summary trên Billing and Cost Management để chốt chi phí vận hành ở kiến trúc Serverless hiện tại.

---

1. ### BẢNG TỔNG HỢP PHÂN CÔNG VÀ GIỜ LÀM VIỆC TUẦN 3

| Sinh viên | MSSV | Vai trò chính | Số giờ cá nhân | Giám sát, test & check chi phí | Tổng số giờ |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Huỳnh Phạm Hoàng Kha** | 24110237 | Cập nhật template.yaml (thêm S3 Bucket, Public Read, Tags); Deploy hạ tầng; Trích xuất biểu đồ CloudWatch Metrics. | 7.0 giờ | 1.5 giờ | **8.5 giờ** |
| **Phạm Vĩ Cận** | 24110169 | Đồng bộ tài liệu thiết kế (Unix Epoch Time); Deploy HTML lên S3 & giả lập lưu lượng; Phân tích CloudWatch Logs. | 6.5 giờ | 1.5 giờ | **8.0 giờ** |

---

### 2. CHI TIẾT CÔNG VIỆC TỪNG SINH VIÊN

#### Sinh viên 1: Huỳnh Phạm Hoàng Kha (MSSV: 24110237)
- Cập nhật AWS SAM template (`template.yaml`) để bổ sung chức năng tự động hóa khởi tạo S3 Bucket, cấp quyền Public Read qua Bucket Policy và bổ sung Tags (`Project`, `Owner`) (4.5 giờ):
  - File IaC cập nhật: [`template.yaml`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/template.yaml) 
  - Ảnh minh chứng Tags trên DynamoDB & S3 (Console): [`docs/Tuan 3/tags.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%203/tags.png)
- Đóng gói, cập nhật hạ tầng (`sam deploy`) và trích xuất chỉ số giám sát từ hệ thống CloudWatch Metrics đo lường Invocations với Statistic: Sum (2.5 giờ):
  - Ảnh minh chứng biểu đồ CloudWatch Metrics: [`docs/Tuan 3/metrics.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%203/metrics.png)
- Cùng kiểm tra Billing and Cost Management chốt chi phí vận hành tuần 3 (1.5 giờ):
  - Ảnh minh chứng Cost Summary ($0.00): [`docs/Tuan 3/billing.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%203/billing.png)

---

#### Sinh viên 2: Phạm Vĩ Cận (MSSV: 24110169)
- Cập nhật và đồng bộ tài liệu thiết kế cơ sở dữ liệu và API Contract sang định dạng Unix Epoch Time (kiểu Number) nhằm khớp với dữ liệu Lambda ghi nhận (2.5 giờ):
  - File API Contract: [`docs/api-contract.md`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%201/api-contract.md)
  - File DB Schema: [`docs/dynamodb-schema.md`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%201/dynamodb-schema.md)
- Upload file `index.html` lên S3 Bucket mới tạo bằng code, chạy kịch bản giả lập lưu lượng (generate traffic) và theo dõi luồng request (2.0 giờ):
  - Ảnh minh chứng giao diện S3 mới: [`docs/Tuan 3/frontend.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%203/frontend.png)
- Truy xuất và phân tích chi tiết log thực thi trong CloudWatch Logs, chỉ ra hiện tượng Cold Start qua `INIT_START` và phân biệt `Duration` (283.22 ms) vs `Billed Duration` (786 ms) (2.0 giờ):
  - Ảnh minh chứng dòng Log CreateLinkFunction: [`docs/Tuan 3/logs.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%203/logs.png)
- Cùng kiểm tra Billing and Cost Management chốt chi phí vận hành tuần 3 (1.5 giờ).

---

### 3. GHI CHÚ CÔNG VIỆC & KHÓ KHĂN CẦN GIẢI QUYẾT Ở TUẦN 4

- **Cảnh báo Cold Start:** Nhóm đã quan sát được thời gian `Billed Duration` bị đội lên trong lần chạy đầu tiên (Cold Start). Sẽ lưu ý vấn đề này khi thực hiện test hiệu năng/throttling ở Tuần 4.
- **Rà soát Tags:** Mới chỉ thực hiện tag cho DynamoDB và S3. Sẽ tiến hành rà soát để đảm bảo API Gateway và Lambda cũng được gắn tag chính xác trong Tuần 4.
- **Test chịu tải:** Hiện tại `Reserved Concurrency` đang khóa ở 5. Tuần tới nhóm sẽ chạy tool đẩy nhiều request cùng lúc để ép xuất hiện lỗi `429 Too Many Requests` (Throttling) phục vụ báo cáo.
- **Cải tiến tính năng nâng cao (Unit Test & Metrics):** Sẽ viết mã Unit Test cho hàm tạo rút gọn URL để kiểm thử bắt lỗi các trường hợp biên (nhập URL chứa khoảng trắng, unicode, hoặc ký tự đặc biệt). Đồng thời, cấu hình thêm Custom Metric trên CloudWatch để ghi nhận chính xác lượt đếm truy cập mỗi link ghi vào DynamoDB.