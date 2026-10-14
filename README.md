# LIMINAL ALOK — phiên bản sửa lỗi 14/10/2026

Trang HTML/CSS/JavaScript **không cần PHP, Node hay Supabase**. Tất cả dữ liệu xuất nằm tại gói dự án. Bộ phối tự nhớ theo từng phiên bản; nút **Lưu bộ phối** và **Bộ đã lưu** lưu riêng qua localStorage trên máy người dùng.

## Chạy trên máy tính

- Windows: nhấn đúp `START_LOCAL.bat` rồi mở `http://127.0.0.1:8765/`.
- macOS / Linux: mở terminal trong thư mục này và chạy `bash start_local.sh` rồi truy cập địa chỉ trên.
- Hoặc có Python 3: `python -m http.server 8765 --bind 127.0.0.1`.
- **Không mở `index.html` bằng file://**: các trình duyệt chặn `fetch()` đọc gói .gz/.bin theo cách này.

## Đưa lên hosting

Upload **toàn bộ nội dung thư mục** lên hosting tĩnh, GitHub Pages, Cloudflare Pages hoặc host có PHP (không cần chạy PHP). File chính `index.html`. Cần upload đầy đủ `assets/runtime/`, `wardrobe-b6178fca57b6.gz`, `export-f5626d75adfe-{0,1}.bin`, các file JS/CSS. Server phải phục vụ file `.bin`, `.gz` và `.webp` như tệp tĩnh; không chặn tải xuống.

## Đã điều chỉnh

- Khôi phục nền tảng/bản game chọn trước từ trình duyệt.
- Kiểm tra độ tương thích trước khi cho xuất 4 phiên bản.
- Cho lưu/khôi phục thủ công bộ phối và giữ tự động lưu theo từng phiên bản.
- Tránh gọi hàng trăm đường dẫn ảnh trang phục chưa tồn tại (404), dùng icon danh mục có sẵn.
- Cải thiện thông báo lỗi tải dữ liệu và trình xem trước, tối ưu màn hình điện thoại.
- Bổ sung cách khởi chạy đúng qua HTTP.

## Ghi chú

Dữ liệu mod chưa được thay đổi; khả năng xuất thành công phụ thuộc dữ liệu gốc có hỗ trợ từng món. Trình duyệt có thể hỏi cho phép tải nhiều file khi chọn **Tạo 4 phiên bản**. Bản này không cung cấp tài khoản/điểm trực tuyến và không tự tải file từ dịch vụ bên ngoài.
