import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
import openai

st.set_page_config(page_title="Diyet Planı", layout="centered")

st.title("📅 Diyet Planı")

# Diyet planları için klasörü kontrol et
Path("db").mkdir(parents=True, exist_ok=True)
Path("temp").mkdir(parents=True, exist_ok=True)  # geçici klasörü oluştur

# db klasörünü diet_plan dosyaları için kontrol et
path = Path("db")
if not path.exists():
    os.makedirs(path)
else:
    # db klasöründe diet_plan_ ile başlayan dosyaları kontrol et
    existing_files = [f for f in os.listdir(path) if f.startswith("diet_plan_") and f.endswith(".json")]

bugun = datetime.now().strftime("%d-%m-%Y")
dosya_adi = f"diet_plan_{bugun}.json"
counter = 0
if dosya_adi in existing_files:
    while dosya_adi in existing_files:
        counter += 1
        dosya_adi = f"diet_plan_{bugun}_{counter}.json"
dosya_yolu = Path("db") / dosya_adi

if len(existing_files) < 1 or st.toggle("yeni plan oluştur", key="plan_olustur", value=False):
    st.write("dosya yolu:", dosya_yolu)
    #st.warning("Henüz bir diyet planı oluşturulmamış.")        
    if st.button("🛠️ Hemen Oluştur"):
        st.session_state["plan_olustur"] = True

else:
    # get all files in db/ folder that start with "diet_plan_"
    existing_files = [f for f in os.listdir("db") if f.startswith("diet_plan_") and f.endswith(".json")]
    if existing_files:
        selected_plan = st.selectbox(
            "📂 Mevcut Diyet Planları",
            options=existing_files,
            index=0,
            key="existing_diet_plans",
            help="Mevcut diyet planlarınızı buradan seçebilirsiniz."
        )
        st.session_state["selected_plan"] = selected_plan

# Plan oluşturulursa gerekli girdileri al
if "plan_olustur" in st.session_state and st.session_state.plan_olustur:
    placeholder_for_title = st.empty()
    openai_key = st.session_state.get("OPENAI_API_KEY") or st.text_input("OpenAI Key'inizi girin", type="password")
    if len(openai_key) < 5:
        placeholder_for_title.subheader("🔑 OpenAI API Key")
    openai.api_key = openai_key

    st.subheader("🔎 Opsiyonel Belgeler (Kan Tahlili, Rapor vs)")
    belgeler = st.file_uploader("Belgeleri yükleyin", type=["pdf", "txt", "csv", "jpg", "jpeg", "png", "webp", "docx"], accept_multiple_files=True)

    st.subheader("📝 Ek Bilgiler")
    ek_bilgi = st.text_area("Diyet için özellikle dikkat edilmesini istediğiniz hususlar", help="Alerjiler, sevmediğiniz gıdalar, bütçe limitleri, her şeyden bahsedebilirsiniz.", placeholder="Alerjiler, sevmediğiniz gıdalar, bütçe limitleri, her şeyden bahsedebilirsiniz.")

    if st.button("📨 OpenAI'ye Gönder ve Planı Oluştur") and openai_key:
        uploaded_file_ids = []
        for file in belgeler or []:
            temp_path = Path("temp") / file.name
            with open(temp_path, "wb") as temp_f:
                temp_f.write(file.read())
            with open(temp_path, "rb") as f:
                uploaded = openai.files.create(file=f, purpose="user_data")
                uploaded_file_ids.append(uploaded.id)
            os.remove(temp_path)

        content_blocks = []
        for fid in uploaded_file_ids:
            content_blocks.append({"type": "file", "file": {"file_id": fid}})

        if ek_bilgi:
            content_blocks.append({"type": "text", "text": ek_bilgi})

        system_prompt = "Sen bir kişisel sağlık ve beslenme asistanısın. Kullanıcı sana kan tahlili belgeleri gibi çeşitli ve açıklayıcı bilgiler içeren belgeler yükleyebilir buna ek olarak ek promptlar da iletebilir alerjileri veya sevmediği gıdalar gibi. Görevin bu bilgileri analiz edip sağlık açısından önemli verileri özetlemek ve sonra buna uygun şekilde kişiselleştirilmiş bir diyet sistemi oluşturmaktır."

        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",
                    "content": (
                        system_prompt
                        + "\n\nLütfen çıktıyı sadece aşağıdaki JSON formatına birebir uygun şekilde üret (eğer hiç belge yüklenmediyse document_reports'u boş array olarak bırak):\n\n"
                        + json.dumps({
                            "document_reports": [
                                {
                                    "document_title": "ai generated kısa title",
                                    "document_summary": "diyet odaklı kısa özet"
                                }
                            ],
                            "generated_system_prompt": "kullanıcının belirlediği gün/hafta sayısına ve kullanıcının sağlık durumuna uygun şekilde diyet programı oluşturacak bir ai requestin sistem promptu olacak şekilde oldukça detaylı oluştur.",
                            "system_prompt_summary": "yukarıda yarattığın sistem promptu kullanıcıya özetlemeye yarayan bir açıklamadır.",
                        }, indent=2, ensure_ascii=False)
                    )
                },
                {
                    "role": "user",
                    "content": content_blocks
                }
            ]
        )

        response_raw = json.loads(response.choices[0].message.content)
        response_text = json.dump(response_raw, open("response.json", "w"), indent=2)
        with st.expander("Response"):
            st.write(response_raw)
        generated_prompt = response_raw["generated_system_prompt"]
        system_prompt_summary = response_raw["system_prompt_summary"]
        
        output = {
            "document_reports": [],
            "system_prompt_summary": system_prompt_summary,
            "generated_system_prompt": generated_prompt
        }

        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        st.success("✅ Diyet planı oluşturuldu")
        st.rerun()

