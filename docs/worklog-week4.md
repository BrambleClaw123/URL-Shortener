## TUẦN 4: KIỂM THỬ TẢI, GIÁM SÁT NÂNG CAO VÀ HOÀN THIỆN

- **Thời gian thực hiện:** 26/10/2026 – 31/10/2026
- **Link GitHub Repository (Public):** https://github.com/BrambleClaw123/URL-Shortener
- **Mục tiêu tuần 4:**
  1. Gắn hoàn thiện Tag `Project` và `Owner` cho các tài nguyên còn lại (Lambda và API Gateway) thông qua `template.yaml`.
  2. Lập trình kịch bản và thực thi kiểm thử tải (Load Test) đa luồng để ghi nhận cơ chế chống quá tải (Throttling) của AWS khi chạm ngưỡng Reserved Concurrency.
  3. Cấu hình đẩy chỉ số kinh doanh tùy chỉnh (Custom Metric) `TotalLinkClicks` lên Amazon CloudWatch bằng `boto3`.
  4. Lập trình kịch bản kiểm thử cục bộ (Unit Test) cho hàm Lambda để đảm bảo tính đúng đắn của logic xử lý.
  5. Đóng gói mã nguồn, tối ưu chi phí và hoàn thiện Báo cáo tổng kết đồ án cuối kỳ.

---

### 1. BẢNG TỔNG HỢP PHÂN CÔNG VÀ GIỜ LÀM VIỆC TUẦN 4

| Sinh viên | MSSV | Vai trò chính | Số giờ cá nhân | Báo cáo, Code Review | Tổng số giờ |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Huỳnh Phạm Hoàng Kha** | 24110237 | Cập nhật Tag template.yaml; Lập trình tích hợp boto3 đẩy Custom Metric; Viết Unit Test `test_create.py`; Tổng hợp Báo cáo. | 7.5 giờ | 1.0 giờ | **8.5 giờ** |
| **Phạm Vĩ Cận** | 24110169 | Viết script Load Test đa luồng; Chạy ép lỗi hệ thống & phân tích biểu đồ Throttles CloudWatch. | 5.5 giờ | 2.5 giờ | **8.0 giờ** |

---

### 2. CHI TIẾT CÔNG VIỆC TỪNG SINH VIÊN

#### Sinh viên 1: Huỳnh Phạm Hoàng Kha (MSSV: 24110237)
- Cập nhật AWS SAM template (`template.yaml`) để bổ sung tag tĩnh (`Project`, `Owner`) cho toàn bộ hàm Lambda và API Gateway, thực thi `sam deploy` (2.0 giờ):
  - Ảnh minh chứng Tag của hàm CreateLinkFunction: [`docs/Tuan 4/tag_lambda.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%204/tag_lambda.png)
  - Ảnh minh chứng Tag API Gateway (hiển thị tag hệ thống): [`docs/Tuan 4/tag_apigw.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%204/tag_apigw.png)
- Phát triển tính năng nâng cao: Sử dụng `boto3` trong hàm `RedirectFunction` để tự động đẩy Custom Metric `TotalLinkClicks` lên hệ thống CloudWatch (3.0 giờ):
  - Ảnh minh chứng mã nguồn `redirect.py`: [`docs/Tuan 4/code_metric.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%204/code_metric.png)
  - Ảnh minh chứng biểu đồ Custom Metric trên CloudWatch: [`docs/Tuan 4/chart_custom_metric.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%204/chart_custom_metric.png)
- Lập trình `test_create.py` sử dụng thư viện `unittest`, giả lập biến môi trường (mocking) để chạy Unit Test cục bộ xử lý ngoại lệ (2.5 giờ):
  - Ảnh kết quả Terminal báo Pass 2 test cases: [`docs/Tuan 4/unit_test.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%204/unit_test.png)
- Tổng hợp báo cáo cuối kỳ (1.0 giờ).
---
#### Sinh viên 2: Phạm Vĩ Cận (MSSV: 24110169)
- Thiết kế kịch bản và lập trình script `load_test.py` bắn 50 requests/s vào API Gateway để kiểm tra độ chịu tải của Serverless stack (2.5 giờ):
  - File Script: [`load_test.py`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/load_test.py)
- Thực thi kịch bản ép lỗi hệ thống (chạm mốc Reserved Concurrency = 5), truy xuất và phân tích báo cáo từ AWS (3.0 giờ):
  - Ảnh Terminal trả về lỗi 500 (Throttling) xen kẽ Status 200: [`docs/Tuan 4/terminal_loadtest.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%204/terminal_loadtest.png)
  - Ảnh CloudWatch Metrics ghi nhận Throttles = 45: [`docs/Tuan 4/chart_throttles.png`](https://github.com/BrambleClaw123/URL-Shortener/blob/main/docs/Tuan%204/chart_throttles.png)
- Thực hiện Pair-programming và Code Review mã nguồn Unit Test (2.5 giờ).

---

### 3. ĐÁNH GIÁ KẾT QUẢ ĐẠT ĐƯỢC

- **Giám sát hệ thống:** Tính năng Custom Metric hoạt động tốt, biểu đồ `TotalLinkClicks` phản hồi chính xác số lượng chuyển hướng thực tế (Status 301).
- **Cơ chế chống quá tải:** AWS Lambda Throttling hoạt động đúng như thiết kế (`Reserved Concurrency = 5`). Cụ thể, khi nhận 50 requests đồng thời, hệ thống chỉ xử lý 5 requests và từ chối 45 requests còn lại để bảo vệ chi phí.
- **Tồn đọng nhỏ (Tagging):** Mặc dù đã gắn trong `template.yaml`, API Gateway trên giao diện AWS Console hiện tại chỉ mới hiển thị 3 tag hệ thống của CloudFormation. Vấn đề này có thể cần tùy chỉnh sâu hơn ở cấp độ REST API stage (nằm ngoài phạm vi yêu cầu môn học). 
- Dự án đã sẵn sàng nghiệm thu và thực hiện video demo tổng kết.
