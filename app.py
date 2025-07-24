import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Quản lý vật tư", layout="wide")
st.title("📦 Quản lý Xuất Nhập Tồn Vật Tư")

# === Thiết lập Google Sheets ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
client = gspread.authorize(creds)

sheet_id = "1QNOHfJw3kRAC5BSfb0YsEfYzhWDYdEFi0L4Rk1t141A"
sheet_tab = "XuatNhapTon"

try:
    worksheet = client.open_by_key(sheet_id).worksheet(sheet_tab)
    sheet_data = worksheet.get_all_records()
    df_sheet = pd.DataFrame(sheet_data)
    st.subheader("📊 Dữ liệu hiện tại từ Google Sheet:")
    st.dataframe(df_sheet)
except Exception as e:
    st.warning("Không thể đọc dữ liệu từ Google Sheet.")
    st.exception(e)

# === Upload file Excel ===
st.markdown("---")
uploaded_file = st.file_uploader("📤 Nhập file Excel cập nhật", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df_upload = pd.read_excel(uploaded_file)

        # Tính toán tồn cuối nếu có cột phù hợp
        if {"Tồn đầu vào", "Nhập", "Xuất"}.issubset(df_upload.columns):
            df_upload["Tồn cuối"] = df_upload["Tồn đầu vào"] + df_upload["Nhập"] - df_upload["Xuất"]

        st.success("✅ Đã đọc dữ liệu từ file:")
        st.dataframe(df_upload)

        if st.button("📤 Gửi dữ liệu lên Google Sheet"):
            worksheet.clear()
            worksheet.update([df_upload.columns.tolist()] + df_upload.values.tolist())
            st.success("🎉 Đã cập nhật Google Sheet thành công!")

    except Exception as e:
        st.error("❌ Lỗi khi xử lý file.")
        st.exception(e)
