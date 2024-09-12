import streamlit as st
import pandas as pd
import time

if code not in st.session_state:
    st.session_state.code = 0

@st.cache_date
def load_data():
    money = pd.read_excel("金銭リスト.xlsx")
    ivent = pd.read_excel("基本ストーリー")
return pd.concat([money, ivent],ignore_index=True)

words_df = load_data()

name = st.text_area("名前を入力してください")

if st.button("次の日へ"):
    if name not in " ":
        st.sideber.title("性別を選択してください")
        gender = st.sideber.radio("",("男", "女"), horizontal=True)
        st.write("サイドバーから男女を選んでください(月収が変わります)")

        if gender == "男":
            

        if gender == "女":

    else:
        st.write("名前を入力してください")