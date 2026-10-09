# Design — reports (hiện trạng)

Báo cáo nghiệp vụ phục vụ phòng BD (Business Development). Đọc dữ liệu chéo module (core,
partner, price, sales/logistics) qua Groovy SQL script. **Read-only**: không entity riêng,
không ghi dữ liệu, không repository Spring Data.

## Boundary

- Package gốc `cloud.datatp.reports`. Chỉ luồng đọc, không transaction ghi.
- Truy vấn qua `CRMDaoService.searchDbRecords(scriptFile, "SearchXxx", sqlParams)` (Groovy SQL).

## Sub-packages

| Package | Trách nhiệm |
|---|---|
| `bd` | `BDService` + `BusinessReportLogic` — entry point các báo cáo BD; `dto` kết quả |
| `performance` | Logic/KPI hiệu suất (có `entity`/`repository` phụ cho dữ liệu tổng hợp nếu cần) |
| `groovy` | Groovy SQL script: `QuotationReportSql`, performance metrics, market metrics, ... |

## Các báo cáo chính

| Báo cáo | Mô tả | Nguồn dữ liệu chính |
|---|---|---|
| Saleman Quotation Report | Báo giá theo salesman + partner, kèm khối lượng FCL/LCL/Air | `lgc_price_inquiry_request`, `lgc_forwarder_crm_partner`, `lgc_sales_specific_service_inquiry` |
| Salesman Performance Metrics | KPI salesman: #inquiry, win rate, volume, #khách mới, #cuộc họp | `lgc_price_inquiry_request`, `user_info`, `crm_sales_task_calendar`, `lgc_forwarder_crm_partner_group_rel`, `forwarder_customer_leads` |
| Partner Performance Metrics | Inquiry theo đối tác, phân theo mode vận chuyển | `lgc_price_inquiry_request`, `lgc_forwarder_crm_partner`, `user_info` |
| Market Performance Metrics | Phân tích thị trường theo hành trình (from/to), VIETNAM vs THIRD_COUNTRY | `lgc_price_inquiry_request`, `user_info` + LocationService |

## Luồng chính (read-only)

```
FE → BDService.createHttpBackendCall(...)
   → BusinessReportLogic.delegate(client, sqlParams)
      → CRMPermissionResolver.computePermission(client, sqlParams)
         (gán filter accessAccountId / accessibleAccountIds / companyId)
      → searchDbRecords(scriptFile, "SearchXxx", sqlParams)
         → Groovy SQL build + execute (dynamic filter)
         → List<SqlMapRecord>
```

## Ghi chú mở rộng

- Thêm báo cáo → thêm Groovy SQL script + method trong `BusinessReportLogic`, không tạo entity ghi.
- Luôn áp `CRMPermissionResolver` để filter theo quyền truy cập account/company.
