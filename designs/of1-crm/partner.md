# Design — partner (hiện trạng)

Quản lý toàn bộ vòng đời đối tác (Partner): từ lead → phê duyệt hồ sơ → đồng bộ với hệ
thống ngoài (BEE_VN, BEE_INDIA, BEE_SHA) → tài liệu, phân công Salesman, shipping instruction.

## Boundary

- Package gốc `cloud.datatp.partner`. Theo RPC-style: Service → Logic → Repository → Entity.
- `CRMPartner` là aggregate root; mutation con đi qua root.

## Sub-packages

| Package | Trách nhiệm |
|---|---|
| root `cloud.datatp.partner` | Service + Logic: CRMPartner, CustomerLeads, PartnerRequest, PartnerIndex, PartnerDocument, ShippingInstruction, SalemanObligation, Subcontractor |
| `entity` | JPA entity: CRMPartner, PartnerRequest, PartnerIndex, CustomerLeads, SalemanPartnerObligation, PartnerShippingInstruction, PartnerContact, PartnerDocumentFileAttachment, ... |
| `repository` | JpaRepository cho từng entity (~12 repos) |
| `plugin` | PartnerServicePlugin, CustomerLeadServicePlugin + impl (Domestics, Overseas, Monitor, Notification, ...) |
| `event.request` | Kafka producer/consumer cho luồng phê duyệt PartnerRequest |
| `event.index` | Kafka producer/consumer đồng bộ PartnerIndex từ hệ thống ngoài |
| `integration` | BFSOne: PartnerIndexBatchSyncService, PartnerReconcileService, PartnerObligationAuditService |
| `credit` | Hồ sơ/giới hạn công nợ đối tác (dto/entity/enums) |
| `cron` | ArchiveRejectedPartnerCronJob: auto-archive request bị từ chối sau 3 ngày |

## Data model (ERD rút gọn)

- `CRMPartner` (aggregate root) ──< `CRMPartnerSource`, `CRMPartnerTransportGroup`,
  `CRMPartnerGroupRelation`, `PartnerContact`, `PartnerDocumentFileAttachment`,
  `PartnerShippingInstruction`, `SalemanPartnerObligation`; ──o| `PartnerRequest`.
- `CRMPartnerGroup` ──< `CRMPartnerGroupRelation`.
- `PartnerShippingInstruction` ──< `PartnerShippingInstructionField`.
- `PartnerIndex` ──o| `CRMPartner` (link nullable — bảng tìm kiếm nhanh sync từ ngoài).
- `CustomerLeads` ──< `PartnerContact` (lead trước khi convert thành partner chính thức).

## Luồng chính

- **Approval**: tạo `PartnerRequest` → Kafka `event.request` → duyệt/từ chối → cập nhật `CRMPartner`;
  request bị reject → cron archive sau 3 ngày.
- **Index sync**: `event.index` + `integration.PartnerIndexBatchSyncService` đồng bộ `PartnerIndex`
  từ BFSOne/BEE; `PartnerReconcileService` đối soát.
- **Lead → Partner**: `CustomerLeads` convert sang `CRMPartner`.

## Ghi chú mở rộng

- Entity con không reference parent trực tiếp (JoinColumn trên root; back-ref `updatable/insertable=false`).
- Index/constraint name ≤ 63 ký tự (giới hạn PostgreSQL).
