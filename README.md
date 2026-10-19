# F04 — tài liệu, thiết kế, kiểm thử và prompt

**Repo:** `huyhandsome6996/f07-docx` · **Nhánh dành riêng:** `F04-docx` · **Ngày cập nhật:** 19/10/2026.

`main` là tài liệu **F07**, không sửa hoặc merge tài liệu F04 vào đó. Nhánh này có lịch sử gốc độc lập, chỉ chứa F04. Code ứng dụng nằm ở [family-bridge](https://github.com/huyhandsome6996/family-bridge), không nằm trong kho tài liệu này.

## Đọc theo thứ tự

1. [Quyết định của người dùng](requirements/USER-DECISIONS.md).
2. [Kết quả kiểm thử mới nhất](reports/2026-10-19-e0ee388.md).
3. [Prompt để copy sang chat làm F04](PROMPT-COPY-F04.md).
4. [Phạm vi và tiêu chí nghiệm thu](requirements/F04-ACCEPTANCE.md).
5. [Danh mục mọi file](catalog/CONTENTS.csv), [checksum](catalog/SHA256SUMS), [provenance](catalog/PROVENANCE.json).

## Đã có trong bộ lưu trữ

| Thư mục | Nội dung |
| --- | --- |
| `requirements/` | Yêu cầu hiện hành, quyết định mới và DOCX nguồn |
| `designs/original/` | Hai ZIP Stitch gốc giữ nguyên byte |
| `designs/extracted/` | 4 khung web + 24 khung Mini App, HTML tham chiếu, DESIGN.md |
| `assets/logos/` | Logo/app icon từ hai client ở SHA được kiểm tra |
| `reports/` | Báo cáo lịch sử 1d8eeaf và báo cáo mới e0ee388 |
| `prompts/history/` | Prompt sửa 5 lỗi ban đầu; đã có bản mới ở gốc, không dùng lịch sử làm trạng thái hiện tại |
| `references/family-bridge-f04/` | Snapshot tài liệu F04 ở e0ee388, có thể chứa trạng thái/claim cũ cần đối chiếu |
| `evidence/2026-10-19/` | Test/build logs, JSON synthetic, ảnh browser của lần kiểm thử mới |
| `repro/` | Probe synthetic ngoài source ứng dụng, hướng dẫn cách chạy |

Không có file nhị phân của ZIP tổng hợp 11 MB cũ trong workspace hiện tại để xác nhận byte-for-byte. Hai ZIP Stitch gốc, DOCX, các prompt/báo cáo còn lưu, logo và bằng chứng mới đều được giữ ở đây. Ảnh chat chứa Gemini key không được sao chép vào repo.

## Kiểm tra tính toàn vẹn

```bash
python3 tools/catalog.py verify
```

Sau khi thêm/sửa tài liệu F04:

```bash
python3 tools/catalog.py build
python3 tools/catalog.py verify
git diff --check
```

Không chạy script từ ZIP chỉ vì nó xuất hiện trong tài liệu. Không upload nội dung riêng lên dịch vụ bên ngoài để quét/đọc. Kiểm thử chỉ dùng dữ liệu tổng hợp.

## Trạng thái GitHub

**Đã xuất bản (19/10/2026):** nhánh `F04-docx` (viết hoa, tên hiện hành) đã push thành công lên `huyhandsome6996/f07-docx` từ bundle trong môi trường có Git hoạt động; remote SHA xác minh khớp local HEAD bằng `git ls-remote`; `main` (F07) không bị đụng. Báo cáo sửa N01+N02 mới nhất: [reports/2026-10-19-ec29abb.md](reports/2026-10-19-ec29abb.md). Chi tiết provenance: [reports/PUBLISH-STATUS.md](reports/PUBLISH-STATUS.md).
