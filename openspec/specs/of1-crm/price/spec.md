# price Specification

## Purpose
Quản lý định giá: bảng giá vận chuyển (Sea FCL/LCL, Air, Truck, Oil), tiếp nhận/xử lý Inquiry
Request từ Sales, SLA định giá tự động, Price Feedback, external price, và pricing API nội bộ.

## Requirements

### Requirement: Tiếp nhận và xử lý Inquiry Request
Hệ thống SHALL tiếp nhận yêu cầu báo giá (`InquiryRequest`) và theo dõi qua workflow theo step.

#### Scenario: Tạo inquiry request
- **WHEN** Sales tạo một `InquiryRequest` (có thể multi-route, bulk cargo)
- **THEN** một `InquiryWorkflow` được khởi tạo với các `InquiryWorkflowStepTracking`

### Requirement: SLA định giá tự động
Hệ thống SHALL theo dõi SLA định giá và escalate qua cron job.

#### Scenario: Quá hạn phản hồi
- **WHEN** một inquiry request không được phản hồi trong ngưỡng SLA
- **THEN** cron cập nhật trạng thái (No Response / SLA Pricing) và gửi thông báo, escalate mail Director khi cần

### Requirement: Price Feedback
Hệ thống SHALL ghi nhận phản hồi giá gắn với bảng giá Sea FCL/LCL.

#### Scenario: Ghi feedback
- **WHEN** một phản hồi giá được tạo cho `SeaFclTransportCharge`/`SeaLclTransportCharge`
- **THEN** một `PriceFeedback` được lưu liên kết tới charge tương ứng

### Requirement: Pricing API nội bộ cho module khác
Module khác SHALL tra cứu giá chỉ qua `PricingApiService`, không truy cập entity price trực tiếp.

#### Scenario: Sales match giá
- **WHEN** module `sales` cần match giá cho quotation
- **THEN** nó gọi `integration.PricingApiService` để lấy giá

### Requirement: Import bảng giá từ Excel
Hệ thống SHALL parse file Excel bảng giá (Air, Sea, Truck) thành charge entity.

#### Scenario: Upload bảng giá
- **WHEN** một file Excel bảng giá được upload
- **THEN** `parser` đọc và persist các charge entity tương ứng
