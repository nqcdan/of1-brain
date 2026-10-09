# Design — sales (hiện trạng)

Quản lý vòng đời giao dịch logistics từ khi khách gửi yêu cầu đến khi booking được xác nhận
và đồng bộ sang hệ thống vận hành BFSOne. Bốn mảng: specific quotation, booking, task calendar,
report; kèm tích hợp hai chiều với BFSOne.

## Boundary

- Package gốc `cloud.datatp.sales`. RPC-style: Service → Logic → Repository → Entity.
- `SpecificQuotation` và `Booking` mỗi cái sở hữu một `SpecificServiceInquiry` (cascade ALL).

## Sub-packages

| Package | Trách nhiệm |
|---|---|
| `booking` | Tạo/lưu/submit/resubmit Booking sang BFSOne; dòng phí trong `BookingCharge` |
| `quotation` | Tạo SpecificQuotation, match giá từ price module, export XLSX / gửi email |
| `inquiry` | `SpecificServiceInquiry` — thông tin lô hàng đính kèm mỗi quotation/booking |
| `common` | QuotationCharge, QuotationAdditionalCharge, ContainerType; CustomerChargeLogic |
| `taskcalendar` / `project` | TaskCalendar (lịch công tác sales), TaskTypeDefinition, plugin per task group, notification |
| `report` | SalemanKeyAccountReport, PerformanceReportLogic — KPI salesman + key account |
| `integration` | BFSOneCRMLogic/Service — REST sang BFSOne tạo/xóa internal booking |
| `automation` | CronJob: update feedback price 2 lần/ngày, xử lý task chưa hoàn thành 8AM |

## Data model (ERD rút gọn)

- `SpecificQuotation` ──|| `SpecificServiceInquiry` (owns, cascade ALL);
  ──< `QuotationCharge`, `QuotationAdditionalCharge` (local handling).
- `Booking` ──|| `SpecificServiceInquiry` (owns, cascade ALL); ──< `BookingCharge` (mọi dòng phí).
- `SpecificServiceInquiry` ──< `Container` (cascade ALL).
- `TaskCalendar` ──< `TaskCalendarFileAttachment`; `TaskTypeDefinition` }o──o{ `TaskCalendar`
  (theo `taskGroupCode` + `taskTypeCode`).
- `SalemanKeyAccountReport` { saleman_account_id, period, status }.

## Luồng chính

- **Quote**: tạo `SpecificQuotation` (+ inquiry) → match giá qua `PricingApiService` (module price)
  → export XLSX hoặc gửi email khách.
- **Booking**: tạo `Booking` → submit/resubmit sang BFSOne qua `integration.BFSOneCRMService` (REST).
- **Task**: `TaskCalendar` lịch công tác; cron 8AM xử lý task chưa hoàn thành.
- **Report**: `PerformanceReportLogic` tổng hợp KPI salesman/key account.

## Ghi chú mở rộng

- Giá luôn lấy qua `price.integration.PricingApiService`, không query entity price trực tiếp.
- Mọi call BFSOne đi qua `integration` + `@Tracked`.
