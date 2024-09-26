import streamlit as st
import pandas as pd
import random

if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-200,200)
if 'xx' not in st.session_state:
    st.session_state.xx = 0
mens_money = 13000 + st.session_state.energy #光熱費
mens_total = 270400 #男の平均月給
womans_total = 208000 #女の平均月給

if 'month' not in st.session_state:
    st.session_state.month = random.randint(1,12)
if 'days' not in st.session_state:
    st.session_state.days = 1
if 'code' not in st.session_state:
    st.session_state.code = 0
st.sidebar.title("性別を選択してください")
gender = st.sidebar.radio("",("男", "女"), horizontal=True)
word = "サイドバーから男女を選んでください(月収が変わります)"
st.write(word)


st.write(str(st.session_state.month) + "月" + str(st.session_state.days) + "日")
if gender == "男":
    st.session_state.creck += 1
    st.write("残金 " + str(mens_total) + "円")
    if st.button("次の日へ"):
        st.session_state.creck += 1
        st.session_state.days += 1
        word = "a" #この部分もexcelで出力
        st.write(word)
        words = ["牛肉200g 500円","豚肉300g 450円"]
        key = st.selectbox("何を買う？",words)
        if key == "牛肉200g 500円":
            mens_total -= 500
            st.session_state.xx += 1
            if st.session_state.month == 1:
    if st.session_state.days == 31:
        st.write("finish!!")
elif st.session_state.month == 3:
    if st.session_state.days == 31:
        st.write("finish!!")
elif st.session_state.days == 5:
    if st.session_state.days == 31:
        st.write("finish!!")
elif st.session_state.days == 7:
    if st.session_state.days == 31:
        st.write("finish!!")
elif st.session_state.days == 8:
    if st.session_state.days == 31:
        st.write("finish!!")
elif st.session_state.days == 10:
    if st.session_state.days == 31:
        st.write("finish!!")
elif st.session_state.days == 12:
    if st.session_state.days == 31:
        st.write("finish!!")
            
elif gender == "女":
    st.write("残金 " + str(womans_total) + "円")
