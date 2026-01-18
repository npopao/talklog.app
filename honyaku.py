import streamlit as st
from googletrans import Translator
from streamlit_mic_recorder import mic_recorder
import requests
import json

# --- 設定（GASのURLを貼ってください） ---
GAS_URL = "あなたのGASのURL"

st.set_page_config(page_title="おはなしメモ", page_icon="🎤")
st.title("🎤 おはなしメモ（録音版）")

translator = Translator()

# 言語選択
option = st.selectbox('翻訳先', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# 録音ボタン（昨夜の部品）
audio = mic_recorder(start_prompt="🎤 録音開始", stop_prompt="⏹️ 録音終了", key='recorder')

if audio:
    # 録音した音を再生できるようにする
    st.audio(audio['bytes'])
    st.info("※音声の自動テキスト化はスマホ・PCの『音声入力』機能が最も正確です。下の枠を使ってください。")

# 入力エリア
text_input = st.text_area("日本語を入力（または音声入力）", height=100)

if text_input:
    try:
        # 翻訳
        translated = translator.translate(text_input, src='ja', dest=lang_code)
        st.subheader(f"【{option}】")
        st.success(translated.text)
        
        # 保存ボタン
        if st.button("✅ スプレッドシートに保存"):
            data = {"ja": text_input, "trans": translated.text}
            requests.post(GAS_URL, data=json.dumps(data))
            st.balloons()
            st.write("保存完了！")
    except Exception as e:
        st.error(f"翻訳エラー: {e}")
