# Sử dụng một hình ảnh gốc Python
FROM python:3.10
# Đặt thư mục làm việc trong container
WORKDIR /app
# Sao chép tệp requirements.txt vào container
COPY requirements.txt .
# Cài đặt các gói phụ thuộc từ tệp requirements.txt
RUN pip install -r requirements.txt
# Sao chép tất cả các tệp trong dự án vào container
COPY . .
# Chạy lệnh migrate để tạo cơ sở dữ liệu SQLite3 và thực hiện các cập nhật
WORKDIR /app/ecom
RUN python manage.py migrate
# Expose cổng 8000 (hoặc bất kỳ cổng nào bạn đang sử dụng cho dự án Django)
EXPOSE 8000
# Chạy lệnh start server của Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]