import streamlit as st
import pandas as pd
import random

if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-200, 200)
if 'month' not in st.session_state:
    st.session_state.month = random.randint(1, 12)
if 'days' not in st.session_state:
    st.session_state.days = 1
if 'code' not in st.session_state:
    st.session_state.code = 0
if 'xx' not in st.session_state:
    st.session_state.xx = 0

mens_money = 13000 + st.session_state.energy
mens_total = 270400
womans_total = 208000

totalcount_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
total_days = totalcount_days[st.session_state.month]

@st.cache_data
def load_data():
    main = pd.read_excel("基本ストーリー.xlsx")
    special = pd.read_excel("金銭リスト.xlsx")
    return pd.concat([main, special], ignore_index=True)

words_df = load_data()

item_date = ["卵 1パック 300円", "米 5kg 2500円", "大根 1本 200円", "豚肉 100g 200円", "キャベツ 1玉 200円"]
st.sidebar.title("性別を選択してください")
gender = st.sidebar.radio("", ("以下から選択してください", "男", "女"), horizontal=True)

if gender == "以下から選択してください":
    st.write("サイドバーから男女を選んでください(月収が変わります)")
else:
    st.session_state.app_started = True
    st.session_state.finished = False
    st.write(f"{st.session_state.month}月 {st.session_state.days}日")

    if gender == "男":
        current_total = mens_total - mens_money
    else:
        current_total = womans_total

    st.write(f"初期金額 {current_total} 円 (光熱費が引かれています)")

    selected_item = st.sidebar.selectbox("基本値段", item_date)

    if gender == "男":
        if st.button("次の日へ"):
            words = [" ", "牛肉200g 500円", "豚肉300g 450円"]
            key = st.selectbox("何を買う？", words)
            if key == "牛肉200g 500円":
                current_total -= 500
                st.session_state.xx += 1
                st.write(f"残金 {current_total} 円")
            st.experimental_rerun()

    elif gender == "女":
        st.write(f"残金 {womans_total} 円")
