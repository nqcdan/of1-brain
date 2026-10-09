# Design — OF1 CRM (overview hiện trạng)

Tài liệu phản ánh **hiện trạng** của dự án `of1-crm` (CRM module cho OF1 Logistics
Platform). Dùng làm điểm vào cho các design per-module trong cùng thư mục.

## Kiến trúc tổng

- **Backend**: Java 21, Spring Boot 3.2.4, Gradle multi-module.
- **Frontend**: React 18 + TypeScript (`@of1-webui/crm`), đóng gói UMD bundle.
- **Database**: PostgreSQL (`of1-crm` primary).
- **Messaging**: Kafka (email async, đồng bộ partner index, identity event, approval flow).
- Port local: CRM BE `7083`, CRM FE `3003`, platform web `8080`.

## Module map (Gradle)

| Module | projectDir | Vai trò |
|---|---|---|
| `core` | `module/core` | Nền tảng dùng chung: enum/constant, DAO base, integration RPC, email/Kafka, config, tracking, user sync |
| `partner` | `module/partner` | Vòng đời đối tác: lead → approval → index → document → salesman → shipping instruction |
| `price` | `module/price` | Định giá (Sea FCL/LCL, Air, Truck, Oil), Inquiry Request + SLA, Price Feedback, external price |
| `sales` | `module/sales` | Specific quotation, booking, task calendar, report, tích hợp BFSOne |
| `reports` | `module/reports` | Báo cáo BD read-only qua Groovy SQL (không entity riêng) |
| `app/server` | `app/server` | Spring Boot app lắp ráp các module |
| `release` | `release` | Đóng gói release |

Package gốc: `cloud.datatp.<module>` (+ `net.datatp.module.config`). Mọi Logic class
extends `CRMDaoService` ở module `core`.

## Kiến trúc backend RPC-style (không REST controller cho WebUI)

Frontend không gọi REST endpoint; nó map thẳng vào Spring `@Service` bean qua
`appContext.createHttpBackendCall("ServiceName", "methodName", params)` (hoặc
`createHttpRemoteBackendCall("crm", ...)`). Phân tầng:

```
Service (@Service, transaction + permission/context)
   → Logic (*Logic, pure business, extends CRMDaoService/BaseComponent, no transaction)
      → Repository (JpaRepository, @Query)
         → Entity (PersistableEntity<Long> | CompanyEntity)
```

- Mọi business method nhận `ClientContext client` làm tham số **đầu tiên** (FE không truyền).
- Params FE match với tham số Java **theo tên** (compile `-parameters`) → typo key = null arg âm thầm.
- Transaction tường minh: read dùng `@Transactional(readOnly = true, transactionManager = "crmTransactionManager")`.
- DDD Aggregate: mọi mutation con đi qua Aggregate Root, không `save()` entity con trực tiếp.

## Quan hệ liên module

```
sales ──(match giá)──▶ price.integration.PricingApiService
sales ──(tạo/xóa internal booking REST)──▶ BFSOne
partner ──(đồng bộ index/obligation)──▶ BFSOne (BEE_VN/BEE_INDIA/BEE_SHA)
reports ──(đọc chéo bảng)──▶ core/partner/sales/price (Groovy SQL, read-only)
mọi module ──(RPC ra ngoài)──▶ core.integration.InternalCallGateway → Platform/FMS
mọi module ──(email async)──▶ core.message (Kafka)
```

## DB schema change (quy ước)

Mọi thay đổi schema/migration append vào **một** file changelog cuốn chiếu:
`module/core/src/main/resources/db/changelog/changes/002-schema-changes.sql` (Liquibase,
idempotent DDL + `--rollback`, không sửa/đổi thứ tự changeset cũ).

## Nguồn tham chiếu trong repo gốc

- Master index: `of1-crm/CLAUDE.md`
- Domain rules: `of1-crm/docs/ai/{backend,frontend,devops,kafka,docs}-rules.md`, `ui-component-conventions.md`
- README per-module: `of1-crm/module/<module>/README.md`
