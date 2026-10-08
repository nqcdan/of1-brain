# brainstorms/ — pha Brainstorming

Thư mục này là pha **brainstorming**: chốt vấn đề + hướng tiếp cận trước khi đặc tả.

## Nhiệm vụ của AI ở đây

Khi làm việc trong thư mục này, sau khi giúp người dùng chốt ý tưởng, **luôn gợi ý đi tiếp
theo workflow**:

```
brainstorm → design → openspecs → code
```

- **brainstorm** (ở đây): làm rõ vấn đề, hướng, giả định, câu hỏi mở.
- **design**: sang `../design/` — cách làm, boundary file/module, data model, task plan.
- **openspecs**: đặc tả qua OpenSpec — `/opsx:propose "<tên-change>"` sinh proposal + specs +
  design + tasks trong `openspec/changes/<tên-change>/`.
- **code**: hiện thực ở `../code/` (TDD: test đỏ trước), rồi người review.

Mỗi artifact brainstorm: `YYMMDD-<slug>.md`. Chốt xong thì nhắc người dùng bước kế là
`design`, đừng nhảy thẳng vào code.
