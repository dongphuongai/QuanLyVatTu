import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import toml

# Load credentials from .toml file
secrets = toml.load(".streamlit/secrets.toml")["gcp_service_account"]

# Set up credentials
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(secrets, scopes=scopes)

# Connect to Google Sheets
try:
    gc = gspread.authorize(credentials)
    sh = gc.open("QuanLyVatTu")  # ⚠️ Thay bằng tên thực tế
    worksheet = sh.XuatNhapTon
except Exception as e:
    st.error("❌ Không thể kết nối Google Sheet.")
    st.stop()

# Streamlit App UI
st.title("📦 Quản Lý Vật Tư")
uploaded_file = st.file_uploader("📥 Tải lên file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("✅ Dữ liệu vừa tải lên:")
    st.dataframe(df)

    if st.button("📤 Gửi dữ liệu lên Google Sheet"):
        worksheet.clear()  # Xóa dữ liệu cũ
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        st.success("✅ Đã gửi dữ liệu lên Google Sheet thành công!")
