import streamlit as st
from googletrans import Translator
import requests
import json

# --- 設定（GASのURLをここに貼る） ---
GAS_URL = "あなたのGASのURLをここに貼る"

st.set_page_config(page_title="おはなしメモ", page_icon="📝")
st.title("📝 おはなしメモ (現場安定版)")

translator = Translator()

st.write("日本語を入力して「翻訳＆保存」を押してください。")

# 入力欄
text_input = st.text_area("日本語を入力", placeholder="例：明日の会議は10時からです", height=100)

if st.button("🚀 翻訳して保存"):
    if text_input:
        try:
            # 翻訳実行
            translated = translator.translate(text_input, src='ja', dest='en')
            
            # 結果表示
            st.subheader("英語翻訳:")
            st.success(translated.text)
            
            # GASへの送信
            if GAS_URL != "あなたのGASのURLをここに貼る":
                data = {"ja": text_input, "trans": translated.text}
                response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
                
                if response.status_code == 200:
                    st.toast("✅ スプレッドシートに保存しました！")
                else:
                    st.error("保存に失敗しました。URLを確認してください。")
            else:
                st.warning("⚠️ GASのURLが設定されていません。")
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("日本語を入力してください。")

st.divider()
st.caption("スマホの音声入力機能（マイクアイコン）を使えば、声での入力も可能です。")
