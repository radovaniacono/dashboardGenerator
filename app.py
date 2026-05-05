"""
AI Data Engineer Dashboard Generator
Versione 2.0 - Sistema Intelligente di Generazione Dashboard
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
st.set_page_config(page_title="AI Dashboard Generator", page_icon="🤖", layout="wide")

# Header
st.markdown(
    """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
    <h1>🤖 AI Data Engineer Dashboard Generator</h1>
    <p>Carica un file → Analisi automatica → Dashboard interattiva</p>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80
    )
    st.markdown("## 📁 Carica File")

    uploaded_file = st.file_uploader(
        "Scegli un file", type=["csv", "xlsx", "xls", "json"], help="CSV, Excel o JSON"
    )

    st.markdown("---")
    st.markdown("### 🎯 Opzioni")
    show_dashboard = st.checkbox("Mostra Dashboard", value=True)
    show_stats = st.checkbox("Mostra Statistiche", value=True)

    st.markdown("### 💾 Formato Export")
    export_formats = st.multiselect(
        "Scegli i formati di export",
        ["HTML", "PDF", "PNG/JPEG", "Tableau"],
        default=["HTML"],
    )


# Funzione per esportare dashboard in PDF
def export_to_pdf(html_content, filename="dashboard.pdf"):
    """Esporta dashboard in PDF"""
    try:
        import pdfkit

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write(html_content)
            temp_html = f.name

        output_path = filename.replace(".pdf", "") + ".pdf"
        pdfkit.from_file(temp_html, output_path)
        os.unlink(temp_html)
        return output_path
    except ImportError:
        st.warning("⚠️ pdfkit non installato. Usa: pip install pdfkit")
        return None


# Funzione per esportare dashboard in PNG
def export_to_image(html_content, filename="dashboard.png"):
    """Esporta dashboard in PNG usando Plotly"""
    try:
        import plotly.io as pio

        # Converte HTML in immagine tramite kaleido
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write(html_content)
            temp_html = f.name
        return temp_html
    except Exception as e:
        st.warning(f"⚠️ Errore esportazione immagine: {str(e)}")
        return None


# Funzione per creare dataset Tableau
def export_to_tableau(df, filename="data.csv"):
    """Esporta dati in formato CSV pronto per Tableau"""
    csv_buffer = df.to_csv(index=False)
    return csv_buffer.encode()


# Funzione per applicare filtri ai dati
def apply_filters_to_data(df, filters):
    """Applica i filtri selezionati al dataframe"""
    filtered_df = df.copy()

    for filter_col, filter_values in filters.items():
        if filter_col in df.columns and filter_values:
            filtered_df = filtered_df[filtered_df[filter_col].isin(filter_values)]

    return filtered_df


# Funzione per pulire i dati (risolve errore Arrow)
def clean_dataframe(df):
    """Pulisce il dataframe per renderlo compatibile con Arrow"""
    df = df.copy()
    for col in df.columns:
        # Converti colonne object in string
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str)
        # Converti datetime in string se necessario
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d")
        # Converti categorie in string
        elif df[col].dtype.name == "category":
            df[col] = df[col].astype(str)
    return df


# Funzione per caricare dati
@st.cache_data
def load_data(uploaded_file):
    """Carica i dati dal file"""
    file_extension = Path(uploaded_file.name).suffix.lower()

    try:
        if file_extension == ".csv":
            # Prova diverse codifiche
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

        # Pulisci i dati
        df = clean_dataframe(df)
        return df
    except Exception as e:
        st.error(f"Errore: {str(e)}")
        return None


