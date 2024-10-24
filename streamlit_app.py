import streamlit as st
import pandas as pd
import random
import altair as alt
import numpy as np
from PIL import Image
import os

# 画像ファイル名のリスト
image_file_meat = [
    '牛肉.jpg',
    '豚肉.jpg',
    '鶏肉.jpg',
    '合いびき肉.jpg'
]
image_file_yasai = [
    'キャベツ.jpg',
    'きゅうり.jpg',
    'グリーンピース.jpg',
    'ごぼう.jpg',
    'しいたけ.jpg',
    'しめじ.jpg',
    'じゃがいも.jpg',
    'トマト.jpg',
    'ニラ.jpg',
    'にんにく.jpg',
    'ネギ.jpg',
    'ピーマン.jpg',
    'ブロッコリー.jpg',
    'レタス.jpg',
    '玉ねぎ.jpg',
    '人参.jpg',
    '生姜.jpg',
    '筍.jpg'
]
image_files = [
    '米.jpg',
    '卵.jpg',
    'さば.jpg',
    'そば.jpg',
    'パスタ.jpg',
    'バター.jpg',
    'ベーコン.jpg',
    '海老.jpg',
    '豆腐.jpg'
]
image_file_choumiryou = [
    '塩.jpg',
    '砂糖.jpg',
    '醤油.jpg',
    'みそ.jpg',
    'サラダ油.jpg'
]

# 画像を格納する辞書
images = {}

# 画像を読み込む
def load_images(image_list):
    images = {}
    for image_file in image_list:
        image_path = os.path.join('/workspaces/money/food/', image_file)
        try:
            img = Image.open(image_path)
            images[image_file] = img
        except FileNotFoundError:
            st.error(f"Error: {image_file} not found.")
    return images

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
        choose = st.sidebar.radio("", ("ゲーム画面", "肉類", "野菜", "調味料", "その他"), horizontal=True)
        if choose == "ゲーム画面":
            if st.button("次の日へ"): 
                st.session_state.days += 1
                st.session_state.code += 1
                st.session_state.current_total -= 500
            st.write(f"現在の合計金額: {st.session_state.current_total}円")
        if choose == "肉類":
    for imgA in images_meat.values():
        st.image(imgA, caption=os.path.basename(imgA.filename), use_column_width=True)
elif choose == "野菜":
    for imgB in images_yasai.values():
        st.image(imgB, caption=os.path.basename(imgB.filename), use_column_width=True)
elif choose == "調味料":
    for imgC in images_choumiryou.values():
        st.image(imgC, caption=os.path.basename(imgC.filename), use_column_width=True)
elif choose == "その他":
    for img in images_other.values():
        st.image(img, caption=os.path.basename(img.filename), use_column_width=True)
    elif gender == "女":
        st.write(f"残金 {womans_total} 円")
