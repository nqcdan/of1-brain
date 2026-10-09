# of1-brain

Nền tri thức & workspace AI-first cho OF1. Dev thao tác ở hai đầu (đặc tả & thẩm định),
AI lo khúc giữa (hiện thực). Nơi sinh ra và lưu artifact theo vòng đời công việc, tách khỏi
code sản phẩm để truy vết và tái dùng.

## Cấu trúc

| Thư mục | Vai trò |
|---|---|
| `brainstorms/` | Pha phân kỳ: vấn đề, hướng tiếp cận, giả định cần kiểm chứng (HMW → converge) |
| `openspec/` | Spec: yêu cầu + acceptance + "Done khi (test list)" theo lối spec-driven |
| `designs/` | Cách làm: boundary file/module, data model, API, task plan cho AI |
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

Map vào 4 thư mục: `brainstorms/` (brainstorming) · `openspec/` (spec) · `designs/`
(design + spec-review) · `code/` (implementation + review).

Chi tiết convention/workflow tham chiếu bộ `knowledge/` trong `of1-harness`.

## OpenSpec — spec-driven cho pha spec

Pha `spec` (thư mục `openspec/`) chạy theo **OpenSpec** — framework spec-driven cho AI
coding assistant: https://github.com/Fission-AI/openspec

Bộ tích hợp Claude Code của OpenSpec đã **vendored sẵn** trong repo này (không cần cài gì
để đọc), tại `.claude/`:

- `.claude/skills/openspec-*` — 6 skill: `explore` · `propose` · `apply` · `sync-specs` ·
  `update-change` · `archive-change`.
- `.claude/commands/opsx/*` — 6 slash-command tương ứng: `/opsx:explore`, `/opsx:propose`,
  `/opsx:apply`, `/opsx:sync`, `/opsx:update`, `/opsx:archive`.

### Cài CLI để kích hoạt

Các skill gọi CLI `openspec` (`allowed-tools: Bash(openspec:*)`), nên muốn **chạy** cần cài CLI:

```bash
npm install -g @fission-ai/openspec@latest   # hoặc: brew install openspec
openspec init --tools claude                 # tạo thư mục dữ liệu openspec/ (specs + changes)
```

`openspec init` sinh lại `.claude/` (đã có sẵn đây) và tạo `openspec/` chứa `specs/` +
`changes/`. Sau đó dùng vòng: `/opsx:explore` → `/opsx:propose "ý tưởng"` → `/opsx:apply`
→ `/opsx:archive`.

> Repo chỉ vendored phần skill/command (để đọc + versioned). CLI là tooling máy-local,
> KHÔNG commit vào repo.
