# OF1 CRM — Specs Overview

Tập hợp capability spec phản ánh **hiện trạng đã implement** của dự án `of1-crm`. Mỗi module
= một capability, spec tại `of1-crm/<module>/spec.md`. Đây là trạng thái ổn định (specs/),
không phải proposal đang chạy (changes/).

## Capabilities

| Capability | Spec | Vai trò |
|---|---|---|
| core | `of1-crm/core/spec.md` | Hạ tầng chung: enum/constant, DAO base, integration RPC, email/Kafka, config, tracking, user sync |
| partner | `of1-crm/partner/spec.md` | Vòng đời đối tác: lead, approval, index sync, document, salesman, shipping instruction |
| price | `of1-crm/price/spec.md` | Định giá, Inquiry Request + SLA, Price Feedback, pricing API nội bộ |
| sales | `of1-crm/sales/spec.md` | Quotation, booking, task calendar, performance report, tích hợp BFSOne |
| reports | `of1-crm/reports/spec.md` | Báo cáo BD read-only qua Groovy SQL |

## Ràng buộc chung (toàn hệ CRM)

- Backend RPC-style: FE map vào `@Service` bean qua `createHttpBackendCall`, không REST controller.
- Phân tầng Service → Logic → Repository → Entity; mọi Logic extends `CRMDaoService`.
- Mọi business method nhận `ClientContext client` đầu tiên (FE không truyền).
- Transaction tường minh; read dùng `transactionManager = "crmTransactionManager"`.
- DDD Aggregate: mutation con đi qua root; không `save()` entity con trực tiếp.
- Schema change append vào `module/core/.../changes/002-schema-changes.sql` (Liquibase idempotent).

Design chi tiết: `../../designs/of1-crm/`. Nguồn gốc: `of1-crm/module/<module>/README.md`.
