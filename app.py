import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Cấu hình quyền truy cập Google Sheet
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Lấy thông tin từ secrets
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["service_account"], scope
)

# Kết nối đến Google Sheet
client = gspread.authorize(creds)

# Mở file Google Sheet và một sheet cụ thể
sheet = client.open("1QNOHfJw3kRAC5BSfb0YsEfYzhWDYdEFi0L4Rk1t141A").worksheet("XuatNhapTon")

# Lấy toàn bộ dữ liệu
data = sheet.get_all_records()

# Hiển thị dữ liệu trên giao diện web
st.title("Dữ liệu từ Google Sheet")
st.write(data)
