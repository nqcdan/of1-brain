# Setup

## TODO (dev)
- [ ] TODO 1 (repo-reference → buồng lái): AI đọc code thật 4 repo sản phẩm (`of1-platform`, `of1-crm`, `of1-core`, `webui-lib`) để grounding design/spec, VÀ sinh code thẳng vào repo đích — có guardrail. Scope đã làm rõ (interview):
    - **Không** manifest/map tĩnh, **không** helper resolve. Chỉ khai "search surface" trong CLAUDE.md: 4 repo + vị trí sibling + `stack` + `entrypoints` (để khoanh vùng, grep-first tránh nổ token).
    - **Grounding:** AI tự grep/search 4 repo mỗi lần → định vị module → đọc → đặc tả bám hiện trạng. Ghi vị trí tìm được thành `refs:` (truy vết, sản phẩm phụ).
    - **Thực thi:** AI tạo nhánh `ai/<slug>` off `develop` trong repo đích, commit. **KHÔNG merge, KHÔNG push develop** — dừng, dev duyệt (guardrail nhánh-riêng).
    - **Pivot bản chất:** đảo protocol hiện tại (code thật = cổng RED cấm) → code thật là đích thực thi, gate bằng nhánh+duyệt. Phải viết lại `brainstorms/CLAUDE.md`.
    - **Canh bạc cần test trước:** AI tự dò đúng module bằng search (không map tĩnh) trên repo Gradle lớn — test rẻ 3 feature + đo token trước khi rewrite protocol.
    - Open: base/tên nhánh `ai/<slug>` off develop OK? · grounding quét cả 4 repo hay TODO chỉ định repo đích để thu hẹp?

## Summary (AI)
<!-- AI tự ghi/cập nhật khối này NGAY DƯỚI mục TODO. Dev không sửa tay. -->
