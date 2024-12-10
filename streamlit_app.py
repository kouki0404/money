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
if 'days_zone' not in st.session_state:
    st.session_state.days_zone = 0
if 'total_money' not in st.session_state:
    st.session_state.total_money = 100000
if 'total_niku' not in st.session_state:
    st.session_state.total_niku = 0
# 曜日設定
youbi_list = ["月", "火", "水", "木", "金", "土", "日"]
youbi = youbi_list[st.session_state.days % 7]
total_days = 7

# 月に応じた条件設定
month_serrect = ""
if 3 <= st.session_state.month <= 5:
    month_serrect = "3~5"
elif 6 <= st.session_state.month <= 8:
    month_serrect = "6~8"
elif 9 <= st.session_state.month <= 11:
    month_serrect = "9~11"
elif st.session_state.month == 12 or st.session_state.month in (1, 2):
    month_serrect = "12~2"

# パスワードをハッシュ化する関数
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

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
    try:
        # パスワードをハッシュ化
        hashed_password = make_hashes(password)

        # カーソルを作成
        c = conn.cursor()
        
        # ユーザーを追加するSQL文
        c.execute('INSERT INTO userstable(username, password) VALUES (?, ?, ?)', 
                  (username, hashed_password))
        
        # コミットして変更を保存
        conn.commit()
        
        # 成功した場合にTrueを返す
        return True
    except sqlite3.IntegrityError as e:
        # ユーザー名が重複している場合など、IntegrityErrorをキャッチ
        st.error(f"エラーが発生しました: {e}")
        return False
    except Exception as e:
        # 他のエラーに対応するための一般的な例外処理
        st.error(f"予期しないエラーが発生しました: {e}")
        return False

def check_user_exists(conn, username):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    return c.fetchone() is not None

def login_user(conn, username, password):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    user = c.fetchone()
    if user and check_hashes(password, user[1]):
        return user
    return None

@st.cache_data
def load_data():
    # Excelファイルを読み込む
    df = pd.read_excel("Nextday.xlsx", header=0)
    df.columns = df.columns.astype(str).str.strip()
    return df
# データを読み込む
words_df = load_data()
print("Columns in words_df:", words_df.columns)

# 読み込まれた列数が予想通りか確認
expected_columns = ['No.', '材料', '料理名', '値段', 'タンパク質', '脂質', '炭水化物', '無機質', 'ビタミン']
if len(words_df.columns) != len(expected_columns):
    st.error(f"Expected {len(expected_columns)} columns, but found {len(words_df.columns)} columns.")
else:
    # 列名が一致した場合、列名を設定
    words_df.columns = expected_columns
dish_start = 1
dish_end = 252
# "No."列が dish_start から dish_end の範囲に含まれるデータをフィルタリングし、"No."列でソート
filtered_words_df = words_df[(words_df['No.'] >= dish_start) & (words_df['No.'] <= dish_end)].sort_values(by='No.')
print("Columns in words_df:", words_df.columns)
# メイン関数

