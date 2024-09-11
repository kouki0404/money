import streamlit as st

if code not in st.session_state:
    st.session_state.code = 0

name = st.text_area("名前を入力してください")

if st.button("次へ"):
    if name not in " ":
        st.sideber.title("性別を選択してください")
        gender = st.sideber.radio("",("男", "女"), horizontal=True)
        st.write("サイドバーから男女を選んでください(月収が変わります)")

        if gender == "男":


        if gender == "女":

    else:
        st.write("名前を入力してください")