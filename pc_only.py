import streamlit as st
from googletrans import Translator
from streamlit_mic_recorder import mic_recorder
import io

st.title("🎤 昨夜の完成版（録音ボタンあり）")

translator = Translator()

# 録音ボタン
audio = mic_recorder(start_prompt="🎤 録音開始", stop_prompt="⏹️ 録音終了", key='pc_recorder')

if audio:
    st.audio(audio['bytes'])
    # ※昨夜の時点ではここから翻訳処理へ繋がっていました
    st.success("音声が届きました！")
    # ここに昨夜の翻訳ロジックを戻せます
