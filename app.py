import streamlit as st
import streamlit.components.v1 as components
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="أفراح أبو ليله", page_icon="💍", layout="centered")


# --- 2. اتصال Firebase ---
@st.cache_resource
def init_db():
    if not firebase_admin._apps:
        path = "key.json" if os.path.exists("key.json") else "A.mid/key.json"
        if os.path.exists(path):
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred)
        else:
            st.error("ملف key.json غير موجود!")
            st.stop()
    return firestore.client()


db = init_db()

if 'opened' not in st.session_state:
    st.session_state.opened = False

# --- 3. تصميم الكارت (HTML + CSS) ---
# حطينا الـ CSS جوه الـ HTML عشان نضمن إن مفيش حاجة تضرب
card_html = """
<div style="direction: rtl; text-align: center; font-family: 'Amiri', serif; background: white; padding: 25px; border-radius: 15px; border: 4px double #D4AF37; color: #333; max-width: 550px; margin: auto;">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Reem+Kufi&display=swap');
    </style>
    <div style="color: #D4AF37; font-size: 1.8rem; font-weight: bold; margin-bottom: 5px;">﷽</div>
    <div style="font-size: 1.1rem; color: #555; line-height: 1.6; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px;">
        ﴿ وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً ﴾
    </div>

    <p style="font-size: 1.1rem; margin:0;">يتشرف الأستاذ/ <b style="color:#000;">صابر عبده</b></p>
    <p style="font-size: 1rem; margin:5px;">بدعوتكم لحضور حفل زفاف شقيقه</p>

    <div style="color: #D4AF37; font-size: 2.8rem; font-family: 'Reem Kufi', sans-serif; font-weight: bold; margin: 5px 0;">محمد عبده</div>
    <p style="color: #999; letter-spacing: 2px; margin-top:-10px; font-family: sans-serif;">MOHAMED ABDO</p>

    <div style="background: #fafafa; padding: 15px; border-radius: 10px; margin: 15px 0; border: 1px solid #eee;">
        <p style="font-size: 1.1rem; margin: 5px;">📍 <b>المكان:</b> قاعة ميراج - بشما</p>
        <p style="font-size: 1.1rem; margin: 5px;">📅 <b>الموعد:</b> الجمعة 2026 / 4 / 10</p>
    </div>

    <p style="font-size: 1.3rem; color: #D4AF37; font-weight: bold;">فرحتنا تكتمل بوجودكم ❤️</p>
</div>
"""

# --- المرحلة 1: الغلاف ---
if not st.session_state.opened:
    st.markdown("<h1 style='text-align: center; color: #D4AF37; font-family: \"Reem Kufi\";'>أفراح أبو ليله</h1>",
                unsafe_allow_html=True)

    img_path = "A.mid/wedding.jpg" if os.path.exists("A.mid/wedding.jpg") else "wedding.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

    if st.button("تفضلوا بفتح الدعوة ✨", use_container_width=True):
        st.session_state.opened = True
        st.rerun()

# --- المرحلة 2: الكارت ---
else:
    st.balloons()

    # هنا بقى "القاضية".. بنعرض الـ HTML كـ Component منفصل تماماً
    components.html(card_html, height=550)

    st.divider()

    st.subheader("💌 سجل كلمة للذكرى")
    with st.form("wishes_form", clear_on_submit=True):
        name = st.text_input("الاسم الكريم:")
        msg = st.text_area("رسالة تهنئة للعريس:")
        if st.form_submit_button("إرسال التهنئة ❤️"):
            if name and msg:
                db.collection("wishes").add({"name": name, "message": msg, "time": datetime.now()})
                st.success("وصلت التهنئة! 🥳")
                st.snow()

    st.divider()
    st.subheader("💟 دفتر المهنئين:")
    docs = db.collection("wishes").order_by("time", direction=firestore.Query.DESCENDING).limit(5).stream()
    for doc in docs:
        d = doc.to_dict()
        st.info(f"👤 {d.get('name')}: {d.get('message')}")

    if st.button("رجوع"):
        st.session_state.opened = False
        st.rerun()