# JSON dosyası varsa, detayları göster
if dosya_yolu.exists() or "selected_plan" in st.session_state:
    if "selected_plan" in st.session_state:
        dosya_yolu = Path("db") / st.session_state.selected_plan
    with open(dosya_yolu, encoding="utf-8") as f:
        veri = json.load(f)

    with st.expander("📌 Sana şunlara dikkat ederek bir diyet programı hazırlayabilirim"):
        st.write(veri.get("system_prompt_summary", "-"))

    st.markdown("---")
    st.subheader("📅 Diyet Planı Seçimi")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1.5, 2, 1], vertical_alignment="center")
    placeholder_diyet = st.empty()
    with col1: st.write("Bana")
    with col2: miktar = st.number_input(" ", label_visibility="collapsed", min_value=1, max_value=30, value=7)
    with col3: periyot = st.selectbox(" ",  label_visibility="collapsed", options=["günlük", "haftalık", "aylık"])
    with col4: st.write("diyet programı")
    with col5:
        if st.button("Hazırla!"):
            system_prompt = veri.get("generated_system_prompt", "")

            # Diyet planı oluşturmak için OpenAI'ye isteği gönder
            second_response = openai.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": (
                            f"Lütfen {miktar} {periyot} sürelik bir diyet programı hazırla ve json olarak çıktı ver. "
                            "Market olarak sadece BİM, A101 ve ŞOK kullanılabilir. "
                            "Yemek tariflerini ve market ürünlerini detaylı yaz. "
                            "Çıktı formatı şu olsun: "
                            + json.dumps({
                                "haftalar": [
                                    {"hafta": 1,
                                    "günler": [
                                        {"gün": "Pazartesi",
                                        "öğünler": [
                                            {"öğün": "Öğle",
                                            "yemekler": [
                                                {
                                                    "isim": "<yemek adı>",
                                                    "sebep": "<diyet için neden önemli.>",
                                                    "önem": "3/5",
                                                    "alinacak_malzemeler": [
                                                        {
                                                            "ürün": "<ürün adı>",
                                                            "marka": "<ürün markası>",
                                                            "miktar": "<miktar> g",
                                                            "market": "<BİM/A101/ŞOK>"
                                                        }
                                                    ],
                                                    "tarif": [
                                                        "<tarif adımı 1>",
                                                        "<tarif adımı 2>",
                                                    ]
                                                }
                                            ]}
                                        ]}
                                    ]}
                                ]
                            })
                        )
                    }
                ]
            )
            placeholder_diyet.markdown("### ✅ Oluşan Diyet Planı:")
            placeholder_diyet.write(second_response)
            response2_raw = json.loads(second_response.choices[0].message.content)
            placeholder_diyet.write(response2_raw)
            json.dump(response2_raw, open("second_response.json", "w"), indent=2)
