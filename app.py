import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scopes
)
client = gspread.authorize(credentials)

# Ví dụ đọc dữ liệu
sheet_id = "1QNOHfJw3kRAC5BSfb0YsEfYzhWDYdEFi0L4Rk1t141A"
worksheet = client.open_by_key(sheet_id).worksheet("XuatNhapTon")
data = worksheet.get_all_records()

st.title("📦 Quản lý Xuất Nhập Tồn Vật Tư")
st.write(data)
