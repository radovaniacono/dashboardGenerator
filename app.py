"""
AI Data Engineer Dashboard Generator
Versione Definitiva - Senza Errori
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import base64

# Configurazione pagina
st.set_page_config(
    page_title="AI Dashboard Generator",
    page_icon="🤖",
    layout="wide"
)

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
    <h1>🤖 AI Data Engineer Dashboard Generator</h1>
    <p>Carica un file → Analisi automatica → Dashboard interattiva</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
    st.markdown("## 📁 Carica File")
    
    uploaded_file = st.file_uploader(
        "Scegli un file",
        type=['csv', 'xlsx', 'xls', 'json'],
        help="CSV, Excel o JSON"
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Opzioni")
    show_dashboard = st.checkbox("Mostra Dashboard", value=True)
    show_stats = st.checkbox("Mostra Statistiche", value=True)

# Funzione per pulire i dati (risolve errore Arrow)
def clean_dataframe(df):
    """Pulisce il dataframe per renderlo compatibile con Arrow"""
    df = df.copy()
    for col in df.columns:
        # Converti colonne object in string
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('').astype(str)
        # Converti datetime in string se necessario
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')
        # Converti categorie in string
        elif df[col].dtype.name == 'category':
            df[col] = df[col].astype(str)
    return df

# Funzione per caricare dati
@st.cache_data
def load_data(uploaded_file):
    """Carica i dati dal file"""
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    try:
        if file_extension == '.csv':
            # Prova diverse codifiche
            for encoding in ['utf-8', 'latin1', 'iso-8859-1']:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    break
                except:
                    continue
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        elif file_extension == '.json':
            df = pd.read_json(uploaded_file)
        else:
            return None
        
        # Pulisci i dati
        df = clean_dataframe(df)
        return df
    except Exception as e:
        st.error(f"Errore: {str(e)}")
        return None

# Funzione per generare dashboard HTML
def generate_dashboard_html(df):
    """Genera dashboard HTML con grafici"""
    
    # Identifica tipi di colonne
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Colori pastello
    colors = ['#A8E6CF', '#FFD3B6', '#FFAAA5', '#C7CEEA', '#B5EAD7', '#FFDAC1', '#D4F1F9', '#E8D0F0']
    
    grafici_html = ""
    chart_counter = 0
    
    # Grafico 1: Istogramma (se ci sono dati numerici)
    if numeric_cols:
        col = numeric_cols[0]
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[col].dropna(),
            nbinsx=20,
            marker_color=colors[0],
            marker_line_color='white',
            marker_line_width=1,
            opacity=0.85
        ))
        fig.update_layout(
            title=f"📊 Distribuzione {col}",
            xaxis_title=col,
            yaxis_title="Frequenza",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40)
        )
        grafici_html += f"""
        <div class="chart-card">
            <div id="chart_{chart_counter}" style="width:100%; height:350px;"></div>
        </div>
        <script>
            var fig_{chart_counter} = {fig.to_json()};
            Plotly.newPlot('chart_{chart_counter}', fig_{chart_counter}.data, fig_{chart_counter}.layout);
        </script>
        """
        chart_counter += 1
    
    # Grafico 2: Bar chart (se ci sono dati categorici)
    if categorical_cols:
        col = categorical_cols[0]
        counts = df[col].value_counts().head(10)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=counts.index.tolist(),
            y=counts.values.tolist(),
            marker_color=colors[1],
            text=counts.values.tolist(),
            textposition='outside'
        ))
        fig.update_layout(
            title=f"📈 Top 10 {col}",
            xaxis_title=col,
            yaxis_title="Conteggio",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            xaxis_tickangle=-45 if len(counts) > 5 else 0
        )
        grafici_html += f"""
        <div class="chart-card">
            <div id="chart_{chart_counter}" style="width:100%; height:350px;"></div>
        </div>
        <script>
            var fig_{chart_counter} = {fig.to_json()};
            Plotly.newPlot('chart_{chart_counter}', fig_{chart_counter}.data, fig_{chart_counter}.layout);
        </script>
        """
        chart_counter += 1
    
    # Grafico 3: Scatter plot (se ci sono almeno 2 metriche)
    if len(numeric_cols) >= 2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[numeric_cols[0]],
            y=df[numeric_cols[1]],
            mode='markers',
            marker=dict(size=8, color=colors[2], opacity=0.6, line=dict(width=1, color='white'))
        ))
        fig.update_layout(
            title=f"🔍 {numeric_cols[0]} vs {numeric_cols[1]}",
            xaxis_title=numeric_cols[0],
            yaxis_title=numeric_cols[1],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40)
        )
        grafici_html += f"""
        <div class="chart-card">
            <div id="chart_{chart_counter}" style="width:100%; height:350px;"></div>
        </div>
        <script>
            var fig_{chart_counter} = {fig.to_json()};
            Plotly.newPlot('chart_{chart_counter}', fig_{chart_counter}.data, fig_{chart_counter}.layout);
        </script>
        """
        chart_counter += 1
    
    # Grafico 4: Box plot
    if numeric_cols:
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=df[numeric_cols[0]].dropna(),
            name=numeric_cols[0],
            marker_color=colors[3],
            line_color=colors[3],
            boxmean='sd'
        ))
        fig.update_layout(
            title=f"📦 Distribuzione {numeric_cols[0]}",
            yaxis_title=numeric_cols[0],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40)
        )
        grafici_html += f"""
        <div class="chart-card">
            <div id="chart_{chart_counter}" style="width:100%; height:350px;"></div>
        </div>
        <script>
            var fig_{chart_counter} = {fig.to_json()};
            Plotly.newPlot('chart_{chart_counter}', fig_{chart_counter}.data, fig_{chart_counter}.layout);
        </script>
        """
        chart_counter += 1
    
    # Heatmap correlazioni (se abbastanza colonne numeriche)
    if len(numeric_cols) >= 3:
        corr = df[numeric_cols].corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.columns.tolist(),
            colorscale='Pastel',
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        fig.update_layout(
            title="🔗 Matrice di Correlazione",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=80, r=20, t=50, b=80),
            xaxis_tickangle=45
        )
        grafici_html += f"""
        <div class="chart-card">
            <div id="chart_{chart_counter}" style="width:100%; height:400px;"></div>
        </div>
        <script>
            var fig_{chart_counter} = {fig.to_json()};
            Plotly.newPlot('chart_{chart_counter}', fig_{chart_counter}.data, fig_{chart_counter}.layout);
        </script>
        """
        chart_counter += 1
    
    # Genera KPI cards
    kpi_html = ""
    for i, col in enumerate(numeric_cols[:6]):
        media = df[col].mean()
        if pd.notna(media):
            kpi_html += f"""
            <div class="kpi-card">
                <div class="kpi-label">{col.upper()}</div>
                <div class="kpi-value">{media:,.2f}</div>
                <div class="kpi-trend">Media</div>
            </div>
            """
    
    # Template HTML completo
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard Interattiva</title>
        <script src="https://cdn.plot.ly/plotly-3.0.1.min.js"></script>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                background: #F9FBF4;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 20px;
            }}
            .dashboard {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 20px;
                padding: 30px;
                color: white;
                text-align: center;
                margin-bottom: 25px;
            }}
            .header h1 {{
                font-size: 1.8rem;
                margin-bottom: 10px;
            }}
            .header p {{
                opacity: 0.9;
            }}
            .kpi-row {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin-bottom: 25px;
            }}
            .kpi-card {{
                background: white;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                border-top: 3px solid #667eea;
            }}
            .kpi-label {{
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: #666;
                margin-bottom: 8px;
            }}
            .kpi-value {{
                font-size: 1.8rem;
                font-weight: bold;
                color: #333;
            }}
            .kpi-trend {{
                font-size: 0.7rem;
                color: #999;
                margin-top: 5px;
            }}
            .charts-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }}
            .chart-card {{
                background: white;
                border-radius: 15px;
                padding: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                transition: transform 0.2s;
            }}
            .chart-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                color: #999;
                font-size: 0.8rem;
            }}
            @media (max-width: 768px) {{
                .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
                .charts-grid {{ grid-template-columns: 1fr; }}
                .header h1 {{ font-size: 1.2rem; }}
            }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <h1>📊 Pastel Interactive Dashboard</h1>
                <p>Dashboard generata automaticamente dai tuoi dati</p>
            </div>
            
            <div class="kpi-row">
                {kpi_html}
            </div>
            
            <div class="charts-grid">
                {grafici_html}
            </div>
            
            <div class="footer">
                <p>🤖 Generato da AI Data Engineer | {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

# Main
if uploaded_file is not None:
    with st.spinner("📊 Caricamento e analisi dei dati..."):
        df = load_data(uploaded_file)
        
        if df is not None and len(df) > 0:
            # Info base
            st.success(f"✅ File caricato: {len(df)} righe, {len(df.columns)} colonne")
            
            # Statistiche in streamlit (senza errori Arrow)
            if show_stats:
                with st.expander("📋 Anteprima dati", expanded=True):
                    st.dataframe(df.head(20), use_container_width=True)
                
                with st.expander("📊 Statistiche descrittive"):
                    numeric_df = df.select_dtypes(include=[np.number])
                    if len(numeric_df.columns) > 0:
                        st.dataframe(numeric_df.describe(), use_container_width=True)
                    else:
                        st.info("Nessuna colonna numerica trovata")
            
            # Dashboard HTML
            if show_dashboard:
                st.markdown("---")
                st.subheader("📊 Dashboard Interattiva")
                
                try:
                    # Genera dashboard HTML
                    html_content = generate_dashboard_html(df)
                    
                    # Salva in file temporaneo
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                        f.write(html_content)
                        temp_path = f.name
                    
                    # Leggi il file
                    with open(temp_path, 'r', encoding='utf-8') as f:
                        html_string = f.read()
                    
                    # Mostra usando components (funziona sempre)
                    st.components.v1.html(html_string, height=800, scrolling=True)
                    
                    # Pulisci
                    os.unlink(temp_path)
                    
                    # Download button
                    st.download_button(
                        label="💾 Scarica Dashboard HTML",
                        data=html_content,
                        file_name=f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
                    
                except Exception as e:
                    st.error(f"Errore generazione dashboard: {str(e)}")
                    st.info("Prova con un file che contiene più dati numerici")
        else:
            st.error("Errore nel caricamento del file")
else:
    # Messaggio iniziale
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👈 **Carica un file CSV, Excel o JSON per iniziare**")
        st.markdown("""
        ### 📌 Esempi di dati che funzionano bene:
        - Vendite (date, prodotto, quantità, prezzo)
        - Clienti (età, città, spesa, acquisti)
        - Marketing (click, impressioni, conversioni)
        - Finanza (entrate, uscite, profitto)
        """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🤖 AI Data Engineer Dashboard Generator</p>", unsafe_allow_html=True) 
