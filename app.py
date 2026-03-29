import streamlit as st
import streamlit.components.v1 as components
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="أفراح أبو ليله", page_icon="💍", layout="centered")

# --- 2. اتصال Firebase (النظام المضمون باستخدام Secrets) ---
@st.cache_resource
def init_db():
    if not firebase_admin._apps:
        try:
            # الربط المباشر مع [textkey] اللي حطيتها في Secrets الموقع
            key_dict = dict(st.secrets["textkey"])
            cred = credentials.Certificate(key_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"خطأ في الـ Secrets: تأكد من كتابة [textkey] بشكل صحيح في إعدادات Streamlit")
            st.stop()
    return firestore.client()

# تشغيل قاعدة البيانات
try:
    db = init_db()
except:
    st.warning("جاري تهيئة قاعدة البيانات...")

# إدارة حالة فتح الكارت
if 'opened' not in st.session_state:
    st.session_state.opened = False

# --- 3. تصميم الكارت (مقاسات مضبوطة للموبايل) ---
card_html = """
<div style="direction: rtl; text-align: center; font-family: 'Amiri', serif; background: white; padding: 15px; border-radius: 15px; border: 4px double #D4AF37; color: #333; max-width: 95%; margin: auto;">
    <style>@import url('https://fonts.googleapis.com/css2?family=Amiri&family=Reem+Kufi&display=swap');</style>
    <div style="color: #D4AF37; font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">﷽</div>
    <div style="font-size: 0.9rem; color: #555; line-height: 1.4; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 8px;">
        ﴿ وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً ﴾
    </div>
    <p style="font-size: 1rem; margin:0;">يتشرف الأستاذ/ <b style="color:#000;">صابر عبده</b></p>
    <p style="font-size: 0.9rem; margin:5px;">بدعوتكم لحضور حفل زفاف شقيقه</p>
    <div style="color: #D4AF37; font-size: 2.2rem; font-family: 'Reem Kufi', sans-serif; font-weight: bold; margin: 2px 0;">محمد عبده</div>
    <p style="color: #999; letter-spacing: 2px; margin-top:-8px; font-family: sans-serif; font-size: 0.7rem;">MOHAMED ABDO</p>
    <div style="background: #fafafa; padding: 8px; border-radius: 10px; margin: 10px 0; border: 1px solid #eee;">
        <p style="font-size: 0.9rem; margin: 3px;">📍 <b>المكان:</b> قاعة ميراج - بشما</p>
        <p style="font-size: 0.9rem; margin: 3px;">📅 <b>الموعد:</b> الجمعة 10 / 4 / 2026</p>
    </div>
    <p style="font-size: 1.1rem; color: #D4AF37; font-weight: bold;">فرحتنا تكتمل بوجودكم ❤️</p>
</div>
"""

# --- 4. العرض (أفراح أبو ليله) ---
st.markdown("<h1 style='text-align: center; color: #D4AF37; font-family: \"Reem Kufi\";'>أفراح أبو ليله</h1>",
            unsafe_allow_html=True)

if not st.session_state.opened:
    if os.path.exists("wedding.jpg"):
        st.image("wedding.jpg", use_container_width=True)
    if st.button("تفضلوا بفتح الدعوة ✨", use_container_width=True):
        st.session_state.opened = True
        st.rerun()
else:
    st.balloons()
    components.html(card_html, height=450)
    st.divider()

    # --- 5. دفتر المهنئين السريع ---
    st.subheader("💌 سجل كلمة للذكرى")
    name = st.text_input("الاسم الكريم:")
    msg = st.text_area("رسالة تهنئة للعريس:")

    if st.button("إرسال التهنئة ❤️", use_container_width=True):
        if name and msg:
            try:
                db.collection("wishes").add({
                    "name": name,
                    "message": msg,
                    "time": datetime.now()
                })
                st.success("تم الإرسال بنجاح! 😍")
                st.rerun()
            except Exception as e:
                st.error("فشل الإرسال، تأكد من إعدادات الـ Secrets على الموقع")
        else:
            st.warning("برجاء ملء الاسم والرسالة")

    st.divider()
    st.markdown("### 💜 دفتر المهنئين:")

    try:
        wishes = db.collection("wishes").order_by("time", direction=firestore.Query.DESCENDING).limit(10).get()
        if not wishes:
            st.info("كن أول المهنئين! ✨")
        else:
            for w in wishes:
                d = w.to_dict()
                st.markdown(f"""
                <div style="background:#f9f9f9; padding:10px; border-radius:10px; margin-bottom:10px; border-right:5px solid #D4AF37; direction:rtl;">
                    <b>{d.get('name')}</b>: {d.get('message')}
                </div>
                """, unsafe_allow_html=True)
    except:
        st.write("جاري تحميل التهاني...")

    if st.button("رجوع"):
        st.session_state.opened = False
        st.rerun()