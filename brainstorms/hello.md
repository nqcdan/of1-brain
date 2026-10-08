---
stage: brainstorming
project: core
topic: hello
status: active
created: 261008
owner: ngcdan
related: []
---

# Hello — demo quy trình

## How Might We
Làm sao để có một hàm chào đơn giản, dùng chứng minh vòng đời brainstorming→…→review chạy thật.

## Bối cảnh
- Mục tiêu: test cơ chế quy trình, KHÔNG phải độ khó domain.
- Thành công = đi hết 6 pha, mỗi pha ra 1 artifact, `code/` có test chạy RED→GREEN thật.

## Các hướng
1. **Hàm `hello(name)`** — thuần, không I/O, dễ TDD. ✔ chọn.
2. CLI in ra stdout — thêm I/O, khó assert hơn. ✘.

## Hướng khuyến nghị
Hàm thuần `hello(name?)` trả chuỗi. Không phụ thuộc, test bằng `node:test`.

## Câu hỏi mở
- Name rỗng/whitespace xử lý sao? → để spec chốt.

## TODO (dev)
- [ ] Hàm thuần `hello(name?)` trả `"Hello, <name>!"`; rỗng/whitespace → `"Hello, World!"`.

## Summary (AI)
<!-- AI tự cập nhật khối này khi chạy pipeline. Dev không sửa tay. -->

| TODO | design | openspecs | code | review | status |
|---|---|---|---|---|---|
| hello(name?) | — | — | — | — | chưa chạy |
