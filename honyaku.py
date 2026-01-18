import streamlit as st
import requests
import json

# 送信先のGAS URL
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="おはなしメモ", page_icon="🎤")

# 余白を削って、入力と翻訳がすぐ目に入るようにします
st.title("🎤 リアルタイム翻訳メモ")

# 言語選択
option = st.selectbox('翻訳言語', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# 1. 入力エリア
# 「Enterで確定」ではなく、文字が変わるたびに即座に反応する設定にします
text_input = st.text_input("日本語で話してください（入力されると自動翻訳）", key="input_text")

# --- ここから「自動翻訳」の処理 ---
if text_input:
    payload = {
        "ja": text_input,
        "lang": lang_code,
        "mode": "translate_only"
    }
    
    try:
        # GASに問い合わせ
        response = requests.post(GAS_URL, data=json.dumps(payload))
        translated_text = response.text
        
        # 翻訳結果を大きく表示
        st.markdown(f"### 【{option}】")
        st.success(translated_text)
        
        # 2. 保存ボタン
        if st.button("✅ この内容をシートに保存"):
            save_payload = {"ja": text_input, "lang": lang_code, "mode": "save"}
            requests.post(GAS_URL, data=json.dumps(save_payload))
            st.balloons()
            st.write("保存しました！")
            
    except Exception as e:
        st.error(f"通信エラー: {e}")

st.divider()
st.caption("スマホ: キーボードのマイクで喋り、少し待つか完了を押すと翻訳されます。")