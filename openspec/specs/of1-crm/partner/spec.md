# partner Specification

## Purpose
Quản lý vòng đời đối tác (Partner): lead, phê duyệt hồ sơ, đồng bộ index với hệ thống ngoài
(BEE_VN/BEE_INDIA/BEE_SHA), tài liệu, phân công Salesman và shipping instruction. `CRMPartner`
là aggregate root.

## Requirements

### Requirement: Phê duyệt hồ sơ đối tác
Hệ thống SHALL quản lý phê duyệt partner qua `PartnerRequest` với luồng Kafka approval.

#### Scenario: Tạo và duyệt request
- **WHEN** một `PartnerRequest` được tạo
- **THEN** event được publish qua Kafka `event.request` để xử lý phê duyệt
- **AND** khi được duyệt thì `CRMPartner` tương ứng được cập nhật trạng thái

#### Scenario: Auto-archive request bị từ chối
- **WHEN** một `PartnerRequest` ở trạng thái rejected quá 3 ngày
- **THEN** `ArchiveRejectedPartnerCronJob` tự động archive request đó

### Requirement: Đồng bộ PartnerIndex từ hệ thống ngoài
Hệ thống SHALL đồng bộ `PartnerIndex` (bảng tìm kiếm nhanh) từ BFSOne/BEE và đối soát.

#### Scenario: Batch sync index
- **WHEN** `PartnerIndexBatchSyncService` chạy hoặc nhận event `event.index`
- **THEN** `PartnerIndex` được cập nhật, link tới `CRMPartner` (nullable nếu chưa khớp)
- **AND** `PartnerReconcileService` đối soát chênh lệch giữa CRM và hệ thống ngoài

### Requirement: Lead chuyển đổi thành Partner
Hệ thống SHALL quản lý `CustomerLeads` trước khi convert thành `CRMPartner` chính thức.

#### Scenario: Convert lead
- **WHEN** một `CustomerLeads` đủ điều kiện được convert
- **THEN** một `CRMPartner` được tạo, giữ liên kết contact từ lead

### Requirement: Mutation qua aggregate root
Mọi thay đổi entity con (contact, document, shipping instruction, obligation) SHALL đi qua
`CRMPartner` aggregate root.

#### Scenario: Cập nhật entity con
- **WHEN** cần thêm/sửa một `PartnerContact`/`PartnerDocumentFileAttachment`/`PartnerShippingInstruction`
- **THEN** thao tác đi qua `CRMPartner`, không `save()` entity con trực tiếp
