import streamlit as st
from googletrans import Translator
from streamlit_mic_recorder import speech_to_text
import requests
import json

# --- 設定（ここにGASのURLを後で入れます） ---
GAS_URL = "あなたのGASのURLをここに貼る"

st.set_page_config(page_title="おはなしメモ", page_icon="🎤")
st.title("🎤 おはなしメモ (Cloud版)")

# 翻訳エンジンの準備
translator = Translator()

st.write("ボタンを押してからお話しください。")

# --- マイク入力部分（ブラウザのマイクを使います） ---
text = speech_to_text(
    language='ja',
    start_prompt="🎤 話す (録音開始)",
    stop_prompt="⏹️ 停止 (翻訳する)",
    just_once=False,
    key='speech'
)

if text:
    st.subheader("入力された日本語:")
    st.write(text)
    
    # 翻訳処理
    try:
        translated = translator.translate(text, src='ja', dest='en')
        st.subheader("英語翻訳:")
        st.success(translated.text)
        
        # --- Googleスプレッドシート(GAS)への送信 ---
        if GAS_URL != "あなたのGASのURLをここに貼る":
            data = {
                "ja": text,
                "trans": translated.text
            }
            response = requests.post(GAS_URL, data=json.dumps(data))
            if response.status_code == 200:
                st.info("✅ 会社のGoogleドライブに保存しました")
            else:
                st.error("⚠️ 保存に失敗しました")
                
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

st.divider()
st.caption("※このアプリはGoogleドライブ（GAS）と連携してデータを保存します。")
