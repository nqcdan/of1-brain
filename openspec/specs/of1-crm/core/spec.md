# core Specification

## Purpose
Module nền tảng dùng chung cho toàn bộ OF1 CRM: enum/constant chung, DAO base, cầu nối RPC
sang Platform/FMS, email async qua Kafka, cấu hình công ty/hệ thống, tracking call ngoài, và
đồng bộ user từ Identity Event.

## Requirements

### Requirement: DAO base cho mọi Logic
Mọi Logic class trong các module khác SHALL extends `CRMDaoService` và chạy query Groovy SQL
qua `searchDbRecords`.

#### Scenario: Chạy Groovy SQL script
- **WHEN** một Logic gọi `searchDbRecords(scriptFile, "SearchXxx", sqlParams)`
- **THEN** `CRMSqlQueryUnitManager` thực thi script và trả về `List<SqlMapRecord>`

### Requirement: Single entry point gọi ra ngoài
Mọi lời gọi CRM → Platform/FMS SHALL đi qua `InternalCallGateway`.

#### Scenario: Gọi Platform/FMS
- **WHEN** một module cần gọi Platform hoặc FMS
- **THEN** nó dùng `PlatformClient`/`FmsClient` thông qua `InternalCallGateway`, không gọi trực tiếp

### Requirement: Email gửi bất đồng bộ qua Kafka
Hệ thống SHALL lưu email vào `CRMMessageSystem` rồi gửi qua Kafka với retry và cron theo lịch.

#### Scenario: Gửi email
- **WHEN** một module phát sinh email cần gửi
- **THEN** một bản ghi `CRMMessageSystem` (status, scheduled_at, recipients, content) được tạo và publish Kafka
- **AND** gửi thất bại thì tăng `retry_count` và ghi `error_message`

### Requirement: Tracking call ra ngoài
Các call tới FMS/BFSOne SHALL được tracking qua AOP và alert khi vượt ngưỡng lỗi.

#### Scenario: Call được annotate @Tracked
- **WHEN** một method được annotate `@Tracked` thực thi
- **THEN** `TrackedCallAspect` lưu `ApiCallTrace` bất đồng bộ
- **AND** khi tỉ lệ lỗi vượt ngưỡng thì gửi alert Telegram

### Requirement: Đồng bộ thông tin user
Hệ thống SHALL đồng bộ `UserInfo` từ Kafka Identity Event của Platform.

#### Scenario: Nhận Identity Event
- **WHEN** một Identity Event được consume từ Kafka
- **THEN** `UserInfo` tương ứng được upsert
