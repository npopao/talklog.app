import streamlit as st
from googletrans import Translator
import requests
import json

# --- 設定（GASのURLをここに貼る） ---
GAS_URL = "あなたのGASのURLをここに貼る"

st.set_page_config(page_title="翻訳メモ(インドネシア語)", page_icon="🇮🇩")
st.title("🇮🇩 リアルタイム翻訳メモ")

translator = Translator()

st.write("キーボードのマイクで話すと、リアルタイムでインドネシア語になります。")

# 入力されたら即座に反応するように設定
text_input = st.text_area("日本語を入力（マイクで話してください）", height=100)

if text_input:
    try:
        # 【修正】翻訳先をインドネシア語 'id' に設定
        translated = translator.translate(text_input, src='ja', dest='id')
        
        # リアルタイム表示
        st.subheader("インドネシア語 (Bahasa Indonesia):")
        st.success(translated.text)
        
        # 保存ボタン
        if st.button("✅ この内容を保存する"):
            if GAS_URL != "あなたのGASのURLをここに貼る":
                data = {"ja": text_input, "trans": translated.text}
                requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
                st.balloons()
                st.info("スプレッドシートに保存しました！")
    except Exception as e:
        st.error(f"翻訳エラー: {e}")

st.divider()
st.caption("※スマホのキーボードで『音声入力』をオンにして話してください。")
