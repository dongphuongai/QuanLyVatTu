import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Lấy secrets từ streamlit cloud
secrets = st.secrets["gcp_service_account"]

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(secrets, scopes=scopes)

client = gspread.authorize(credentials)

# Mở Google Sheet bằng TÊN (hoặc dùng .open_by_key nếu có ID)
spreadsheet = client.open("QuanLyVatTu")
worksheet = spreadsheet.worksheet("XuatNhapTon")

# Lấy dữ liệu
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.title("📦 Quản lý vật tư")
st.dataframe(df)
