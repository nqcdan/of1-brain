# reports Specification

## Purpose
Báo cáo nghiệp vụ cho phòng BD, đọc dữ liệu chéo module qua Groovy SQL. Read-only: không
entity ghi, không transaction ghi, không repository Spring Data.

## Requirements

### Requirement: Báo cáo read-only qua Groovy SQL
Hệ thống SHALL thực hiện mọi báo cáo qua `CRMDaoService.searchDbRecords` với Groovy SQL script,
không ghi dữ liệu.

#### Scenario: FE gọi báo cáo
- **WHEN** FE gọi `BDService` cho một báo cáo
- **THEN** `BusinessReportLogic` delegate tới Groovy SQL script và trả về `List<SqlMapRecord>`
- **AND** không có thao tác ghi nào được thực hiện

### Requirement: Áp quyền truy cập theo account/company
Mọi báo cáo SHALL áp filter quyền trước khi query.

#### Scenario: Resolve permission
- **WHEN** một báo cáo được yêu cầu
- **THEN** `CRMPermissionResolver.computePermission` gán filter `accessAccountId` / `accessibleAccountIds` / `companyId` vào `sqlParams`

### Requirement: Các báo cáo BD chuẩn
Hệ thống SHALL cung cấp các báo cáo: Saleman Quotation, Salesman Performance Metrics, Partner
Performance Metrics, Market Performance Metrics.

#### Scenario: Market performance phân loại hành trình
- **WHEN** chạy Market Performance Metrics
- **THEN** dữ liệu inquiry được phân theo hành trình (from/to location) và phân loại VIETNAM vs THIRD_COUNTRY (dùng LocationService qua internal call)
