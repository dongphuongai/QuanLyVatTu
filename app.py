import streamlit as st
import pandas as pd
import openai

# === Cấu hình OpenAI ===
openai.api_key = "YOUR_API_KEY"  # 🔑 Thay bằng API key của bạn

st.set_page_config(page_title="Quản lý kho vật tư", layout="wide")
st.title("📦 Ứng dụng quản lý kho vật tư bằng AI")

# === Upload file Excel ===
uploaded_file = st.file_uploader("📁 Tải lên file Excel chứa dữ liệu nhập/xuất kho", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📄 Dữ liệu gốc")
    st.dataframe(df)

    # Xử lý tồn kho
    try:
        df["Số lượng"] = df["Số lượng"].astype(int)
        df["Loại giao dịch"] = df["Loại giao dịch"].str.lower()

        pivot = df.pivot_table(index=["Mã VT", "Tên VT"],
                               columns="Loại giao dịch",
                               values="Số lượng",
                               aggfunc="sum",
                               fill_value=0)

        pivot["Tồn kho"] = pivot.get("nhập", 0) - pivot.get("xuất", 0)
        pivot["Cảnh báo"] = ""
        pivot.loc[pivot["Tồn kho"] < 0, "Cảnh báo"] = "Âm tồn kho"
        pivot.loc[(pivot.get("xuất", 0) > 0) & (pivot.get("nhập", 0) == 0), "Cảnh báo"] = "Xuất nhưng chưa từng nhập"

        result = pivot.reset_index()

        st.subheader("📊 Kết quả tồn kho")
        st.dataframe(result)

        # Sinh báo cáo AI
        if st.button("🧠 Sinh báo cáo bằng AI"):
            with st.spinner("Đang phân tích bằng GPT..."):
                content = result.to_string(index=False)

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Bạn là trợ lý quản lý kho, viết báo cáo bằng tiếng Việt."},
                        {"role": "user", "content": f"Dữ liệu tồn kho:\n{content}\n\nHãy viết báo cáo ngắn nêu các vấn đề tồn kho hoặc cảnh báo."}
                    ]
                )

                report = response["choices"][0]["message"]["content"]
                st.subheader("📋 Báo cáo AI")
                st.markdown(report)

    except Exception as e:
        st.error(f"Lỗi xử lý file: {e}")
else:
    st.info("Vui lòng tải lên file Excel để bắt đầu.")
