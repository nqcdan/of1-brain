# Design — price (hiện trạng)

Quản lý toàn bộ nghiệp vụ định giá: bảng giá vận chuyển (Sea FCL/LCL, Air, Truck, Oil),
tiếp nhận/xử lý Inquiry Request từ Sales, SLA định giá tự động, Price Feedback, external
price, và expose API nội bộ cho module khác.

## Boundary

- Package gốc `cloud.datatp.price`. RPC-style: Service → Logic → Repository → Entity.
- Expose `integration.PricingApiService` cho module khác (đặc biệt `sales`) tra cứu giá.

## Sub-packages

| Package | Trách nhiệm |
|---|---|
| root `cloud.datatp.price` | Service + Logic bảng giá: Sea FCL/LCL, Air, Truck, Oil Price; xuất/nhập Excel; external; Price Feedback |
| `request` | Tiếp nhận & xử lý Inquiry Request (yêu cầu báo giá) + SLA tracking |
| `entity` | JPA entity: bảng giá nội bộ + ngoại bộ, phụ phí, giá dầu, phản hồi giá |
| `cron` | CronJob: cập nhật No Response, SLA Pricing, SLA mail Director, Mismatch, Bulk Cargo |
| `parser` | Parse Excel bảng giá (Air, Sea, Truck) |
| `plugin` | Message plugin: gửi Zalo/mail theo sự kiện (reject, mismatch, overdue, SLA, ...) |
| `integration` | RPC API nội bộ `PricingApiService` để module khác tra cứu giá |
| `common` | Model dùng chung: nhóm giá, chi tiết lô hàng, template mail Sea |
| `net.datatp.logistics.intg.carrier.maersk` | Tích hợp API hãng tàu Maersk |

## Data model (ERD rút gọn)

- `InquiryRequest` ──o| `InquiryWorkflow` ──< `InquiryWorkflowStepTracking`.
- `InquiryRequest` ──< `InquiryRequestRoute` (multi-route), `InquiryRequestAttachment`;
  ──o| `BulkCargoInquiryRequest` (biến thể bulk cargo).
- `SeaFclTransportCharge` / `SeaLclTransportCharge` ──< `PriceFeedback`.
- Bảng giá: `SeaFclTransportCharge`, `SeaLclTransportCharge`, (+ Air/Truck/Oil charge) với
  `code`, `from_location_code`, `to_location_code`, ...

## Luồng chính

- **Inquiry → quote**: Sales tạo `InquiryRequest` → `InquiryWorkflow` theo step → pricing team
  điền giá → `PriceFeedback`; SLA theo dõi qua cron (No Response, SLA Pricing, escalate Director).
- **Tra giá liên module**: `sales` gọi `PricingApiService` để match giá vào quotation.
- **Import bảng giá**: `parser` đọc Excel → persist charge entity.

## Ghi chú mở rộng

- Thêm sự kiện thông báo giá → thêm plugin trong `plugin`, không nhét vào Logic.
- Giá cho module khác → chỉ qua `PricingApiService`, không cho truy cập entity trực tiếp.
