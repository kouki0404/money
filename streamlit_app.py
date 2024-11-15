import streamlit as st
import pandas as pd
import numpy as np
import random
from PIL import Image
import sqlite3
import hashlib
import os

# 画像をロードする関数
def load_images():
    images = {
        'beef': Image.open('牛肉.png'),
        'pork': Image.open('豚肉.png'),
        'chicken': Image.open('鶏肉.png'),
        'hamburger': Image.open('合いびき肉.png'),
        'carrot': Image.open('人参.png'),
        'potato': Image.open('じゃがいも.png'),
        'onion': Image.open('玉ねぎ.png'),
        'cabbage': Image.open('キャベツ.png'),
        'lettuce': Image.open('レタス.png'),
        'tomato': Image.open('トマト.png'),
        'cucumber': Image.open('きゅうり.png'),
        'shiitake': Image.open('しいたけ.png'),
        'gobo': Image.open('ごぼう.png'),
        'broccoli': Image.open('ブロッコリー.png'),
        'green_onion': Image.open('ネギ.png'),
        'nira': Image.open('ニラ.png'),
        'garlic': Image.open('にんにく.png'),
        'green_pepper': Image.open('ピーマン.png'),
        'ginger': Image.open('生姜.png'),
        'green_peas': Image.open('グリーンピース.png'),
        'bamboo_shoot': Image.open('筍.png'),
        'salt': Image.open("塩.png"),
        'sugar': Image.open("砂糖.png"),
        'soy_sauce': Image.open("醤油.png"),
        'miso': Image.open("みそ.png"),
        'salad_oil': Image.open("サラダ油.png"),
        'rice': Image.open("米.png"),
        'egg': Image.open("卵.png"),
        'saba': Image.open("さば.png"),
        'soba': Image.open("そば.png"),
        'pasta': Image.open("パスタ.png"),
        'butter': Image.open("バター.png"),
        'bacon': Image.open("ベーコン.png"),
        'shrimp': Image.open("海老.png"),
        'tofu': Image.open("豆腐.png")
    }
    return images

# セッションステートの初期化
if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-700, 700)
if 'month' not in st.session_state:
    st.session_state.month = random.randint(1, 12)
if 'days' not in st.session_state:
    st.session_state.days = 1
if 'code' not in st.session_state:
    st.session_state.code = 0
if 'username' not in st.session_state:
    st.session_state.username = ""

# パスワードをハッシュ化する関数
def make_hashes(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ハッシュ化されたパスワードをチェックする関数
def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def create_user_table(conn):
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS user_data(username TEXT PRIMARY KEY, text_content TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS study_data(username TEXT, date TEXT, study_hours REAL, score INTEGER, subject TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS class_data(username TEXT PRIMARY KEY, class_grade TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS goals(username TEXT PRIMARY KEY, goal TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS projects(username TEXT, project_name TEXT, progress REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS events(username TEXT, date TEXT, description TEXT)')
    conn.commit()

def add_user(conn, username, password):
    hashed_password = make_hashes(password)
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

def check_user_exists(conn, username):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    return c.fetchone() is not None

def login_user(conn, username, password):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    user = c.fetchone()
    if user:
        hashed_password = user[1]
        if check_hashes(password, hashed_password):
            return user  # ログイン成功
    return None  # ユーザー名またはパスワードが間違っている

# メイン関数
def main():
    # データベースに接続
    conn = sqlite3.connect('database.db')
    create_user_table(conn)
    
    menu = ["アカウント作成", "ログイン", "メイン画面"]
    choose = st.sidebar.selectbox("", menu)

    # ログイン処理
    if choose == "ログイン":
        st.subheader("ログイン画面です")
        username = st.sidebar.text_input("ユーザー名を入力してください")
        password = st.sidebar.text_input("パスワードを入力してください", type='password')

        if st.sidebar.button("ログイン"):
            user_info = login_user(conn, username, password)
            if user_info:
                st.session_state['username'] = username  # ログイン時にセッションにユーザー名を保存
                st.success(f"{username}さんでログインしました")
                st.success('メイン画面に移動して下さい')
            else:
                st.warning("ユーザー名またはパスワードが間違っています")

    # アカウント作成
    elif choose == "アカウント作成":
        st.subheader("新しいアカウントを作成します")
        new_user = st.text_input("ユーザー名を入力してください")
        new_password = st.text_input("パスワードを入力してください", type='password')
        gender = st.selectbox("性別を選んでください", ["性別を選択してください", "男", "女"])

        if st.button("サインアップ"):
            if check_user_exists(conn, new_user):
                st.error("このユーザー名は既に使用されています。別のユーザー名を選んでください。")
            else:
                try:
                    add_user(conn, new_user, new_password)
                    st.session_state['username'] = new_user  # ここでセッションにユーザー名を設定
                    st.success("アカウントの作成に成功しました")
                    st.info("ログイン画面からログインしてください")
                except Exception as e:
                    st.error(f"アカウントの作成に失敗しました: {e}")

if __name__ == '__main__':
    main()
