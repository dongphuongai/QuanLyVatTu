import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Kết nối GSheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)

# ID Sheet & tên sheet
SHEET_ID = "1QNOHfJw3kRAC5BSfb0YsEfYzhWDYdEFi0L4Rk1t141A"  # <-- thay bằng sheet thật
SHEET_NAME = "XuatNhapTon"

try:
    worksheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    st.success("✅ Kết nối thành công!")
    st.write(worksheet.get_all_records())
except Exception as e:
    st.error("❌ Không thể kết nối Google Sheet.")
    st.exception(e)