def main():
    # データベースに接続
    conn = sqlite3.connect('database.db')
    create_user_table(conn)
    menu = ["アカウント作成", "ログイン", "メイン画面"]
    choose = st.sidebar.selectbox("", menu)

    # アカウント作成
    if choose == "アカウント作成":
        st.subheader("新しいアカウントを作成します")
        new_user = st.text_input("ユーザー名を入力してください")
        new_password = st.text_input("パスワードを入力してください", type='password')

        if st.button("サインアップ"):
            if check_user_exists(conn, new_user):
                st.error("このユーザー名は既に使用されています。別のユーザー名を選んでください。")
            else:
                # ユーザー名、ハッシュ化されたパスワード、性別をデータベースに保存
                if add_user(conn, new_user, new_password):
                    st.session_state['username'] = new_user  # セッションにユーザー名を設定
                    st.success("アカウントの作成に成功しました")
                    st.info("ログイン画面からログインしてください")
                else:
                    st.error("アカウント作成に失敗しました。")

    # ログイン処理
    elif choose == "ログイン":
        st.subheader("ログイン画面")
        username = st.sidebar.text_input("ユーザー名を入力してください")
        password = st.sidebar.text_input("パスワードを入力してください", type='password')

        if st.sidebar.button("ログイン"):
            user_info = login_user(conn, username, password)
            if user_info:
                st.session_state['username'] = username  # ログイン時にセッションにユーザー名を保存
                st.success(f"{username}さんでログインしました")
                st.success('メイン画面に移動して下さい')
            else:
                st.warning("ユーザー名かパスワードが間違っています")
            
            if username == "sky_kk":
                st.success("昊")
 
                if st.button("すべてのユーザーのデータを削除"):
                    if delete_all_users(conn):
                        st.success("すべてのユーザーのデータが削除されました。")
                    else:
                        st.error("データの削除に失敗しました。")
    if 'username' in st.session_state and st.session_state.username:
        username = st.session_state['username']
        foods = ["ホーム", "肉類", "野菜", "調味料", "その他"]
        reizouko = st.sidebar.selectbox("冷蔵庫", foods)
        item_date = ["牛肉 100g 900円", "豚肉 100g 200円", "鶏肉 100g 150円", "卵 1パック 200円", "米 5kg 2500円", "大根 1本 200円", "キャベツ 1玉 300円", "みそ 1パック 300円", "合いびき肉 100g 200円"]


        selected_item = st.sidebar.selectbox("基本値段", item_date)
        if choose == "メイン画面" and reizouko == "ホーム":
            st.session_state.update({
                'test_started': True,
                'correct_dish': 0,
                'current_dish': 0,
                'finished': False,
                'wrong_answers': [],
            })
            times = ["朝","昼","夜"]
            days_total = st.session_state.days//3 + 1
            st.write(f"{st.session_state.month}月 {days_total}日 {youbi}曜日{times[st.session_state.days_zone]}")
            st.write(f"残金: {st.session_state.total_money} 円")  # 修正: remaining_balance を直接mens_totalとして表示
            selected_dishes = filtered_words_df.sample(4).reset_index(drop=True)
            st.session_state.update({
                'selected_dishes': selected_dishes,
                'total_dishes': len(selected_dishes),
                'current_dish_data': selected_dishes.iloc[0],
            })
            options = list(st.session_state.current_dish_data['材料'])

            np.random.shuffle(options)
            st.session_state.options = options
            st.session_state.dish = None
            def update_dish(dish):
                correct_dish = st.session_state.current_dish_data['料理名']
                dish_value = st.session_state.current_dish_data['値段']

                st.session_state.current_dish += 1
                if st.session_state.current_dish < 9:
                    st.session_state.current_question_data = st.session_state.selected_questions.iloc[st.session_state.current_question]
                    options = list(st.session_state.selected_dishes['料理名'].sample(3))
                    options.append(st.session_state.current_question_data['料理名'])
                    np.random.shuffle(options)
                    st.session_state.options = options
                    st.session_state.answer = None
                else:
                    st.session_state.finished = True
            if 'test_started' in st.session_state and not st.session_state.finished:
                st.subheader(f"料理")
                st.subheader(f"{st.session_state.current_dish_data['料理名']}")
                st.markdown('<div class="choices-container">', unsafe_allow_html=True)
                if 'selected_dish' not in st.session_state:
                    st.session_state.selected_dish = None
                if 'selected_ingredients' not in st.session_state:
                    st.session_state.selected_ingredients = []

                if st.session_state.selected_dish is None:
                    st.subheader("料理を選んでください")
                
                    for idx, dish in enumerate(st.session_state.selected_dishes['料理名']):
                        if st.button(dish, key=f"dish_{idx}"):
                            # 料理名を選んだ時にその料理の材料を設定
                            st.session_state.selected_dish = dish
                            # 選ばれた料理の材料をsession_stateに保存
                            st.session_state.selected_ingredients = st.session_state.selected_dishes[st.session_state.selected_dishes['料理名'] == dish]['材料'].values[0]
                            st.experimental_rerun()  # ページを再読み込みして、材料ボタンを表示する
                
                # 料理を選んだ後に材料のボタンを表示
                if st.session_state.selected_dish is not None:
                    st.subheader(f"{st.session_state.selected_dish} の材料を選んでください")
                    
                    for idx, ingredient in enumerate(st.session_state.selected_ingredients):
                        if st.button(ingredient, key=f"ingredient_{idx}"):
                            st.write(f"選んだ材料: {ingredient}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if 'test_started' in st.session_state and st.session_state.finished:
                    display_results()    
            if st.button("決定"):
                st.session_state.days += 1
                st.session_state.days_zone += 1
                if st.session_state.days_zone == 2:
                    st.session_state.days_zone = 0
        # 冷蔵庫のアイテム選択
        images = load_images()
        if reizouko == "肉類":
            st.image(images['beef'])
            niku = st.number_input("購入する量 100g900円", min_value=100, max_value=1000, step=100)
            if st.button("購入する"):
                st.session_state.total_niku += niku
                st.session_state.total_money -= (900 // 100) * niku
            st.write(f"現在{st.session_state.total_niku}g")
            st.image(images['pork'])
            buta = st.number_input("購入する量 100g300円", min_value=100, max_value=1000, step=100)
            if st.button("購入する"):
                st.session_state.total_buta += buta
                st.session_state.total_money -= (300 // 100) * buta
            st.write(f"現在{st.session_state.total_buta}g")
            st.image(images['chicken'])
            tori = st.number_input("購入する量 100g200円", min_value=100, max_value=1000, step=100)
            if st.button("購入する"):
                st.session_state.total_tori += tori
                st.session_state.total_money -= (200 // 100) * tori
            st.write(f"現在{st.session_state.total_tori}g")
            st.image(images['hamburger'])
            aibiki = st.number_input("購入する量 100g200円", min_value=100, max_value=1000, step=100)
            if st.button("購入する"):
                st.session_state.total_aibiki += aibiki
                st.session_state.total_money -= (300 // 100) * aibiki
            st.write(f"現在{st.session_state.total_aibiki}g")
        elif reizouko == "野菜":
            st.image(images['carrot'])
            st.image(images['potato'])
            st.image(images['onion'])
            st.image(images['cabbage'])
            st.image(images['lettuce'])
            st.image(images['tomato'])
            st.image(images['cucumber'])
            st.image(images['shiitake'])
            st.image(images['gobo'])
            st.image(images['broccoli'])
        elif reizouko == "調味料":
            st.image(images['salt'])
            st.image(images['sugar'])
            st.image(images['soy_sauce'])
            st.image(images['miso'])
            st.image(images['salad_oil'])
        elif reizouko == "その他":
            st.image(images['rice'])
            st.image(images['egg'])
            st.image(images['saba'])
            st.image(images['soba'])
            st.image(images['pasta'])
            st.image(images['butter'])
            st.image(images['bacon'])

def display_results():
    correct_answers = st.session_state.correct_answers
    total_questions = st.session_state.total_questions
    wrong_answers = [wa for wa in st.session_state.wrong_answers if wa[0] in st.session_state.selected_questions['No.'].values]
    result = mens_total //100
    st.write(f"終了！スコア: {result}")
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()