# Funzione per generare dashboard HTML con DashboardGenerator intelligente
def generate_dashboard_html(df):
    """Genera dashboard HTML intelligente con DashboardGenerator"""

    try:
        # Crea analizzatore ML
        ml_analyzer = MLAnalyzer(df)

        # Crea generatore dashboard
        dashboard_gen = DashboardGenerator(df, ml_analyzer, insights=None)

        # Genera KPI cards HTML
        kpi_html = ""
        for kpi in dashboard_gen.kpis:
            kpi_html += f"""
            <div class="kpi-card">
                <div class="kpi-label">{kpi['icon']} {kpi['title']}</div>
                <div class="kpi-value">{kpi['value']}</div>
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
                st.warning(f"⚠️ Errore nel grafico {chart_type}: {str(e)}")
                continue

        # Genera filtri HTML
        filters_html = ""
        if dashboard_gen.suggested_filters:
            filters_html = '<div class="filters-section"><h3>🔍 Filtri Suggeriti</h3><div class="filters-row">'
            for filt in dashboard_gen.suggested_filters:
                filters_html += (
                    f'<div class="filter-chip">{filt["icon"]} {filt["column"]}</div>'
                )
            filters_html += "</div></div>"

        # Template HTML completo
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
                    max-width: 1000px;
                    width: 1000px;
                    margin: 0 auto;
                    box-sizing: border-box;
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
                    font-size: 2rem;
                    margin-bottom: 10px;
                }}
                .header p {{
                    opacity: 0.9;
                    font-size: 1.1rem;
                }}
                .kpi-row {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-bottom: 25px;
                }}
                .kpi-card {{
                    background: white;
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    border-left: 4px solid #667eea;
                    transition: transform 0.2s;
                }}
                .kpi-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                .kpi-label {{
                    font-size: 0.85rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: #666;
                    margin-bottom: 8px;
                }}
                .kpi-value {{
                    font-size: 1.6rem;
                    font-weight: bold;
                    color: #333;
                }}
                .filters-section {{
                    background: white;
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 25px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                }}
                .filters-section h3 {{
                    margin-bottom: 15px;
                    color: #333;
                }}
                .filters-row {{
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }}
                .filter-chip {{
                    background: #A8E6CF;
                    padding: 8px 12px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    color: #333;
                }}
                .charts-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
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
                .chart-info {{
                    font-size: 0.85rem;
                    color: #666;
                    margin-bottom: 10px;
                    font-weight: 500;
                }}
                @media (max-width: 768px) {{
                    .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
                    .charts-grid {{ grid-template-columns: 1fr; }}
                    .header h1 {{ font-size: 1.5rem; }}
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
                
                {filters_html}
                
                <div class="charts-grid">
                    {grafici_html}
                </div>
                
                <div class="footer">
                    <p>🤖 Generato da AI Dashboard Generator v2.0 | Layout: {dashboard_gen.layout_type} | Grafici: {len(dashboard_gen.chart_types)} | {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html_template

    except Exception as e:
        # Fallback se qualcosa va male
        st.error(f"Errore nella generazione intelligente: {str(e)}")
        return f"<h1>Errore: {str(e)}</h1>"


# Main
if uploaded_file is not None:
    with st.spinner("📊 Caricamento e analisi dei dati..."):
        df = load_data(uploaded_file)

        if df is not None and len(df) > 0:
            # Info base
            st.success(f"✅ File caricato: {len(df)} righe, {len(df.columns)} colonne")

            # ========== FILTRI INTERATTIVI ==========
            st.markdown("---")
            st.markdown("### 🔍 Filtri Interattivi")

            filters = {}
            col1, col2 = st.columns(2)

            # Filtri dinamici in base ai dati
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

            # Filtro categorico 1
            if categorical_cols:
                with col1:
                    filter_col_1 = st.selectbox(
                        "🏷️ Filtro 1 - Categoria",
                        [None] + categorical_cols,
                        key="filter_cat_1",
                    )
                    if filter_col_1:
                        filter_values_1 = st.multiselect(
                            f"Seleziona {filter_col_1}",
                            df[filter_col_1].unique(),
                            default=df[filter_col_1].unique()[:5],
                        )
                        if filter_values_1:
                            filters[filter_col_1] = filter_values_1

            # Filtro numerico (range)
            if numeric_cols:
                with col2:
                    filter_col_2 = st.selectbox(
                        "📊 Filtro 2 - Range Numerico",
                        [None] + numeric_cols,
                        key="filter_num_1",
                    )
                    if filter_col_2:
                        min_val = float(df[filter_col_2].min())
                        max_val = float(df[filter_col_2].max())
                        range_vals = st.slider(
                            f"Seleziona range {filter_col_2}",
                            min_val,
                            max_val,
                            (min_val, max_val),
                            key="filter_range_1",
                        )
                        filters[f"{filter_col_2}_range"] = range_vals

            # Applica filtri
            if filters:
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

                st.info(f"📊 Filtri applicati: {len(filtered_df)} righe su {len(df)}")
            else:
                filtered_df = df

            # Statistiche in streamlit (senza errori Arrow)
            if show_stats:
                with st.expander("📋 Anteprima dati", expanded=True):
                    st.dataframe(filtered_df.head(20), use_container_width=True)

                with st.expander("📊 Statistiche descrittive"):
                    numeric_df = filtered_df.select_dtypes(include=[np.number])
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
                    with tempfile.NamedTemporaryFile(
                        mode="w", suffix=".html", delete=False, encoding="utf-8"
                    ) as f:
                        f.write(html_content)
                        temp_path = f.name

                    # Leggi il file
                    with open(temp_path, "r", encoding="utf-8") as f:
                        html_string = f.read()

                    # Mostra usando components (funziona sempre)
                    st.components.v1.html(html_string, height=800, scrolling=True)

                    # Pulisci
                    os.unlink(temp_path)

                    # ========== DOWNLOAD OPTIONS ==========
                    st.markdown("---")
                    st.markdown("### 💾 Scarica Dashboard")

                    col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    # Download HTML
                    with col_dl1:
                        st.download_button(
                            label="📄 HTML",
                            data=html_content,
                            file_name=f"dashboard_{timestamp}.html",
                            mime="text/html",
                        )

                    # Download CSV (dati filtrati)
                    with col_dl2:
                        csv_data = filtered_df.to_csv(index=False)
                        st.download_button(
                            label="📊 CSV (Tableau)",
                            data=csv_data,
                            file_name=f"data_{timestamp}.csv",
                            mime="text/csv",
                        )

                    # Download JSON
                    with col_dl3:
                        json_data = filtered_df.to_json(orient="records")
                        st.download_button(
                            label="🔗 JSON",
                            data=json_data,
                            file_name=f"data_{timestamp}.json",
                            mime="application/json",
                        )

                    # Info Tableau
                    with col_dl4:
                        st.info(
                            "💡 Usa il CSV in Tableau Public (gratuito) per creare dashboard"
                        )

                    # Istruzioni Tableau
                    with st.expander("📚 Come usare con Tableau"):
                        st.markdown("""
                        1. Scarica il file CSV 📊
                        2. Vai su [Tableau Public](https://public.tableau.com)
                        3. Accedi o registrati gratuitamente
                        4. Clicca su "Create" → "New Workbook"
                        5. Carica il file CSV scaricato
                        6. Trascina campi per creare visualizzazioni
                        7. Pubblica il tuo dashboard!
                        """)

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
st.markdown(
    "<p style='text-align: center; color: gray;'>🤖 AI Data Engineer Dashboard Generator</p>",
    unsafe_allow_html=True,
)
