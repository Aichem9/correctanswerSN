import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="문항별 정답률 시각화", layout="wide")

st.title("📊 모의고사 문항별 정답률 시각화 앱")

# 1. 파일 업로드
uploaded_file = st.file_uploader("📂 Excel 파일(.xlsx)을 업로드하세요", type=["xlsx"])

if uploaded_file:
    try:
        # 2. 시트 목록 자동 로딩
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        
        st.success(f"✅ 파일 업로드 완료. 총 {len(sheet_names)}개의 시트 발견됨.")

        # 3. 시트 선택
        selected_sheet = st.selectbox("🗂 시트를 선택하세요", sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

        # 4. 정답률(%) → 숫자로 변환
        df.iloc[:, 1:] = df.iloc[:, 1:].replace('%', '', regex=True).astype(float)

        # 5. 과목 선택
        subject_list = df.columns[1:]
        selected_subjects = st.multiselect("📘 시각화할 과목을 선택하세요", subject_list, default=list(subject_list[:3]))

        # 6. 그래프 출력
        if selected_subjects:
            fig, ax = plt.subplots(figsize=(12, 6))
            for subj in selected_subjects:
                ax.plot(df.iloc[:, 0], df[subj], marker='o', label=subj)

            ax.set_title(f"[{selected_sheet}] 문항별 정답률", fontsize=16)
            ax.set_xlabel("문항 번호")
            ax.set_ylabel("정답률 (%)")
            ax.set_ylim(0, 100)
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("❗ 최소 한 개의 과목을 선택해주세요.")
    except Exception as e:
        st.error(f"⚠️ 오류 발생: {e}")
else:
    st.info("⬆️ 상단에 Excel 파일을 업로드해주세요.")
