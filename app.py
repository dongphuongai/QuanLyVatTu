import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Lấy thông tin từ streamlit.secrets (tự động được cung cấp trên Streamlit Cloud)
secrets = st.secrets["gcp_service_account"]

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(secrets, scopes=scopes)

gc = gspread.authorize(credentials)
sh = gc.open("QuanLyVatTu")  # đổi tên cho phù hợp
worksheet = sh.XuatNhapTon
