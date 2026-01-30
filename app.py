import streamlit as st
import pandas as pd
import plotly.express as px

# Excel dosya yolu
FILE_PATH = "data/KARNE ÇALIŞMA GÜNCEL.xlsx"

@st.cache_data
def get_data(sheet, skip):
    return pd.read_excel(FILE_PATH, sheet_name=sheet, skiprows=skip)

st.title("🚀 Operasyonel Karne Dashboard")

try:
    # Sayfaları çekiyoruz
    df_kalite = get_data("KALİTE HAM DATA", 16)
    df_quiz = get_data("QUİZ HAM RAPOR", 14)
    df_mma = get_data("MMA HAM DATA", 13)

    # Yan Panel Filtreleri
    st.sidebar.header("Filtreleme")
    lokasyon = st.sidebar.multiselect("Lokasyon Seç", options=df_kalite["LOKASYON"].unique(), default=df_kalite["LOKASYON"].unique())
    
    # Filtrelemeyi uygula
    df_filtered = df_kalite[df_kalite["LOKASYON"].isin(lokasyon)]

    # KPI'lar
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Ortalama Kalite", f"{df_filtered['Kalite Puanı'].mean():.2f}")
    kpi2.metric("Quiz Başarısı", f"%{df_quiz['BasariPuani'].mean():.2f}")
    kpi3.metric("Toplam Çağrı (MMA)", len(df_mma))

    # Grafik
    fig = px.sunburst(df_filtered, path=['LOKASYON', 'Takım Lideri'], values='Kalite Puanı', title="Lokasyon ve Lider Dağılımı")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Dosya okunurken bir hata oluştu. Lütfen 'data' klasöründe dosyanın olduğundan emin olun. Hata: {e}")
