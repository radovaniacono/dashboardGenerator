"""
AI Data Engineer Dashboard Generator - Versione Intelligente
Layout fisso 1000x800, KPI e grafici adattivi, filtri dinamici, colori pastello
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ==================== CONFIG PAGINA ====================
st.set_page_config(
    page_title="AI Dashboard Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS per fissare altezza e rimuovere scroll
st.markdown("""
<style>
    .main > div {
        height: 100vh;
        overflow: hidden;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    .stApp {
        background: #F9FBF4;
    }
    /* Sidebar più stretta e ordinata */
    section[data-testid="stSidebar"] {
        width: 260px !important;
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    /* Card KPI personalizzate */
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 0.8rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        border-top: 3px solid;
        transition: all 0.2s;
    }
    .kpi-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #4A5568;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2D3748;
        line-height: 1.2;
    }
    .kpi-trend {
        font-size: 0.65rem;
        color: #A0AEC0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNZIONI UTILI ====================
def clean_dataframe(df):
    """Pulisce il dataframe per evitare errori Arrow"""
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('').astype(str)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')
        elif df[col].dtype.name == 'category':
            df[col] = df[col].astype(str)
    return df

@st.cache_data
def load_data(uploaded_file):
    """Carica file CSV/Excel/JSON"""
    file_extension = Path(uploaded_file.name).suffix.lower()
    try:
        if file_extension == '.csv':
            for enc in ['utf-8', 'latin1', 'iso-8859-1']:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=enc)
                    break
                except:
                    continue
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        elif file_extension == '.json':
            df = pd.read_json(uploaded_file)
        else:
            return None
        return clean_dataframe(df)
    except Exception as e:
        st.error(f"Errore caricamento: {e}")
        return None

def intelligente_kpi(df, numeric_cols):
    """Seleziona automaticamente i 4 KPI più rilevanti"""
    kpi_list = []
    
    # 1. Totale vendite/fatturato se esiste colonna simile
    keywords_tot = ['vendite', 'sales', 'ricavi', 'revenue', 'fatturato', 'amount']
    for col in numeric_cols:
        if any(k in col.lower() for k in keywords_tot):
            kpi_list.append(('💰 ' + col, df[col].sum(), 'Totale'))
            break
    
    # 2. Profitto o margine
    keywords_prof = ['profitto', 'profit', 'margine', 'margin']
    for col in numeric_cols:
        if any(k in col.lower() for k in keywords_prof):
            kpi_list.append(('📈 ' + col, df[col].mean() if 'marg' in col.lower() else df[col].sum(), 'Media' if 'marg' in col.lower() else 'Totale'))
            break
    
    # 3. Conteggio righe come KPI generico (numero transazioni/clienti)
    kpi_list.append(('📊 N. Record', len(df), 'Conteggio'))
    
    # 4. Media di una metrica importante rimasta
    for col in numeric_cols:
        if col.lower() not in ['vendite','sales','ricavi','profitto','profit','margine','margin']:
            kpi_list.append(('📉 Media ' + col, df[col].mean(), 'Media'))
            break
    
    # Se abbiamo meno di 4, riempi con altre medie
    while len(kpi_list) < 4 and len(numeric_cols) > len(kpi_list):
        for col in numeric_cols:
            if not any(kpi[0].endswith(col) for kpi in kpi_list):
                kpi_list.append(('📊 ' + col, df[col].mean(), 'Media'))
                break
    
    return kpi_list[:4]

def scegli_grafici(df, numeric_cols, categorical_cols, date_cols):
    """Decide quali grafici mostrare in base ai dati"""
    grafici = []
    
    # 1. Se c'è una colonna data -> grafico a linee (trend)
    if date_cols:
        date_col = date_cols[0]
        # Aggrega per data se ci sono metriche numeriche
        if numeric_cols:
            metric = numeric_cols[0]
            df_time = df.groupby(date_col)[metric].sum().reset_index()
            fig = px.line(df_time, x=date_col, y=metric, title=f"Andamento {metric} nel tempo",
                          color_discrete_sequence=['#764BA2'])
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=20,r=20,t=40,b=20))
            grafici.append(('time_series', fig))
    
    # 2. Bar chart per categoria principale
    if categorical_cols:
        cat_col = categorical_cols[0]
        if numeric_cols:
            metric = numeric_cols[0]
            df_bar = df.groupby(cat_col)[metric].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(df_bar, x=cat_col, y=metric, title=f"Top 10 {cat_col} per {metric}",
                         color_discrete_sequence=['#A8E6CF'])
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', xaxis_tickangle=45, margin=dict(l=20,r=20,t=40,b=20))
            grafici.append(('bar_chart', fig))
    
    # 3. Scatter plot (due metriche numeriche)
    if len(numeric_cols) >= 2:
        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                         color_discrete_sequence=['#FFAAA5'], opacity=0.7)
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=20,r=20,t=40,b=20))
        grafici.append(('scatter', fig))
    
    # 4. Heatmap correlazione
    if len(numeric_cols) >= 3:
        corr = df[numeric_cols].corr()
        fig = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns,
                                       colorscale='tealrose', text=corr.values.round(2), texttemplate='%{text}'))
        fig.update_layout(title="Matrice di correlazione", height=350, margin=dict(l=20,r=20,t=40,b=20))
        grafici.append(('heatmap', fig))
    
    # 5. Tabella pivot (se spazio e pochi grafici)
    if len(grafici) < 3 and categorical_cols and numeric_cols:
        pivot = df.groupby(categorical_cols[0])[numeric_cols[0]].mean().reset_index().head(8)
        fig = go.Figure(data=[go.Table(header=dict(values=list(pivot.columns), fill_color='#C7CEEA'),
                                       cells=dict(values=[pivot[c] for c in pivot.columns], fill_color='white'))])
        fig.update_layout(title=f"Media {numeric_cols[0]} per {categorical_cols[0]}", height=300)
        grafici.append(('table', fig))
    
    return grafici[:3]  # massimo 3 grafici per non sovraccaricare

