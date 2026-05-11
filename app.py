"""
AI Data Engineer Dashboard Generator - Versione 3.0
Sistema Intelligente di Generazione Dashboard con Analisi ML Avanzata
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
import sys
from plotly.utils import PlotlyJSONEncoder
import json

# Importa le classi custom
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from ml_analyzer import MLAnalyzer
from dashboard_generator import DashboardGenerator

# Configurazione pagina
st.set_page_config(
    page_title="AI Dashboard Generator v3.0",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizzato per un design moderno
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .insight-box {
        background: #f0f8ff;
        padding: 1rem;
        border-left: 4px solid #4169e1;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header principale
st.markdown(
    """
<div class="main-header">
    <h1>🤖 AI Data Engineer Dashboard Generator</h1>
    <p><strong>v3.0</strong> - Carica → Analizza → Visualizza con AI</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">Sistema intelligente di rilevamento dati, KPI dinamici e raccomandazioni grafiche</p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# SIDEBAR - Caricamento file e opzioni
# ============================================================================
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80
    )
    st.markdown("## 📁 Carica Dati")

    uploaded_file = st.file_uploader(
        "Scegli un file",
        type=["csv", "xlsx", "xls", "json"],
        help="Formati supportati: CSV, Excel (xlsx/xls), JSON",
    )

    st.markdown("---")
    st.markdown("### 🎯 Opzioni Visualizzazione")
    show_insights = st.checkbox("📊 Mostra Analisi ML", value=True)
    show_kpis = st.checkbox("💰 Mostra KPI", value=True)
    show_dashboard = st.checkbox("📈 Mostra Dashboard", value=True)
    show_tables = st.checkbox("📋 Mostra Tabelle", value=True)
    show_stats = st.checkbox("📉 Mostra Statistiche", value=False)

    st.markdown("---")
    st.markdown("### 💾 Formato Export")
    export_formats = st.multiselect(
        "Scegli formati di export", ["HTML", "CSV", "JSON"], default=["HTML"]
    )

# ============================================================================
# FUNZIONI UTILITY
# ============================================================================


def clean_dataframe(df):
    """Pulisce il dataframe per compatibilità Arrow"""
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d")
        elif df[col].dtype.name == "category":
            df[col] = df[col].astype(str)
    return df


@st.cache_data
def load_data(uploaded_file):
    """Carica i dati dal file con gestione errori"""
    file_extension = Path(uploaded_file.name).suffix.lower()

    try:
        if file_extension == ".csv":
            for encoding in ["utf-8", "latin1", "iso-8859-1"]:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    break
                except:
                    continue
        elif file_extension in [".xlsx", ".xls"]:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif file_extension == ".json":
            df = pd.read_json(uploaded_file)
        else:
            return None

        df = clean_dataframe(df)
        return df
    except Exception as e:
        st.error(f"❌ Errore caricamento: {str(e)}")
        return None


def display_ml_insights(ml_analyzer):
    """Mostra gli insights ottenuti dall'analisi ML"""
    st.markdown("---")
    st.subheader("🔍 Analisi Intelligente dei Dati")

    profile = ml_analyzer.analyze_data_profile()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📊 Shape Dataset",
            f"{profile['shape'][0]} × {profile['shape'][1]}",
            "righe × colonne",
        )

    with col2:
        quality = profile.get("missing_percentage", {})
        avg_missing = np.mean(list(quality.values())) if quality else 0
        st.metric("🛡️ Completezza Media", f"{100 - avg_missing:.1f}%", "dati non nulli")

    with col3:
        st.metric(
            "🔢 Metriche Numeriche", len(ml_analyzer.numeric_cols), "colonne numeriche"
        )

    # Mostra problemi di qualità
    issues = profile.get("data_quality_issues", [])
    if issues:
        st.markdown("### ⚠️ Problemi di Qualità Dati")
        for issue in issues[:3]:
            severity_icon = "🔴" if issue.get("severity") == "high" else "🟡"
            st.warning(
                f"{severity_icon} {issue.get('message', 'Problema sconosciuto')}"
            )

    # Mostra correlazioni forti
    strong_corr = profile.get("strong_correlations", [])
    if strong_corr:
        st.markdown("### 📈 Correlazioni Rilevate")
        for corr in strong_corr[:3]:
            st.info(
                f"🔗 **{corr['var1']}** ↔ **{corr['var2']}** (r = {corr['correlation']:.2f})"
            )

    # Mostra tipi di dati rilevati
    st.markdown("### 🏷️ Tipi di Dati Rilevati")
    col1, col2, col3 = st.columns(3)

    with col1:
        if ml_analyzer.monetary_cols:
            st.success(f"💰 Monetarie: {', '.join(ml_analyzer.monetary_cols[:2])}")

    with col2:
        if ml_analyzer.percentage_cols:
            st.info(f"📊 Percentuali: {', '.join(ml_analyzer.percentage_cols[:2])}")

    with col3:
        if ml_analyzer.datetime_cols:
            st.success(f"📅 Temporali: {', '.join(ml_analyzer.datetime_cols[:2])}")


