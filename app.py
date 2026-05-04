"""
AI Data Engineer Dashboard Generator
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from datetime import datetime
import plotly.express as px
import json

# Import dei moduli locali
from src.ml_analyzer import MLAnalyzer
from src.dashboard_generator import DashboardGenerator
from src.pdf_generator import PDFGenerator

# Configurazione pagina
st.set_page_config(
    page_title="AI Data Engineer - Dashboard Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 10px;
        font-weight: bold;
        transition: transform 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
    }
    .insight-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.5rem; }
        .metric-card { margin-bottom: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Data Engineer Dashboard Generator</h1>
    <p>Machine Learning-powered analytics | Automatic Dashboard | Tableau Ready</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
    st.markdown("## ⚙️ Configurazione")
    
    uploaded_file = st.file_uploader(
        "📁 Carica il tuo file",
        type=['csv', 'xlsx', 'xls', 'json', 'txt'],
        help="Supporto: CSV, Excel, JSON, TXT"
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Opzioni ML")
    auto_clustering = st.checkbox("Auto-Clustering", value=True)
    outlier_detection = st.checkbox("Rilevazione Outlier", value=True)
    feature_importance = st.checkbox("Feature Importance", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Output")
    generate_dashboard = st.checkbox("Genera Dashboard Web", value=True)
    generate_pdf = st.checkbox("Genera PDF per Tableau", value=True)
    
    st.markdown("---")
    st.markdown("### 📖 Info")
    st.info("""
    **Come funziona:**
    1. Carica un file dati
    2. ML analizza pattern
    3. Dashboard automatica
    4. PDF con istruzioni Tableau
    """)

# Funzione per caricare dati
@st.cache_data
def load_data(uploaded_file):
    """Carica e cache dei dati"""
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    try:
        if file_extension == '.csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == '.json':
            df = pd.read_json(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file, sep='\t')
        
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento: {str(e)}")
        return None

# Main content
if uploaded_file is not None:
    with st.spinner("🧠 Analisi con Machine Learning in corso..."):
        # Carica dati
        df = load_data(uploaded_file)
        
        if df is not None:
            # Inizializza analyzer
            analyzer = MLAnalyzer(df)
            
            # Esegui analisi ML
            profile = analyzer.analyze_data_profile()
            insights = analyzer.generate_ml_insights()
            
            # Mostra metriche principali
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Righe", f"{len(df):,}")
            with col2:
                st.metric("📋 Colonne", len(df.columns))
            with col3:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                st.metric("🔢 Metriche", len(numeric_cols))
            with col4:
                quality_score = insights.get('data_quality', {}).get('score', 0)
                st.metric("🎯 Qualità Dati", f"{quality_score:.0f}/100")
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Anteprima Dati", "🤖 ML Insights", "📊 Dashboard Dinamica", "📝 Guida Tableau"])
            
            with tab1:
                st.subheader("Anteprima dei dati")
                rows_to_show = st.slider("Numero di righe da mostrare", 5, 100, 20)
                st.dataframe(df.head(rows_to_show), use_container_width=True)
                
                st.subheader("Statistiche descrittive")
                st.dataframe(df.describe(), use_container_width=True)
                
                # Info colonne
                with st.expander("ℹ️ Info Colonne"):
                    col_info = pd.DataFrame({
                        'Tipo': df.dtypes,
                        'Non-Null': df.count(),
                        'Null %': (df.isnull().sum() / len(df) * 100).round(2),
                        'Unique': df.nunique()
                    })
                    st.dataframe(col_info, use_container_width=True)
            
            with tab2:
                st.subheader("Insights Machine Learning")
                
                # Data Quality
                with st.expander("📊 Data Quality Assessment", expanded=True):
                    quality = insights.get('data_quality', {})
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Score Qualità", f"{quality.get('score', 0):.0f}/100")
                    with col2:
                        st.metric("Dati Mancanti", f"{quality.get('missing_percentage', 0):.1f}%")
                    with col3:
                        st.metric("Outlier", "✅" if quality.get('has_outliers') else "❌")
                
                # Key Drivers
                if feature_importance and insights.get('key_drivers'):
                    with st.expander("🎯 Key Drivers (Random Forest)", expanded=True):
                        for driver in insights['key_drivers'][:5]:
                            st.progress(driver['importance'], text=f"{driver['feature']}: {driver['importance']:.2%}")
                
                # Correlazioni
                if profile.get('strong_correlations'):
                    with st.expander("🔗 Correlazioni Forti"):
                        for corr in profile['strong_correlations'][:3]:
                            st.info(f"**{corr['var1']}** ↔ **{corr['var2']}**: {corr['correlation']:.2f}")
                
                # Anomalie
                if insights.get('anomalies'):
                    with st.expander(f"⚠️ Anomalie Rilevate ({len(insights['anomalies'])})"):
                        for i, anomaly in enumerate(insights['anomalies'][:5]):
                            st.json(anomaly)
                
                # Raccomandazioni
                with st.expander("💡 Raccomandazioni per Tableau", expanded=True):
                    for rec in insights.get('recommendations', []):
                        st.markdown(f"""
                        <div class="insight-card">
                            <strong>🎯 {rec['type'].upper()}</strong><br>
                            {rec['text']}<br>
                            <small>📌 {rec['action']}</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab3:
                if generate_dashboard:
                    st.subheader("Dashboard Generata Automaticamente")
                    st.info("🎨 La dashboard è generata dinamicamente in base ai tuoi dati")
                    
                    # Genera dashboard HTML
                    dashboard_gen = DashboardGenerator(df, analyzer, insights)
                    
                    try:
                        html_content = dashboard_gen.create_dashboard_html()
                        
                        # Mostra in iframe
                        st.components.v1.html(html_content, height=800, scrolling=True)
                        
                        # Download button
                        st.download_button(
                            label="💾 Scarica Dashboard HTML",
                            data=html_content,
                            file_name=f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Errore nella generazione dashboard: {str(e)}")
                        st.info("Prova con un file con più dati numerici o categorie")
            
            with tab4:
                if generate_pdf:
                    st.subheader("Genera PDF con Passaggi Dettagliati per Tableau")
                    st.markdown("""
                    Il PDF includerà:
                    - ✅ Passaggi preparazione dati in Tableau Prep
                    - ✅ Layout dashboard raccomandato
                    - ✅ Campi calcolati suggeriti
                    - ✅ Checklist validazione
                    - ✅ Best practices Tableau
                    """)
                    
                    if st.button("📄 Genera PDF Guide", use_container_width=True):
                        with st.spinner("Creazione PDF in corso..."):
                            try:
                                pdf_gen = PDFGenerator(df, insights, analyzer)
                                pdf_file = pdf_gen.generate()
                                
                                with open(pdf_file, 'rb') as f:
                                    st.download_button(
                                        label="📥 Scarica PDF Guide Tableau",
                                        data=f.read(),
                                        file_name=f"tableau_guide_{datetime.now().strftime('%Y%m%d')}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                
                                st.success("✅ PDF generato con successo! Contiene tutti i passaggi per ricreare la dashboard in Tableau.")
                                
                                # Mostra anteprima
                                with st.expander("📖 Anteprima del contenuto"):
                                    st.markdown("""
                                    **Il PDF include:**
                                    1. Analisi del dataset (dimensioni, qualità)
                                    2. Passaggi preparazione dati
                                    3. Layout dashboard consigliato
                                    4. Calcoli e formule Tableau
                                    5. Filtri interattivi
                                    6. Checklist di verifica
                                    """)
                            except Exception as e:
                                st.error(f"Errore generazione PDF: {str(e)}")
                                st.info("Assicurati di avere reportlab installato")
else:
    # Hero section quando nessun file è caricato
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/fluency/200/000000/data-configuration.png")
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>🚀 Pronto a generare dashboard intelligenti?</h2>
            <p>Carica un file CSV, Excel o JSON e lascia che il Machine Learning faccia il resto</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Esempi di dataset
        with st.expander("📁 Dataset di esempio"):
            st.markdown("""
            **Puoi usare:**  
            - Dataset vendite (order_date, product, sales, quantity)  
            - Dati HR (employee_id, department, salary, performance)  
            - Metriche marketing (impressions, clicks, conversions)  
            - Dati finanziari (date, revenue, costs, profit)  
            - Qualsiasi file tabellare!
            
            **Colonne ideali per migliori risultati:**  
            - Almeno 2-3 colonne numeriche  
            - 1 colonna temporale (opzionale ma consigliata)  
            - 1-2 colonne categoriche  
            - Minimo 50 righe di dati
            """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<p style='text-align: left; color: gray;'>🤖 Powered by Machine Learning</p>", unsafe_allow_html=True)
with col2:
    st.markdown("<p style='text-align: center; color: gray;'>📊 Generazione Dashboard Automatica</p>", unsafe_allow_html=True)
with col3:
    st.markdown("<p style='text-align: right; color: gray;'>📝 Guida Tableau Inclusa</p>", unsafe_allow_html=True)
