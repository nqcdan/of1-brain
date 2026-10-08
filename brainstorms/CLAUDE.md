# brainstorms/ — điểm vào tự động (dev chỉ viết TODO)

Đây là **điểm vào duy nhất cho dev**. Dev KHÔNG viết design/spec/code tay. Dev chỉ:

1. Tạo/ mở 1 file `<slug>.md` trong thư mục này.
2. Thêm ý tưởng dưới dạng **TODO** ở mục `## TODO (dev)`.

Phần còn lại **AI tự động chạy**.

## Cấu trúc file brainstorm (bắt buộc)

```markdown
## TODO (dev)
- [ ] <việc / ý tưởng dev muốn làm>
- [ ] ...

## Summary (AI)
<!-- AI tự ghi/ cập nhật khối này NGAY DƯỚI mục TODO. Dev không sửa tay. -->
```

- Dev chỉ đụng `## TODO (dev)`. Khối `## Summary (AI)` do AI sở hữu.
- TODO chưa tick = AI nhận việc; AI tick `[x]` khi chạy xong cả pipeline cho mục đó.

## AI tự động làm gì

Khi thấy TODO chưa xử lý (chưa tick, chưa có trong Summary), chạy **liền mạch** cả pipeline,
KHÔNG dừng hỏi giữa các pha (continuous execution). Thứ tự:

```
brainstorm(TODO) → design → openspecs(spec) → code → review
```

1. **design** → tạo `../design/<slug>.md`: cách làm, boundary file/module, data model, task plan.
2. **openspecs (spec)** → `/opsx:propose "<slug>"`: sinh `openspec/changes/<slug>/` (proposal + specs + design + tasks).
3. **code** → hiện thực ở `../code/<slug>/` theo **TDD** (viết test, xem fail đỏ, rồi code cho xanh).
4. **review** → tự `/code-review` + chạy test; sửa hết CRITICAL/HIGH trước khi báo dev.

Xong mỗi mục: tick `[x]` TODO đó và cập nhật **Summary** với link + trạng thái từng pha.

## Khối Summary — định dạng

| TODO | design | openspecs | code | review | status |
|---|---|---|---|---|---|
| <tóm tắt todo> | `../design/<f>.md` | `openspec/changes/<slug>/` | `../code/<slug>/` | test ✓ / findings | done / in-progress / blocked |

## Quy tắc an toàn

- TODO mơ hồ (ảnh hưởng scope/hành vi/acceptance) → ghi **giả định** vào design + 1 dòng ở
  Summary (`assumption: ...`), vẫn chạy tiếp. Chỉ **dừng hỏi dev** khi mơ hồ thật sự chặn.
- TODO chạm code sản phẩm thật (ngoài `code/` demo) → dừng, hỏi trước (RED).
- Luôn TDD: không viết code khi chưa có test đỏ.