# ==================== MAIN ====================
st.sidebar.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
st.sidebar.markdown("## 📁 Carica il tuo file")
uploaded_file = st.sidebar.file_uploader("CSV, Excel o JSON", type=['csv','xlsx','xls','json'])

if uploaded_file is not None:
    with st.spinner("Analisi in corso..."):
        df = load_data(uploaded_file)
        if df is not None and len(df) > 0:
            # Info rapida
            st.success(f"Caricato: {len(df)} righe, {len(df.columns)} colonne")
            
            # Identificazione colonne
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            date_cols = []
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]) or (df[col].dtype == 'object' and df[col].str.match(r'\d{4}-\d{2}-\d{2}').any()):
                    date_cols.append(col)
            
            # KPI intelligenti
            kpis = intelligente_kpi(df, numeric_cols)
            
            # Layout fisso: prima riga KPI, seconda riga filtri+grafici
            # Usiamo colonne per i KPI
            cols_kpi = st.columns(len(kpis))
            for i, (label, value, trend) in enumerate(kpis):
                with cols_kpi[i]:
                    st.markdown(f"""
                    <div class="kpi-card" style="border-top-color: #{['A8E6CF','FFD3B6','C7CEEA','FFAAA5'][i%4]}">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value:,.2f}</div>
                        <div class="kpi-trend">{trend}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Filtri (solo colonne con pochi valori unici)
            st.markdown("---")
            col_filtri, col_grafici = st.columns([1, 3], gap="medium")
            
            with col_filtri:
                st.markdown("### 🔍 Filtri")
                filtro_dict = {}
                # Filtri per colonne categoriche con cardinalità < 30
                for col in categorical_cols:
                    if df[col].nunique() < 30:
                        unique_vals = sorted(df[col].dropna().unique().tolist())
                        selected = st.multiselect(f"{col}", unique_vals, default=unique_vals, key=f"filt_{col}")
                        filtro_dict[col] = selected if selected else unique_vals
                # Filtro date (se presente)
                if date_cols:
                    date_col = date_cols[0]
                    min_date = pd.to_datetime(df[date_col]).min()
                    max_date = pd.to_datetime(df[date_col]).max()
                    start_date, end_date = st.slider("Intervallo date", min_value=min_date, max_value=max_date, value=(min_date, max_date))
                    filtro_dict[date_col] = (start_date, end_date)
            
            # Applica filtri al dataframe
            df_filtered = df.copy()
            for col, vals in filtro_dict.items():
                if col in date_cols:
                    df_filtered = df_filtered[(pd.to_datetime(df_filtered[col]) >= vals[0]) & (pd.to_datetime(df_filtered[col]) <= vals[1])]
                else:
                    df_filtered = df_filtered[df_filtered[col].isin(vals)]
            
            # Ricalcola KPI filtrati (opzionale: aggiornare anche i KPI? Sì, più professionale)
            numeric_cols_f = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
            kpis_filtrati = intelligente_kpi(df_filtered, numeric_cols_f)
            # Mostra KPI filtrati in piccolo (o sostituisci quelli sopra? Per semplicità li mostriamo sotto)
            with col_filtri:
                st.markdown("### 📌 KPI filtrati")
                for label, val, trend in kpis_filtrati[:3]:
                    st.metric(label, f"{val:,.2f}", delta=trend)
            
            # Genera grafici sul dataframe filtrato
            grafici = scegli_grafici(df_filtered, numeric_cols_f, 
                                     [c for c in categorical_cols if c in df_filtered.columns], 
                                     [c for c in date_cols if c in df_filtered.columns])
            
            with col_grafici:
                if grafici:
                    # Mostra primo grafico (principale) grande
                    with st.container():
                        _, _, fig = grafici[0]
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    # Secondo e terzo affiancati
                    if len(grafici) > 1:
                        col2, col3 = st.columns(2)
                        with col2:
                            _, _, fig2 = grafici[1]
                            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
                        if len(grafici) > 2:
                            with col3:
                                _, _, fig3 = grafici[2]
                                st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Nessun grafico generabile con i filtri selezionati.")
            
            # Footer nascosto (non aumenta scroll)
            st.markdown("<p style='text-align:center; color:#A0AEC0; font-size:0.7rem; margin-top:0.5rem;'>🤖 Dashboard intelligente | KPI e grafici adattivi</p>", unsafe_allow_html=True)
        else:
            st.error("Errore: file non valido o vuoto.")
else:
    # Schermata iniziale
    st.markdown("""
    <div style="text-align: center; margin-top: 15%;">
        <h2 style="color: #667eea;">🤖 AI Data Engineer Dashboard</h2>
        <p style="color: #4A5568;">Carica un file CSV, Excel o JSON sulla sidebar sinistra.</p>
        <p style="font-size:0.9rem;">Analisi automatica, KPI intelligenti, grafici adattivi e filtri dinamici.</p>
    </div>
    """, unsafe_allow_html=True)
