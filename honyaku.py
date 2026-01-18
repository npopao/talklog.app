import streamlit as st
from googletrans import Translator
import requests
import json

# --- 設定（ここにGASのURLを後で貼ります） ---
GAS_URL = "あなたのGASのURLをここに貼る"

st.set_page_config(page_title="翻訳保存ツール", page_icon="📝")
st.title("📝 現場用・おはなしメモ")

translator = Translator()

st.write("下の枠をタップして、キーボードのマイクで話すか、文字を入力してください。")

# 入力エリア
text_input = st.text_area("日本語を入力", placeholder="例：明日の会議は10時からです", height=150)

if text_input:
    try:
        # 翻訳実行
        translated = translator.translate(text_input, src='ja', dest='en')
        
        st.subheader("英語翻訳:")
        st.success(translated.text)
        
        # 送信ボタン
        if st.button("✅ この内容をスプレッドシートに保存"):
            if GAS_URL != "あなたのGASのURLをここに貼る":
                data = {"ja": text_input, "trans": translated.text}
                response = requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
                if response.status_code == 200:
                    st.balloons()
                    st.info("スプレッドシートに保存しました！")
                else:
                    st.error("保存に失敗しました。URLを確認してください。")
            else:
                st.warning("GASのURLが設定されていません。")
                
    except Exception as e:
        st.error(f"翻訳エラー: {e}")

st.divider()
st.caption("スマホのキーボードにあるマイクを使うと、きれいに聞き取れます。")