def display_smart_tables(df, ml_analyzer):
    """Mostra tabelle intelligenti - summary e dettagli"""
    st.markdown("---")
    st.subheader("📋 Tabelle Intelligenti")

    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Dettagli Completi", "📈 Statistiche"])

    with tab1:
        st.markdown("#### Anteprima Dati (Prime 10 righe)")
        st.dataframe(df.head(10), use_container_width=True)

        st.markdown("#### Statistiche Descrittive")
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 0:
            st.dataframe(numeric_df.describe(), use_container_width=True)

    with tab2:
        st.markdown("#### Dataset Completo (Esplorabile)")
        st.dataframe(df, use_container_width=True)

    with tab3:
        st.markdown("#### Profilo Dati")
        profile = ml_analyzer.analyze_data_profile()

        # Cardinalità
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Colonne e Cardinalità")
            card_df = pd.DataFrame(
                {
                    "Colonna": list(profile["unique_counts"].keys()),
                    "Valori Unici": list(profile["unique_counts"].values()),
                    "Tipo": [
                        str(profile["data_types"].get(c, "Unknown"))
                        for c in profile["unique_counts"].keys()
                    ],
                }
            )
            st.dataframe(card_df, use_container_width=True)

        with col2:
            st.markdown("##### Dati Mancanti (%)")
            missing_df = pd.DataFrame(
                {
                    "Colonna": list(profile["missing_percentage"].keys()),
                    "Missing %": [
                        f"{v:.1f}%" for v in profile["missing_percentage"].values()
                    ],
                }
            )
            st.dataframe(missing_df, use_container_width=True)


