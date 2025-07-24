import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

# Thiết lập quyền truy cập Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Mở Google Sheet
sheet = client.open_by_key("YOUR_GOOGLE_SHEET_ID").sheet1

st.title("📦 Quản lý vật tư - Xuất Nhập Tồn")

uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Tính tồn
    df["Tồn"] = df["Nhập"] - df["Xuất"]

    st.subheader("📄 Dữ liệu tính toán:")
    st.dataframe(df)

    # Ghi lên Google Sheet
    set_with_dataframe(sheet, df)
    st.success("✅ Dữ liệu đã được ghi vào Google Sheets!")
