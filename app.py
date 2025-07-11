import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 📌 한글 폰트 설정 함수
def set_korean_font():
    if platform.system() == "Windows":
        plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows 기본
    elif platform.system() == "Darwin":  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    else:  # Linux (Streamlit Cloud 포함)
        plt.rcParams['font.family'] = 'NanumGothic'  # 나눔고딕 설치 필요
    plt.rcParams['axes.unicode_minus'] = False

# 📊 웹 앱 제목
st.set_page_config(page_title="문항별 정답률 시각화", layout="wide")
st.title("📊 모의고사 문항별 정답률 시각화 앱")

# 📁 파일 업로드
uploaded_file = st.file_uploader("📂 Excel 파일(.xlsx)을 업로드하세요", type=["xlsx"])

if uploaded_file:
    try:
        # ✅ 한글 폰트 설정
        set_korean_font()

        # 📄 시트 목록 불러오기
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        
        st.success(f"✅ 파일 업로드 완료. {len(sheet_names)}개의 시트가 확인되었습니다.")

        # 🗂 시트 선택
        selected_sheet = st.selectbox("🗂 시트를 선택하세요", sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

        # 🔢 정답률 퍼센트 → 숫자 변환
        df.iloc[:, 1:] = df.iloc[:, 1:].replace('%', '', regex=True).astype(float)

        # 📘 단일 과목 선택
        subject_list = df.columns[1:]
        selected_subject = st.selectbox("📘 과목을 선택하세요", subject_list)

        # 📈 시각화
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.iloc[:, 0], df[selected_subject], marker='o', color='blue')

        ax.set_title(f"[{selected_sheet}] 문항별 정답률 - {selected_subject}", fontsize=16)
        ax.set_xlabel("문항 번호")
        ax.set_ylabel("정답률 (%)")
        ax.set_ylim(0, 100)
        ax.grid(True)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❗ 오류 발생: {e}")
else:
    st.info("⬆️ 위에 Excel 파일(.xlsx)을 업로드해주세요.")
