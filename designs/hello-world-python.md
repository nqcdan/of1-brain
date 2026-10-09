# Design — hello world function (Python)

## Mục tiêu
Một hàm Python trả về lời chào "Hello, World!", có thể chào tên tuỳ biến.

## Boundary
- Chỉ nằm trong `code/hello-world-python/` (demo, không chạm code sản phẩm thật).
- Không phụ thuộc thư viện ngoài; chuẩn `pytest` cho test.

## API
```python
def hello(name: str = "World") -> str
```
- `hello()` → `"Hello, World!"`
- `hello("Dan")` → `"Hello, Dan!"`
- `name` rỗng/chỉ khoảng trắng → fallback về `"World"`.

## Data model
Không có state. Pure function, input `str`, output `str`.

## Task plan (TDD)
1. Viết `test_hello.py` (3 case: mặc định, có tên, tên rỗng) → chạy fail đỏ.
2. Hiện thực `hello.py` cho xanh.
3. `pytest` xanh toàn bộ.

## Giả định
- Format chào cố định `"Hello, {name}!"` (assumption — dev chưa nêu format).
