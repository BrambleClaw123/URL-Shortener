# 🏷️ Quy Ước Gắn Nhãn (Tagging) & Giới Hạn Tài Nguyên AWS Learner Lab

Tài liệu này quy định các nguyên tắc cấu hình, phân quyền, gắn nhãn tài nguyên (Tagging) và các giới hạn kỹ thuật của môi trường **AWS Learner Lab** áp dụng xuyên suốt đề tài **Dịch vụ rút gọn URL (URL Shortener) serverless**.

---

## 1. Quy Ước Gắn Nhãn Tài Nguyên (Resource Tagging)

Mọi tài nguyên khởi tạo trên AWS trong phạm vi đồ án (DynamoDB Table, Lambda Functions, API Gateway, S3 Bucket, CloudFormation Stack) bắt buộc phải gắn đầy đủ 2 nhãn (Tag) theo quy ước sau:

| Tag Key | Tag Value | Mục đích & Ý nghĩa |
| :--- | :--- | :--- |
| `Project` | `URLShortener` | Tên dự án dùng để phân loại và theo dõi chi phí trên AWS Billing. |
| `Owner` | `24110237_24110169` | Mã số sinh viên của các thành viên thực hiện nhằm xác định người chịu trách nhiệm tài nguyên. |

> **Lưu ý:** Tag `Owner` hỗ trợ định danh người phụ trách tài nguyên trên AWS Console, không thay thế cho nhật ký hoạt động (Worklog) hằng tuần của nhóm.

---

## 2. Quy Định Về Vùng (Region) & Quyền Truy Cập (IAM)

### 2.1. Region triển khai
- **Region của Learner Lab:** Chỉ sử dụng `us-east-1` hoặc `us-west-2`.
- **Region cố định của nhóm:** `us-east-1` (N. Virginia).

### 2.2. Quyền thực thi (IAM Role & Credentials)
- **Không tạo mới IAM User / Role:** Tuân thủ giới hạn của AWS Learner Lab, nhóm sử dụng trực tiếp Role có sẵn để cấp quyền thực thi cho các dịch vụ (Lambda, API Gateway, CloudFormation).
- **Tên Role:** `LabRole`
- **Role ARN:**

        arn:aws:iam::487906062447:role/LabRole

- **Instance Profile ARN:**

        arn:aws:iam::487906062447:instance-profile/LabInstanceProfile

- **Bảo mật thông tin xác thực (AWS CLI Credentials):** Thông tin `aws_access_key_id`, `aws_secret_access_key` và `aws_session_token` được lấy từ phiên làm việc của AWS Learner Lab, có thời hạn theo phiên (session) và **tuyệt đối không được đẩy (commit) lên GitHub repository**.

---

## 3. Giới Hạn Tài Nguyên AWS Learner Lab & Cách Áp Dụng

| Hạng mục giới hạn | Quy định của AWS Learner Lab | Cách áp dụng trong đề tài |
| :--- | :--- | :--- |
| **AWS Lambda Concurrency** | Tổng concurrency không vượt quá `10`. | Đặt cấu hình `Reserved Concurrency <= 5` cho các hàm Lambda khi triển khai; thực hiện kiểm thử tải nhẹ và ghi nhận hiện tượng throttling trên CloudWatch. |
| **Amazon EC2 & Amazon EBS** | Chỉ dùng loại `nano` → `large`, tối đa 9 instance, 32 vCPU; EBS tối đa 100 GB. | Kiến trúc của đề tài thuần Serverless (API Gateway, Lambda, DynamoDB, S3) nên **không sử dụng** EC2 và EBS. |
| **Quản lý vòng đời & Chi phí** | Dừng hoặc xóa tài nguyên sau mỗi buổi thực hành; báo cáo chi phí cuối kỳ. | Dọn dẹp các tài nguyên phát sinh chi phí sau các buổi thử nghiệm; sử dụng cơ chế **DynamoDB TTL** (`ttl_expire`) để tự động xóa các liên kết hết hạn mà không tốn chi phí chạy hàm dọn dẹp riêng; tổng hợp báo cáo chi phí vào tuần cuối. |