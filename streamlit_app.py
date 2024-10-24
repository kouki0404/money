import streamlit as st
import pandas as pd
import random
import altair as alt
import numpy as np
from PIL import Image
import os

imga = Image.open('/workspaces/money/food/キャベツ.jpg')
imgb = Image.open('/workspaces/money/food/きゅうり.jpg')
imgc = Image.open('/workspaces/money/food/グリーンピース.jpg')
imgd = Image.open('/workspaces/money/food/ごぼう.jpg')
imge = Image.open('/workspaces/money/food/さば.jpg')
imgf = Image.open('/workspaces/money/food/サラダ油.jpg')
imgh = Image.open('/workspaces/money/food/しいたけ.jpg')
imgi = Image.open('/workspaces/money/food/しめじ.jpg')
imgj = Image.open('/workspaces/money/food/じゃがいも.jpg')
imgk = Image.open('/workspaces/money/food/そば.jpg')
imgl = Image.open('/workspaces/money/food/トマト.jpg')
imgm = Image.open('/workspaces/money/food/ニラ.jpg')
imgn = Image.open('/workspaces/money/food/にんにく.jpg')
imgn = Image.open('/workspaces/money/food/ネギ.jpg')
imgo = Image.open('/workspaces/money/food/パスタ.jpg')
imgp = Image.open('/workspaces/money/food/バター.jpg')
imgq = Image.open('/workspaces/money/food/ピーマン.jpg')
imgr = Image.open('/workspaces/money/food/ブロッコリー.jpg')
imgs = Image.open('/workspaces/money/food/ベーコン.jpg')
imgt = Image.open('/workspaces/money/food/みそ.jpg')
imgu = Image.open('/workspaces/money/food/レタス.jpg')
imgv = Image.open('/workspaces/money/food/塩.jpg')
imgw = Image.open('/workspaces/money/food/海老.jpg')
imgx = Image.open('/workspaces/money/food/牛肉.jpg')
imgy = Image.open('/workspaces/money/food/玉ねぎ.jpg')
imgz = Image.open('/workspaces/money/food/鶏肉.jpg')
imgab = Image.open('/workspaces/money/food/合いびき肉.jpg')
imgac = Image.open('/workspaces/money/food/砂糖.jpg')
imgad = Image.open('/workspaces/money/food/醤油.jpg')
imgae = Image.open('/workspaces/money/food/人参.jpg')
imgaf = Image.open('/workspaces/money/food/生姜.jpg')
imgag = Image.open('/workspaces/money/food/豆腐.jpg')
imgah = Image.open('/workspaces/money/food/豚肉.jpg')
imgai = Image.open('/workspaces/money/food/米.jpg')
imgaj = Image.open('/workspaces/money/food/卵.jpg')
imgak = Image.open('/workspaces/money/food/筍.jpg')

if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-200, 200)
if 'month' not in st.session_state:
    st.session_state.month = random.randint(1, 12)
if 'days' not in st.session_state:
    st.session_state.days = 0
if 'code' not in st.session_state:
    st.session_state.code = 0
if 'xx' not in st.session_state:
    st.session_state.xx = 0
if 'number' not in st.session_state:
    st.session_state.number = 1
if 3 <= st.session_state.month <= 5:
    month_serrect = "3~5"
elif 6 <= st.session_state.month <= 8:
    month_serrect = "6~8"
elif 9 <= st.session_state.month <= 11:
    month_serrect = "9~11"
elif st.session_state.month == 12 or st.session_state.month in (1, 2):
    month_serrect = "12~2"
mens_money = 13000 + st.session_state.energy
mens_total = 270400
womans_total = 208000

totalcount_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
total_days = totalcount_days[st.session_state.month]

@st.cache_data
def load_data():
    main = pd.read_excel("基本ストーリー.xlsx")
    special = pd.read_excel("金銭リスト.xlsx")
    cook = pd.read_excel("栄養・材料の量の内訳")
    return pd.concat([main, special], ignore_index=True)

words_df = load_data()

item_date = ["卵 1パック 300円", "米 5kg 2500円", "大根 1本 200円", "豚肉 100g 200円", "キャベツ 1玉 200円"]
st.sidebar.title("性別を選択してください")
gender = st.sidebar.radio("", ("以下から選択してください", "男", "女"), horizontal=True)
selected_item = st.sidebar.selectbox("基本値段", item_date)

if gender == "以下から選択してください":
    st.write("サイドバーから男女を選んでください(月収が変わります)")
else:
    st.session_state.app_started = True
    st.session_state.finished = False
    st.write(f"{st.session_state.month}月 {st.session_state.days}日")
    filtered_words_df = words_df[(words_df['No.'] >= range_start) & (words_df['No.'] <= range_end)].sort_values(by='No.')
    selected_month = filtered_words_df.sample(month_serrect).reset_index(drop=True)
    all_month = filtered_words_df.sample()
    
    if gender == "男":
        st.session_state.current_total = mens_total - mens_money
    else:
        st.session_state.current_total = womans_total
    st.write(f"初期金額 {st.session_state.current_total} 円 (光熱費が引かれています)")

    if gender == "男":
        choose = st.sidebar.radio("", ("ゲーム画面", "冷蔵庫"), horizontal=True)
        if choose == "ゲーム画面":
            if st.button("次の日へ"): 
                st.session_state.days += 1
                st.session_state.code += 1
                st.session_state.current_total -= 500
            st.write(f"現在の合計金額: {st.session_state.current_total}円")
        elif choose == "冷蔵庫":
            imga.show()
            imgb.show()
            imgc.show()
            imgd.show()
            imge.show()
            imgf.show()
            imgh.show()
            imgi.show()
            imgj.show()
            imgk.show()
            imgl.show()
            imgm.show()
            imgn.show()
            imgo.show()
            imgp.show()
            imgq.show()
            imgr.show()
            imgs.show()
            imgt.show()
            imgu.show()
            imgv.show()
            imgw.show()
            imgx.show()
            imgy.show()
            imgz.show()
            imgab.show()   
            imgac.show()
            imgad.show()
            imgae.show()
            imgaf.show()
            imgag.show()
            imgah.show()
            imgai.show()
            imgaj.show()
            imgak.show()            

    elif gender == "女":
        st.write(f"残金 {womans_total} 円")
