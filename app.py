import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Operasyon Karnesi", layout="wide")

# Excel dosya yolu
EXCEL_PATH = "data/KARNE ÇALIŞMA GÜNCEL.xlsx"

@st.cache_data
def load_all_data():
    # Sayfa yapılarına göre skiprows (atlanan satır) ayarları
    kalite = pd.read_excel(EXCEL_PATH, sheet_name="KALİTE HAM DATA", skiprows=16)
    quiz = pd.read_excel(EXCEL_PATH, sheet_name="QUİZ HAM RAPOR", skiprows=14)
    mma = pd.read_excel(EXCEL_PATH, sheet_name="MMA HAM DATA", skiprows=13)
    return kalite, quiz, mma

try:
    kalite_df, quiz_df, mma_df = load_all_data()

    st.title("📊 Çağrı Merkezi Karne Dashboard")
    st.markdown("---")

    # Yan Panel Filtreleri
    st.sidebar.header("Filtreleme")
    selected_loc = st.sidebar.multiselect("Lokasyon Seç", options=kalite_df["LOKASYON"].unique(), default=kalite_df["LOKASYON"].unique())

    # Veriyi Filtreleme
    k_filtered = kalite_df[kalite_df["LOKASYON"].isin(selected_loc)]
    q_filtered = quiz_df[quiz_df["LOKASYON"].isin(selected_loc)]

    # Üst Bölüm: KPI Kartları
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Genel Kalite Puanı", f"{k_filtered['Kalite Puanı'].mean():.2f}")
    col2.metric("Quiz Başarı Ort.", f"%{q_filtered['BasariPuani'].mean():.2f}")
    col3.metric("Anket Sayısı (MMA)", len(mma_df))
    col4.metric("Toplam Değerlendirme", len(k_filtered))

    st.markdown("---")

    # Grafikler
    c1, c2 = st.columns(2)
    
    with c1:
        # Lider Bazlı Performans
        fig_lider = px.bar(k_filtered.groupby("Takım Lideri")["Kalite Puanı"].mean().reset_index(),
                           x="Takım Lideri", y="Kalite Puanı", title="Takım Lideri Kalite Puanları",
                           color="Kalite Puanı", color_continuous_scale="Viridis")
        st.plotly_chart(fig_lider, use_container_width=True)

    with c2:
        # Lokasyon Dağılımı
        fig_pie = px.pie(k_filtered, names="LOKASYON", title="Lokasyon Bazlı Değerlendirme Yüzdesi")
        st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Bir hata oluştu! Lütfen dosya adının ve klasör yapısının doğru olduğunu kontrol edin.")
    st.info(f"Hata Detayı: {e}")
