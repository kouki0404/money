import streamlit as st
import pandas as pd
import random
from PIL import Image
import os
import altair as alt
import numpy as np

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
image_file_choumiryou = [
    '塩.jpg',
    '砂糖.jpg',
    '醤油.jpg',
    'みそ.jpg',
    'サラダ油.jpg'
]
image_files_other = [
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

# 画像を読み込む関数
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

# 画像をロード
images_meat = load_images(image_file_meat)
images_yasai = load_images(image_file_yasai)
images_choumiryou = load_images(image_file_choumiryou)
images_other = load_images(image_files_other)

def load_images(image_list):
    images = {}
    for image_file in image_list:
        image_path = os.path.join('/workspaces/money/food/', image_file)
        print(f"Trying to load: {image_path}")  # 追加したデバッグメッセージ
        try:
            img = Image.open(image_path)
            images[image_file] = img
        except FileNotFoundError:
            st.error(f"Error: {image_file} not found at {image_path}.")
    return images

# セッションステートの初期化
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

# 性別選択
st.sidebar.title("性別を選択してください")
gender = st.sidebar.radio("", ("以下から選択してください", "男", "女"), horizontal=True)

# ゲームの進行
if gender == "以下から選択してください":
    st.write("サイドバーから男女を選んでください(月収が変わります)")
else:
    st.session_state.app_started = True
    st.session_state.finished = False
    st.write(f"{st.session_state.month}月 {st.session_state.days}日")

    if gender == "男":
        mens_total = 270400
        mens_money = 13000 + st.session_state.energy
        st.session_state.current_total = mens_total - mens_money
    else:
        womens_total = 208000
        st.session_state.current_total = womens_total

    st.write(f"初期金額 {st.session_state.current_total} 円 (光熱費が引かれています)")

    choose = st.sidebar.radio("", ("ゲーム画面", "肉類", "野菜", "調味料", "その他"), horizontal=True)

    if choose == "ゲーム画面":
        if st.button("次の日へ"): 
            st.session_state.days += 1
            st.session_state.code += 1
            st.session_state.current_total -= 500
        st.write(f"現在の合計金額: {st.session_state.current_total}円")

    elif choose == "肉類":
        for img in images_meat.values():
            st.image(img, caption=os.path.basename(img.filename), use_column_width=True)
    elif choose == "野菜":
        for img in images_yasai.values():
            st.image(img, caption=os.path.basename(img.filename), use_column_width=True)
    elif choose == "調味料":
        for img in images_choumiryou.values():
            st.image(img, caption=os.path.basename(img.filename), use_column_width=True)
    elif choose == "その他":
        for img in images_other.values():
            st.image(img, caption=os.path.basename(img.filename), use_column_width=True)

    if gender == "女":
        st.write(f"残金 {womens_total} 円")
