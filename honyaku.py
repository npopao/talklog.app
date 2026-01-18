import streamlit as st
import requests
import json

# 送信先のGAS URL
GAS_URL = "https://script.google.com/macros/s/AKfycbwcsvq1jvhrUzpw1fDw10E8VUQg0qIhUAVPJEQzLqRLPSi5sAXo1lK8XFo1gAc3aecTKA/exec"

st.set_page_config(page_title="おはなしメモ", page_icon="🎤")
st.title("🎤 リアルタイム翻訳メモ")

# 言語選択
option = st.selectbox('翻訳言語', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# 1. 入力エリア（音声入力が終わると、プログラムが自動で下へ進みます）
text_input = st.text_area("日本語で話してください（入力が終わると自動で翻訳します）", height=120)

# --- ここから「自動翻訳」の処理 ---
if text_input:
    # GASに翻訳だけをお願いする
    payload = {
        "ja": text_input,
        "lang": lang_code,
        "mode": "translate_only" # 翻訳だけして、まだ保存しないモード
    }
    
    try:
        # ボタンを押さなくても、入力があれば即座にGASに通信
        response = requests.post(GAS_URL, data=json.dumps(payload))
        translated_text = response.text # GASから返ってきた翻訳結果
        
        # 翻訳結果を即座に表示！
        st.subheader(f"【{option}】")
        st.success(translated_text)
        
        # 2. 保存ボタン（翻訳結果を見てから、残したい場合だけ押す）
        if st.button("✅ この内容をシートに保存する"):
            save_payload = {"ja": text_input, "lang": lang_code, "mode": "save"}
            requests.post(GAS_URL, data=json.dumps(save_payload))
            st.balloons()
            st.write("スプレッドシートに記録しました！")
            
    except Exception as e:
        st.error(f"翻訳通信エラー: {e}")

st.divider()
st.caption("PC: [Win+H] / スマホ: キーボードのマイク で音声入力してください。")