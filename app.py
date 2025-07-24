iimport gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# Kết nối Google Sheet
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
    client = gspread.authorize(creds)

    sheet_id = "1QNOHfJw3kRAC5BSfb0YsEfYzhWDYdEFi0L4Rk1t141A"
    sheet_tab = "XuatNhapTon"

    worksheet = client.open_by_key(sheet_id).worksheet(sheet_tab)
except Exception as e:
    st.error("❌ Không thể kết nối Google Sheet.")
    st.stop()

# Xóa dữ liệu (nếu bạn cần)
try:
    worksheet.clear()
    st.success("✅ Đã xóa dữ liệu.")
except Exception as e:
    st.error(f"Không thể xóa: {e}")


