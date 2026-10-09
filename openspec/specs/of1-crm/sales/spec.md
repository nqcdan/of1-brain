# sales Specification

## Purpose
Quản lý vòng đời giao dịch logistics: specific quotation, booking (đồng bộ BFSOne), task
calendar của salesman, và báo cáo hiệu suất. `SpecificQuotation` và `Booking` mỗi cái sở hữu
một `SpecificServiceInquiry`.

## Requirements

### Requirement: Tạo specific quotation và match giá
Hệ thống SHALL tạo `SpecificQuotation` với inquiry lô hàng và match giá từ module price.

#### Scenario: Tạo quotation
- **WHEN** tạo một `SpecificQuotation`
- **THEN** một `SpecificServiceInquiry` được tạo kèm (cascade ALL) cùng các `QuotationCharge`
- **AND** giá được match qua `price.integration.PricingApiService`

#### Scenario: Export / gửi quotation
- **WHEN** người dùng export hoặc gửi quotation
- **THEN** hệ thống xuất XLSX hoặc gửi qua email cho khách

### Requirement: Booking đồng bộ BFSOne
Hệ thống SHALL tạo và submit/resubmit `Booking` sang hệ thống vận hành BFSOne.

#### Scenario: Submit booking
- **WHEN** một `Booking` được submit
- **THEN** mọi dòng phí nằm trong `BookingCharge`
- **AND** `integration.BFSOneCRMService` gọi REST sang BFSOne để tạo internal booking

### Requirement: Task calendar của salesman
Hệ thống SHALL quản lý lịch công tác (`TaskCalendar`) theo task group/type.

#### Scenario: Task chưa hoàn thành
- **WHEN** cron automation chạy lúc 8AM
- **THEN** các task chưa hoàn thành được xử lý/nhắc theo plugin của task group

### Requirement: Báo cáo hiệu suất kinh doanh
Hệ thống SHALL cung cấp báo cáo KPI salesman và key account.

#### Scenario: Truy vấn performance
- **WHEN** FE yêu cầu báo cáo performance
- **THEN** `PerformanceReportLogic` trả về KPI của salesman / key account (`SalemanKeyAccountReport`)
