# of1-brain

Nền tri thức & workspace AI-first cho OF1. Dev thao tác ở hai đầu (đặc tả & thẩm định),
AI lo khúc giữa (hiện thực). Nơi sinh ra và lưu artifact theo vòng đời công việc, tách khỏi
code sản phẩm để truy vết và tái dùng.

## Cấu trúc

| Thư mục | Vai trò |
|---|---|
| `brainstorms/` | Pha phân kỳ: vấn đề, hướng tiếp cận, giả định cần kiểm chứng (HMW → converge) |
| `openspecs/` | Spec: yêu cầu + acceptance + "Done khi (test list)" theo lối spec-driven |
| `design/` | Cách làm: boundary file/module, data model, API, task plan cho AI |
| `code/` | Hiện thực & sản phẩm code AI sinh (hoặc link/submodule tới repo code) |

## Vòng đời workflow

```
brainstorming → spec → design → spec-review → implementation → review
   (người)     (người) (người)   (AI critic)     (AI code)       (dev)
                          └──── cổng Ready-for-AI ────┘
```

- **Người** làm 3 pha đầu (brainstorming/spec/design); **AI critic** soi spec+design
  (`spec-review`) bắt mơ hồ/thiếu trước khi code; **AI** hiện thực (`implementation`);
  **dev** review code AI (`review`) và giữ nút merge.
- **Đối xứng review:** AI review *design của người* · dev review *code của AI*.
- **Cổng Ready-for-AI:** spec+design chỉ giao AI khi hết TBD, acceptance/test-list đo được,
  boundary file/module đã chốt.

Map vào 4 thư mục: `brainstorms/` (brainstorming) · `openspecs/` (spec) · `design/`
(design + spec-review) · `code/` (implementation + review).

Chi tiết convention/workflow tham chiếu bộ `knowledge/` trong `of1-harness`.
