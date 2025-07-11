import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 📂 파일 불러오기
@st.cache_data
def load_sheet(sheet_name):
    df = pd.read_excel("7회모의고사 7차일반 3학년 과목별 문항 정답률.xlsx", sheet_name=sheet_name)
    df.iloc[:, 1:] = df.iloc[:, 1:].replace('%', '', regex=True).astype(float)
    return df

st.title("📊 7회 모의고사 문항별 정답률 분석")
sheet_names = ['전체', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# 🌐 시트(전체/반) 선택
sheet = st.selectbox("시트를 선택하세요 (전체 or 반 선택)", sheet_names)
df = load_sheet(sheet)

# 📘 과목 선택
subjects = df.columns[1:]
selected_subjects = st.multiselect("과목을 선택하세요 (복수 선택 가능)", subjects, default=list(subjects[:3]))

# 📉 시각화
if selected_subjects:
    fig, ax = plt.subplots(figsize=(12, 6))
    for subject in selected_subjects:
        ax.plot(df['번호'], df[subject], marker='o', label=subject)

    ax.set_title(f"{sheet} 시트 - 선택 과목 문항별 정답률", fontsize=16)
    ax.set_xlabel("문항 번호")
    ax.set_ylabel("정답률 (%)")
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("최소 하나의 과목을 선택해주세요.")