def generate_dashboard_html(df, ml_analyzer):
    """Genera dashboard HTML intelligente con DashboardGenerator"""
    try:
        # Crea generatore dashboard
        dashboard_gen = DashboardGenerator(df, ml_analyzer, insights=None)

        # Genera KPI cards HTML
        kpi_html = ""
        for kpi in dashboard_gen.kpis:
            kpi_html += f"""
            <div class="kpi-card">
                <div class="kpi-label">{kpi['icon']} {kpi['title']}</div>
                <div class="kpi-value">{kpi['value']}</div>
                <div class="kpi-trend" style="font-size: 0.85rem; color: #666;">{kpi.get('trend', '')}</div>
            </div>
            """

        # Genera grafici dinamicamente
        grafici_html = ""
        chart_functions = {
            "line": dashboard_gen.create_line_chart,
            "bar": dashboard_gen.create_bar_chart,
            "scatter": dashboard_gen.create_scatter_chart,
            "bubble": dashboard_gen.create_bubble_chart,
            "heatmap": dashboard_gen.create_heatmap_chart,
            "histogram": dashboard_gen.create_histogram_chart,
            "boxplot": dashboard_gen.create_boxplot_chart,
            "treemap": dashboard_gen.create_treemap_chart,
            "radar": dashboard_gen.create_radar_chart,
            "violin": dashboard_gen.create_violin_chart,
            "area": dashboard_gen.create_area_chart,
            "pie": dashboard_gen.create_pie_chart,
        }

        chart_counter = 0
        for idx, chart_type in enumerate(dashboard_gen.chart_types):
            try:
                if chart_type in chart_functions:
                    fig = chart_functions[chart_type](idx)
                    fig_json = json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder)
                    icon = dashboard_gen.get_chart_icon(chart_type)

                    grafici_html += f"""
                    <div class="chart-card">
                        <div id="chart_{chart_counter}" style="width:100%; height:350px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_{chart_counter} = {fig_json};
                            Plotly.newPlot('chart_{chart_counter}', fig_{chart_counter}.data, fig_{chart_counter}.layout, {{responsive: true}});
                        }})();
                    </script>
                    """
                    chart_counter += 1
            except Exception as e:
                st.warning(f"⚠️ Errore grafico {chart_type}: {str(e)}")
                continue

        # Template HTML completo moderno
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard Interattiva - AI Generated</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
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
                    max-width: 1200px;
                    margin: 0 auto;
                    box-sizing: border-box;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 15px;
                    padding: 40px;
                    color: white;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                }}
                .header p {{
                    opacity: 0.9;
                    font-size: 1.1rem;
                }}
                .kpi-row {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 15px;
                    margin-bottom: 30px;
                }}
                .kpi-card {{
                    background: white;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    border-left: 5px solid #667eea;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }}
                .kpi-card:hover {{
                    transform: translateY(-4px);
                    box-shadow: 0 6px 16px rgba(0,0,0,0.12);
                }}
                .kpi-label {{
                    font-size: 0.85rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: #666;
                    margin-bottom: 10px;
                }}
                .kpi-value {{
                    font-size: 1.8rem;
                    font-weight: bold;
                    color: #333;
                }}
                .charts-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .chart-card {{
                    background: white;
                    border-radius: 12px;
                    padding: 15px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    transition: transform 0.2s;
                }}
                .chart-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding: 20px;
                    color: #999;
                    font-size: 0.8rem;
                    border-top: 1px solid #eee;
                }}
                @media (max-width: 768px) {{
                    .charts-grid {{ grid-template-columns: 1fr; }}
                    .header h1 {{ font-size: 1.8rem; }}
                }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1>📊 Dashboard Interattiva Intelligente</h1>
                    <p>✨ Generata automaticamente con AI Data Engineering</p>
                </div>
                
                <div class="kpi-row">
                    {kpi_html}
                </div>
                
                <div class="charts-grid">
                    {grafici_html}
                </div>
                
                <div class="footer">
                    <p>🤖 Generato da AI Dashboard Generator v3.0 | {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html_template

    except Exception as e:
        st.error(f"❌ Errore nella generazione dashboard: {str(e)}")
        return f"<h1>Errore: {str(e)}</h1>"


# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================

if uploaded_file is not None:
    with st.spinner("🔄 Caricamento e analisi dei dati..."):
        df = load_data(uploaded_file)

        if df is not None and len(df) > 0:
            st.success(
                f"✅ File caricato: **{len(df):,}** righe, **{len(df.columns)}** colonne"
            )

            # Inizializza ML Analyzer
            ml_analyzer = MLAnalyzer(df)

            # ================================================================
            # SEZIONE INSIGHTS ML
            # ================================================================
            if show_insights:
                display_ml_insights(ml_analyzer)

            # ================================================================
            # SEZIONE FILTRI INTERATTIVI
            # ================================================================
            st.markdown("---")
            st.subheader("🔍 Filtri Interattivi")

            filters = {}
            col1, col2, col3 = st.columns(3)

            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

            # Filtro categorico
            with col1:
                if categorical_cols:
                    filter_col_1 = st.selectbox(
                        "🏷️ Filtro Categoria",
                        [None] + categorical_cols,
                        key="filter_cat_1",
                    )
                    if filter_col_1:
                        filter_values_1 = st.multiselect(
                            f"Seleziona {filter_col_1}",
                            df[filter_col_1].unique(),
                            default=df[filter_col_1].unique()[:5],
                            key="filter_values_1",
                        )
                        if filter_values_1:
                            filters[filter_col_1] = filter_values_1

            # Filtro numerico (range)
            with col2:
                if numeric_cols:
                    filter_col_2 = st.selectbox(
                        "📊 Filtro Range Numerico",
                        [None] + numeric_cols,
                        key="filter_num_1",
                    )
                    if filter_col_2:
                        min_val = float(df[filter_col_2].min())
                        max_val = float(df[filter_col_2].max())
                        range_vals = st.slider(
                            f"Range {filter_col_2}",
                            min_val,
                            max_val,
                            (min_val, max_val),
                            key="filter_range_1",
                        )
                        filters[f"{filter_col_2}_range"] = range_vals

            # Bottone reset filtri
            with col3:
                if st.button("🔄 Reset Filtri", key="reset_filters"):
                    filters = {}
                    st.rerun()

            # Applica filtri
            filtered_df = df.copy()

            # Applica filtri categorici
            for col, values in filters.items():
                if col in df.columns:
                    filtered_df = filtered_df[filtered_df[col].isin(values)]

            # Applica filtri numerici
            for key, (min_v, max_v) in filters.items():
                if "_range" in key:
                    col_name = key.replace("_range", "")
                    if col_name in df.columns:
                        filtered_df = filtered_df[
                            (filtered_df[col_name] >= min_v)
                            & (filtered_df[col_name] <= max_v)
                        ]

            if filters:
                st.info(
                    f"✅ Filtri applicati: **{len(filtered_df):,}** righe su **{len(df):,}** ({len(filtered_df)/len(df)*100:.1f}%)"
                )
            else:
                filtered_df = df

            # ================================================================
            # SEZIONE KPI
            # ================================================================
            if show_kpis:
                st.markdown("---")
                st.subheader("💰 Key Performance Indicators")

                ml_analyzer_filtered = MLAnalyzer(filtered_df)
                dashboard_gen = DashboardGenerator(
                    filtered_df, ml_analyzer_filtered, None
                )

                cols = st.columns(len(dashboard_gen.kpis))
                for i, kpi in enumerate(dashboard_gen.kpis):
                    with cols[i % len(cols)]:
                        st.metric(
                            label=f"{kpi['icon']} {kpi['title']}",
                            value=kpi["value"],
                            delta=kpi.get("trend", ""),
                        )

            # ================================================================
            # SEZIONE TABELLE
            # ================================================================
            if show_tables:
                display_smart_tables(filtered_df, ml_analyzer_filtered)

            # ================================================================
            # SEZIONE DASHBOARD HTML
            # ================================================================
            if show_dashboard:
                st.markdown("---")
                st.subheader("📊 Dashboard Interattiva")

                try:
                    html_content = generate_dashboard_html(
                        filtered_df, ml_analyzer_filtered
                    )

                    with tempfile.NamedTemporaryFile(
                        mode="w", suffix=".html", delete=False, encoding="utf-8"
                    ) as f:
                        f.write(html_content)
                        temp_path = f.name

                    with open(temp_path, "r", encoding="utf-8") as f:
                        html_string = f.read()

                    st.components.v1.html(html_string, height=900, scrolling=True)

                    os.unlink(temp_path)

                    # ========== DOWNLOAD OPTIONS ==========
                    st.markdown("---")
                    st.markdown("### 💾 Scarica Risultati")

                    col_dl1, col_dl2, col_dl3 = st.columns(3)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    # Download HTML
                    with col_dl1:
                        st.download_button(
                            label="📄 Scarica Dashboard (HTML)",
                            data=html_content,
                            file_name=f"dashboard_{timestamp}.html",
                            mime="text/html",
                        )

                    # Download CSV
                    with col_dl2:
                        csv_data = filtered_df.to_csv(index=False)
                        st.download_button(
                            label="📊 Scarica Dati (CSV)",
                            data=csv_data,
                            file_name=f"data_{timestamp}.csv",
                            mime="text/csv",
                        )

                    # Download JSON
                    with col_dl3:
                        json_data = filtered_df.to_json(orient="records")
                        st.download_button(
                            label="🔗 Scarica Dati (JSON)",
                            data=json_data,
                            file_name=f"data_{timestamp}.json",
                            mime="application/json",
                        )

                except Exception as e:
                    st.error(f"❌ Errore generazione dashboard: {str(e)}")

        else:
            st.error("❌ Errore nel caricamento del file")
else:
    # Messaggio iniziale
    st.markdown("""
    ## 👈 Carica un File per Iniziare

    Questa applicazione genera automaticamente:
    
    - 📊 **Dashboard interattive** con grafici intelligenti
    - 💰 **KPI dinamici** rilevati automaticamente dai dati
    - 🔍 **Analisi ML** per qualità, correlazioni e anomalie
    - 📋 **Tabelle intelligenti** con statistiche descrittive
    - 📈 **Visualizzazioni ottimizzate** per il tuo dataset
    
    ### 📌 Esempi di Dati Supportati:
    - **Vendite**: date, prodotto, quantità, prezzo, regione
    - **Clienti**: età, città, spesa, numero acquisti
    - **Marketing**: click, impressioni, conversioni, costo
    - **Finanza**: entrate, uscite, profitto, margine
    - **Operazioni**: KPI, metriche, target, status
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.85rem;'>🤖 AI Data Engineer Dashboard Generator v3.0 | Powered by ML & Streamlit</p>",
    unsafe_allow_html=True,
)
