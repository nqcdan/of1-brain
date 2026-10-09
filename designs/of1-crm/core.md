# Design — core (hiện trạng)

Module nền tảng dùng chung cho toàn bộ OF1 CRM. Cung cấp hạ tầng cốt lõi; mọi Logic class
ở các module khác extends `CRMDaoService` từ đây.

## Boundary

- Package gốc `cloud.datatp.core` (+ `net.datatp.module.config`).
- Không chứa nghiệp vụ domain (partner/price/sales) — chỉ hạ tầng + enum/constant chung.
- Là dependency của mọi module khác.

## Sub-packages

| Package | Trách nhiệm |
|---|---|
| `common` | Enum/constant chung: `InquiryStatus`, `ContainerType`, `FreightTerm`, `TransportationMode`, `PartnerType`, `PartnerGroup`, `TypeOfService`, `Scope`, `Purpose`, `KafkaMessage` |
| `db` | DAO hạ tầng: `CRMDaoService` (base cho mọi Logic), `CRMSqlQueryUnitManager` (chạy Groovy SQL), `CRMDAOTemplatePrimary` |
| `groovy` | Groovy SQL script động cho query phức tạp (`BDSql`, `UserInfoSql`, `CRMMessageSystemSql`, ...) |
| `integration` | RPC sang Platform (`PlatformClient`) và FMS (`FmsClient`); `InternalCallGateway` là single entry point CRM → Platform/FMS |
| `message` | Email async: lưu `CRMMessageSystem`, publish/consume Kafka, retry, cron gửi theo lịch |
| `notification` | Alert nội bộ qua Telegram (`TelegramAlertService`, `TelegramMessage`) |
| `template` | Config theo công ty (`CrmCompanyConfig`) + hệ thống (`CrmSystemConfig`), `CustomList` |
| `tracking` | AOP tracking call ra ngoài (FMS/BFSOne): `@Tracked`, `TrackedCallAspect`, lưu `ApiCallTrace`, alert khi vượt ngưỡng lỗi |
| `user` | `UserInfo` đồng bộ từ Kafka Identity Event của Platform |
| `milestone`, `idempotency`, `cron`, `kafka` | Hạ tầng phụ: milestone tracking, chống xử lý trùng, cron base, Kafka helper |

## Data model chính

- `CRMMessageSystem` — hàng đợi email: `message_type`, `status`, `scheduled_at`, `plugin_name`,
  `reference_id/type`, `recipients`, `metadata`, `content`, `error_message`, `retry_count`.
- `UserInfo` — thông tin user CRM sync từ Identity Event.
- `CrmCompanyConfig` / `CrmSystemConfig` / `CustomList` — cấu hình.
- `ApiCallTrace` — vết call ra ngoài (async).

## Luồng chính

- **Email async**: Logic → lưu `CRMMessageSystem` → publish Kafka → consumer gửi → retry/cron theo lịch.
- **Outbound RPC**: mọi call CRM → Platform/FMS đi qua `InternalCallGateway` (+ `@Tracked` ghi `ApiCallTrace`).
- **User sync**: consume Kafka Identity Event → upsert `UserInfo`.

## Ghi chú mở rộng

- Thêm enum/constant dùng chung → đặt ở `common`, không nhân bản trong module khác.
- Thêm call ra ngoài → qua `InternalCallGateway` + annotate `@Tracked`.
