# 🎬 Movie Recommendation System (Hệ thống Gợi ý Phim Netflix-style)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![API](https://img.shields.io/badge/Data-TMDb%20API-green?logo=themoviedatabase)](https://www.themoviedb.org/)

Một ứng dụng gợi ý phim hiện đại mang phong cách giao diện Netflix, sử dụng thuật toán Học máy **Content-Based Filtering** (Lọc dựa trên nội dung) để đề xuất phim chính xác dựa trên sở thích của người dùng. Dự án tích hợp API TMDb để cập nhật hình ảnh, thông tin phim thời gian thực và trực quan hóa dữ liệu qua biểu đồ tương tác.

---

## 📌 Các Tính Năng Nổi Bật (Key Features)

*   **Bộ lọc gợi ý Content-Based Filtering**: Sử dụng kỹ thuật chuyển đổi văn bản `CountVectorizer` và công thức đo lường độ tương đồng `Cosine Similarity` trên các đặc trưng tổng hợp: Thể loại (genres), Tóm tắt (overview), Từ khóa (keywords), Đạo diễn và Diễn viên chính.
*   **Giao diện Netflix-Style Premium**: Tối ưu hóa giao diện Streamlit với Dark Mode sang trọng, các thẻ phim (movie cards) responsive, bo góc, hiệu ứng hover mượt mà và thanh tìm kiếm tự động gợi ý tên phim.
*   **Tích hợp Real-time TMDb API**: Tự động tải ảnh poster phim chất lượng cao, điểm đánh giá và mô tả phim từ cơ sở dữ liệu điện ảnh TMDb lớn nhất thế giới.
*   **Kiến trúc Đa trang (Multi-page)**:
    *   **Home**: Trang tìm kiếm phim chính, nhận gợi ý tương tự và hiển thị trailer.
    *   **Trending**: Danh sách phim đang thịnh hành theo ngày/tuần.
    *   **Top Rated**: Phim được chấm điểm cao nhất mọi thời đại.
    *   **Analytics**: Báo cáo thống kê, trực quan hóa xu hướng điện ảnh thông qua biểu đồ trực quan (Plotly).
    *   **Browse by Genre**: Khám phá phim theo thể loại yêu thích.
    *   **Watchlist**: Danh sách lưu trữ các phim muốn xem cá nhân.

---

## 🏗️ Kiến Trúc Hệ Thống (Architecture)

```text
HeThongGoiYPhim/
├── data/                  # Thư mục chứa dữ liệu CSV gốc (TMDb 5000)
├── models/                # Lưu trữ các file model đã huấn luyện (.pkl)
├── api/                   # Mã nguồn gọi API tương tác với TMDb
│   └── tmdb_client.py
├── src/                   # Logic xử lý thuật toán học máy
│   ├── data_preprocessing.py # Tiền xử lý dữ liệu và xuất model
│   └── recommendation_engine.py # Engine tính toán Cosine Similarity
├── pages/                 # Danh sách các trang tính năng của Streamlit
│   ├── 1_Trending.py
│   ├── 2_Top_Rated.py
│   ├── 3_Analytics.py
│   ├── 4_Browse_by_Genre.py
│   └── 5_Watchlist.py
├── assets/                # Chứa file CSS tùy biến giao diện
│   └── style.css
├── app.py                 # File chạy ứng dụng chính (Trang Home)
├── Dockerfile             # Cấu hình container hóa ứng dụng
├── requirements.txt       # Danh sách thư viện phụ thuộc
├── .env.example           # File cấu hình biến môi trường mẫu
└── README.md              # Tài liệu hướng dẫn sử dụng
```

---

## 🛠️ Hướng Dẫn Cài Đặt Và Chạy Cục Bộ (Setup & Installation)

Dành cho Nhà tuyển dụng hoặc Lập trình viên muốn tải dự án về chạy thử trên môi trường cục bộ:

### 1. Chuẩn bị môi trường (Prerequisites)
*   Yêu cầu máy tính cài đặt sẵn **Python 3.10** trở lên.
*   Một tài khoản và API Key từ hệ thống TMDb (Đăng ký miễn phí tại [https://www.themoviedb.org/](https://www.themoviedb.org/) -> Settings -> API).

### 2. Tải mã nguồn về máy
```bash
git clone https://github.com/LeQuocNam2004/HeThongGoiYPhim.git
cd HeThongGoiYPhim
```

### 3. Thiết lập Môi trường ảo & Cài đặt thư viện
Nên sử dụng môi trường ảo của Python (`venv`) để tránh xung đột thư viện:
```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
# Trên Windows (Command Prompt):
.venv\Scripts\activate
# Trên Windows (PowerShell):
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; .venv\Scripts\Activate.ps1
# Trên macOS/Linux:
source .venv/bin/activate

# Cài đặt toàn bộ các thư viện cần thiết
pip install -r requirements.txt
```

### 4. Cấu hình khóa API TMDb
1. Tạo một tệp tên là `.env` ở thư mục gốc của dự án (hoặc đổi tên file `.env.example` thành `.env`).
2. Mở file `.env` bằng trình chỉnh sửa code và điền mã TMDb API Key của bạn vào:
   ```env
   TMDB_API_KEY=mã_api_key_tmd_của_bạn_ở_đây
   ```

### 5. Tải dữ liệu và Huấn luyện mô hình (Data & Model Training)
Để tối ưu dung lượng Git, các file dữ liệu gốc và model tính toán tương tự dung lượng lớn (184MB) đã được lược bỏ khỏi Git. Bạn chỉ cần thực hiện 2 bước đơn giản sau để tự tạo tự động:
1. Tải bộ dữ liệu **TMDb 5000 Movie Dataset** từ Kaggle: [Tải tại đây](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv).
2. Giải nén và copy 2 file `tmdb_5000_movies.csv` và `tmdb_5000_credits.csv` vào thư mục `data/` trong thư mục dự án.
3. Chạy script xử lý dữ liệu và tạo ma trận tương đồng (mất khoảng 15-30 giây):
   ```bash
   python src/data_preprocessing.py
   ```
   *Script sẽ tự động làm sạch dữ liệu, xử lý chuỗi văn bản đặc trưng và xuất ra các mô hình nhị phân `.pkl` bên trong thư mục `models/`.*

### 6. Khởi chạy ứng dụng Web
Chạy lệnh khởi động Streamlit:
```bash
streamlit run app.py
```
Hệ thống sẽ tự động khởi động và mở trang web trên trình duyệt mặc định của bạn tại địa chỉ: `http://localhost:8501`.

---

## 🐳 Triển Khai Bằng Docker (Optional)

Nếu máy bạn đã cài sẵn Docker, bạn có thể khởi chạy dự án cực nhanh không cần cài đặt Python thủ công:
```bash
# Xây dựng Docker Image
docker build -t movie-recommender .

# Chạy Docker Container bằng cách truyền file cấu hình biến môi trường
docker run -p 8501:8501 --env-file .env movie-recommender
```
Sau đó truy cập ứng dụng tại `http://localhost:8501`.

---

## 👤 Tác Giả (Author)
*   **Lê Quốc Nam** (LeQuocNam2004) - *Phát triển Thuật toán gợi ý & Thiết kế giao diện đa trang Netflix-style.*
*   GitHub: [@LeQuocNam2004](https://github.com/LeQuocNam2004)
*   Email: [lequocnam0704537690@gmail.com](mailto:lequocnam0704537690@gmail.com)
