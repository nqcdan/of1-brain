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

## Vòng đời

```
brainstorms → openspecs → design → code
  (người)      (người)    (người)   (AI + review người)
                   └── cổng Ready-for-AI ──┘
```

Người viết brainstorm/spec/design; qua cổng Ready-for-AI thì AI nhận việc ở `code/`;
người review lại. Chi tiết convention/workflow tham chiếu bộ `knowledge/` trong `of1-harness`.
