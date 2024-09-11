import streamlit as st
import html

if code not in st.session_state:
    st.session_state.code = 0

name = st.text_area("名前を入力してください")

st.html(
    <a href="https://google.com">google</a>
    #ルール
    <a href="https://google.com">google</a>
    #ランキング
)

if name not in "":
    st.sideber.title("性別を選択してください")
    gender = st.sideber.radio("",("男", "女"), horizontal=True)
    st.write("サイドバーから男女を選んでください(月収が変わります)")

    if gender == "男":


    if gender == "女":