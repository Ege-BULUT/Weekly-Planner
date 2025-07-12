import streamlit as st
import os 
import json

@st.dialog("Bilgi!")
def text_renderer(text):
    st.write(text)
    

st.title("Diyet oluşturucu & Haftalık Planlama")

# check db/ folder if "OPENAI_KEY.json" is not exists warn the user and create a new one
if not os.path.exists("db/OPENAI_KEY.json") or len(open("db/OPENAI_KEY.json").read()) < 5:

    st.info("bu programı kullanabilmek için geçerli bir OpenAI API anahtarınız gereklidir.")
    if st.button("Nereden bulurum?"):
        text_renderer("Lütfen [buraya](https://platform.openai.com/account/api-keys) giderek bir anahtar oluşturun ve bu anahtarı buraya yapıştırın.")
    st.text_input("OpenAI API anahtarınızı girin", key="OPENAI_API_KEY")
    disabled = len(st.session_state.OPENAI_API_KEY) < 5
    if st.button("Kaydet", disabled=disabled):
        with open("db/OPENAI_KEY.json", "w") as f:
            out={"openai_api_key": st.session_state.OPENAI_API_KEY}
            f.write(json.dumps(out))
        st.rerun()
else:
    try:
        key = json.loads(open("db/OPENAI_KEY.json", "r").read())["openai_api_key"]
        st.session_state.OPENAI_API_KEY = key
        st.info("OpenAI Anahtarınız başarıyla kaydedildi. (db/OPENAI_KEY.json)")
    except:
        st.info("bu programı kullanabilmek için geçerli bir OpenAI API anahtarınız gereklidir.")
        if st.button("Nereden bulurum?"):
            text_renderer("Lütfen [buraya](https://platform.openai.com/account/api-keys) giderek bir anahtar oluşturun ve bu anahtarı buraya yapıştırın.")
        st.text_input("OpenAI API anahtarınızı girin", key="OPENAI_API_KEY")
        disabled = len(st.session_state.OPENAI_API_KEY) < 5
        if st.button("Kaydet", disabled=disabled):
            with open("db/OPENAI_KEY.json", "w") as f:
                out={"openai_api_key": st.session_state.OPENAI_API_KEY}
                f.write(json.dumps(out))
            st.rerun()
            
    