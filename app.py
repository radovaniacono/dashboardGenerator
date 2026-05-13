"""
AI Data Engineer Dashboard Generator - Versione 4.0
Sistema Intelligente di Generazione Dashboard con Layout Responsivo, Dinamico e Accessibile
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import os
from datetime import datetime
import sys
import tempfile

# Importa moduli custom
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ml_analyzer import MLAnalyzer
from dashboard_generator import DashboardGenerator
from responsive_layout import ResponsiveLayoutEngine, create_responsive_columns
from layout_randomizer import (
    LayoutRandomizer,
    AdvancedLayoutRandomizer,
    LayoutBalancer,
    LayoutMemory,
    create_dynamic_kpi_grid,
    create_dynamic_chart_grid,
)
from kpi_cards import (
    KPICard,
    render_kpi_grid,
    create_kpi_from_metric,
    render_kpi_summary,
)
from kpi_calculator import KPICalculator, KPI
from charts_intelligent import (
    IntelligentChartBuilder,
    get_chart_candidates,
    render_intelligent_chart,
)
from tables_interactive import InteractiveTable, render_table_with_filters
from filter_system import GlobalFilterManager, FilterBar
from accessibility import AccessibilityManager, add_skip_link, ColorAccessibility
from error_handler import DashboardErrorHandler, ErrorMessageFormatter
from tableau_documentation_generator import TableauDocumentationGenerator

# ============================================================================
# CONFIGURAZIONE PAGINA E TEMA
# ============================================================================

st.set_page_config(
    page_title="AI Dashboard Generator v4.0",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Layout engine responsivo
layout_engine = ResponsiveLayoutEngine()
layout_engine.render_responsive_css()

# Accessibility manager
a11y_manager = AccessibilityManager()

# ============================================================================
# HEADER PRINCIPALE
# ============================================================================

st.markdown(
    """
    <div class="main-header" style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <h1>🤖 AI Data Engineer Dashboard Generator</h1>
        <p><strong>v4.0</strong> - Dashboard Responsiva, Dinamica e Accessibile</p>
        <p style="font-size: 0.9rem; opacity: 0.9;">
            Carica → Analizza → Visualizza con AI + Layout Intelligente
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# SIDEBAR - CONTROLLI PRINCIPALI
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
    st.markdown("### 🎯 Visualizzazione")
    show_insights = st.checkbox("📊 Analisi ML", value=True)
    show_filters = st.checkbox("🔍 Filtri Globali", value=True)
    show_kpis = st.checkbox("💰 KPI Dinamici", value=True)
    show_charts = st.checkbox("📈 Grafici", value=True)
    show_tables = st.checkbox("📋 Tabelle", value=True)

    st.markdown("---")
    st.markdown("### 🎨 Layout")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Layout"):
            st.session_state["layout_seed"] = None
            st.rerun()
    with col2:
        if st.button("💾 Export All"):
            st.info("Feature disponibile nella sezione export")

    # Accessibilità
    a11y_manager.render_accessibility_controls()
    a11y_manager.apply_accessibility_css()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def clean_dataframe(df):
    """Pulisce il dataframe per compatibilità"""
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                df[col] = df[col].dt.strftime("%Y-%m-%d")
            except:
                pass
        elif df[col].dtype.name == "category":
            df[col] = df[col].astype(str)
    return df


@st.cache_data
def load_data_with_validation(uploaded_file):
    """
    Carica i dati dal file con validazione e correzione automatica

    Returns:
        Tuple: (is_valid: bool, df: pd.DataFrame, corrections: List[str])
    """
    error_handler = DashboardErrorHandler()

    # Salva file temporaneamente
    temp_path = tempfile.NamedTemporaryFile(
        delete=False, suffix=Path(uploaded_file.name).suffix
    ).name
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Valida e ripara
    is_valid, df, corrections = error_handler.validate_and_repair_file(temp_path)

    # Pulisci temp file
    try:
        os.remove(temp_path)
    except:
        pass

    if is_valid and df is not None:
        df = clean_dataframe(df)

    return is_valid, df, corrections


@st.cache_data
def load_data(uploaded_file):
    """Carica i dati dal file (compatibilità)"""
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


# ============================================================================
# MAIN APPLICATION
# ============================================================================

if uploaded_file is not None:
    with st.spinner("🔄 Caricamento, validazione e analisi dati..."):
        # Step 1: Carica con validazione e correzione automatica
        is_valid, df, corrections = load_data_with_validation(uploaded_file)

        if is_valid and df is not None and len(df) > 0:
            # Mostra correzioni applicate se presenti
            if corrections:
                with st.expander("⚙️ Correzioni Automatiche Applicate", expanded=False):
                    for correction in corrections:
                        if "✅" in correction:
                            st.success(correction)
                        elif "⚠️" in correction:
                            st.warning(correction)
                        else:
                            st.info(correction)

            st.success(
                f"✅ File caricato: **{len(df):,}** righe × **{len(df.columns)}** colonne"
            )

            # Inizializza ML Analyzer
            ml_analyzer = MLAnalyzer(df)

            # Inizializza KPI Calculator
            kpi_calculator = KPICalculator(df, ml_analyzer)

            # ================================================================
            # SEZIONE 1: INSIGHTS ML
            # ================================================================
            if show_insights:
                st.markdown("---")
                st.subheader("🔍 Analisi Intelligente dei Dati")

                profile = ml_analyzer.analyze_data_profile()

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "📊 Shape",
                        f"{profile['shape'][0]} × {profile['shape'][1]}",
                        help="Righe × Colonne",
                    )

                with col2:
                    quality = profile.get("missing_percentage", {})
                    avg_missing = np.mean(list(quality.values())) if quality else 0
                    st.metric("🛡️ Completezza", f"{100-avg_missing:.1f}%")

                with col3:
                    numeric_count = (
                        len(ml_analyzer.numeric_cols)
                        if hasattr(ml_analyzer, "numeric_cols")
                        else 0
                    )
                    st.metric("🔢 Colonne Numeriche", numeric_count)

                # Problemi qualità
                issues = profile.get("data_quality_issues", [])
                if issues:
                    with st.expander("⚠️ Problemi di Qualità"):
                        for issue in issues[:5]:
                            severity = "🔴" if issue.get("severity") == "high" else "🟡"
                            st.warning(f"{severity} {issue.get('message', 'Problema')}")

                # Correlazioni
                strong_corr = profile.get("strong_correlations", [])
                if strong_corr:
                    with st.expander("📈 Correlazioni Forti"):
                        for corr in strong_corr[:5]:
                            st.info(
                                f"🔗 **{corr['var1']}** ↔ **{corr['var2']}** (r = {corr['correlation']:.2f})"
                            )

            # ================================================================
            # SEZIONE 2: FILTRI GLOBALI
            # ================================================================
            if show_filters:
                filter_bar = FilterBar(df)
                filter_bar.render()

                # Applica filtri
                filtered_df = filter_bar.apply_to_dataframe(df)

                if filter_bar.manager.has_active_filters():
                    st.info(
                        f"📊 Filtri attivi: **{len(filtered_df):,}** di **{len(df):,}** righe "
                        f"({len(filtered_df)/len(df)*100:.1f}%)"
                    )
                    filter_bar.show_active_filters()
            else:
                filtered_df = df

            # Reinizializza analyzer e calculator con dati filtrati
            ml_analyzer_filtered = MLAnalyzer(filtered_df)
            kpi_calculator_filtered = KPICalculator(filtered_df, ml_analyzer_filtered)

            # ================================================================
            # SEZIONE 3: KPI DINAMICI (NUOVI - INTELLIGENTI)
            # ================================================================
            if show_kpis:
                st.markdown("---")
                st.subheader("💰 Key Performance Indicators Intelligenti")

                try:
                    # Calcola KPI automaticamente
                    kpis = kpi_calculator_filtered.calculate_all_kpis(max_kpis=8)

                    # Ottieni data quality assessment
                    quality = kpi_calculator_filtered._assess_data_quality()

                    # Mostra qualità dati
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(
                            "📊 Completezza", f"{quality['completeness_pct']:.1f}%"
                        )
                    with col2:
                        st.metric("📝 Righe", quality["total_rows"])
                    with col3:
                        st.metric("📌 Colonne", quality["total_columns"])
                    with col4:
                        st.metric("🔢 Numeriche", quality["numeric_columns"])

                    # Renderizza KPI Cards
                    if kpis:
                        num_cols = layout_engine.get_kpi_columns()
                        cols = st.columns(num_cols)

                        for idx, kpi in enumerate(kpis):
                            col_idx = idx % num_cols

                            with cols[col_idx]:
                                # Determina colore basato su trend
                                if kpi.trend_direction == "up":
                                    color = "🟢"
                                elif kpi.trend_direction == "down":
                                    color = "🔴"
                                else:
                                    color = "⚪"

                                # Crea card con border colorato
                                border_color = (
                                    "#10b981"
                                    if kpi.trend_direction == "up"
                                    else (
                                        "#ef4444"
                                        if kpi.trend_direction == "down"
                                        else "#667eea"
                                    )
                                )

                                st.markdown(
                                    f"""
                                    <div style="
                                        border-left: 4px solid {border_color};
                                        padding: 1rem;
                                        background: #f8f9fa;
                                        border-radius: 8px;
                                        margin-bottom: 0.5rem;
                                    ">
                                        <p style="margin: 0; color: #6b7280; font-size: 0.875rem; font-weight: 500;">
                                            {kpi.icon} {kpi.name}
                                        </p>
                                        <h3 style="margin: 0.5rem 0 0 0; color: #1f2937; font-size: 1.875rem; font-weight: bold;">
                                            {kpi.format_value()}
                                        </h3>
                                        {f'<p style="margin: 0.25rem 0 0 0; color: {border_color}; font-size: 0.875rem;">{color} {kpi.trend_text}</p>' if kpi.trend_text else ''}
                                        {f'<p style="margin: 0.25rem 0 0 0; color: #6b7280; font-size: 0.75rem;">{kpi.description}</p>' if kpi.description else ''}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                    else:
                        st.info("📊 Nessun KPI disponibile con i dati attuali")

                    # Mostra KPI Summary
                    if st.checkbox("📊 Vedi Dettagli KPI"):
                        summary = kpi_calculator_filtered.get_kpi_summary()
                        st.json(
                            {
                                "total_kpis": summary["total_kpis"],
                                "data_quality": summary["data_quality"],
                                "timestamp": summary["timestamp"],
                            }
                        )

                except Exception as e:
                    st.error(f"❌ Errore KPI: {str(e)}")
                    import traceback

                    st.error(traceback.format_exc())

            # ================================================================
            # SEZIONE 4: GRAFICI INTELLIGENTI
            # ================================================================
            if show_charts:
                st.markdown("---")
                st.subheader("📈 Grafici Intelligenti")

                try:
                    # Detecta chart candidati
                    chart_candidates = get_chart_candidates(filtered_df)

                    if chart_candidates:
                        # Layout randomizer per charts
                        chart_config = create_dynamic_chart_grid(
                            chart_candidates, layout_engine
                        )

                        st.caption(
                            f"Template: {chart_config['template']['description']}"
                        )

                        # Renderizza charts
                        num_cols = chart_config["num_cols"]
                        cols = st.columns(num_cols)

                        for idx, chart in enumerate(chart_config["charts"][:6]):
                            col_idx = idx % num_cols
                            render_intelligent_chart(
                                filtered_df, chart, col=cols[col_idx]
                            )
                    else:
                        st.info("📊 Non abbastanza dati per generare grafici")

                except Exception as e:
                    st.error(f"❌ Errore grafici: {str(e)}")

            # ================================================================
            # SEZIONE 5: TABELLE INTERACTIVE
            # ================================================================
            if show_tables:
                st.markdown("---")

                # Usa tabella interattiva
                table = InteractiveTable(filtered_df, title="Dati Dettagliati")
                table.render()

            # ================================================================
            # SEZIONE 6: EXPORT
            # ================================================================
            st.markdown("---")
            st.subheader("💾 Download Risultati")

            col1, col2, col3, col4 = st.columns(4)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            with col1:
                csv_data = filtered_df.to_csv(index=False)
                st.download_button(
                    "📊 CSV", csv_data, f"data_{timestamp}.csv", "text/csv"
                )

            with col2:
                json_data = filtered_df.to_json(orient="records")
                st.download_button(
                    "🔗 JSON", json_data, f"data_{timestamp}.json", "application/json"
                )

            with col3:
                # Excel export (richiede openpyxl)
                try:
                    import openpyxl

                    with tempfile.NamedTemporaryFile(
                        suffix=".xlsx", delete=False
                    ) as tmp:
                        filtered_df.to_excel(tmp.name, index=False)
                        with open(tmp.name, "rb") as f:
                            st.download_button(
                                "📋 Excel",
                                f.read(),
                                f"data_{timestamp}.xlsx",
                                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )
                except:
                    st.button("📋 Excel", disabled=True, help="Richiede openpyxl")

            with col4:
                # Tableau documentation
                try:
                    tableau_gen = TableauDocumentationGenerator(
                        filtered_df, title="Dashboard"
                    )
                    tableau_guide = tableau_gen.generate_tableau_guide()
                    st.download_button(
                        "📊 Guida Tableau",
                        tableau_guide,
                        f"tableau_guide_{timestamp}.md",
                        "text/markdown",
                        help="Guida completa per ricreate i grafici su Tableau",
                    )
                except Exception as e:
                    st.button(
                        "📊 Guida Tableau", disabled=True, help=f"Errore: {str(e)}"
                    )

else:
    # Landing page
    st.markdown("""
    ## 👈 Carica un File per Iniziare
    
    **Dashboard Generator v4.0** crea automaticamente:
    
    ### ✨ Funzionalità
    - 📊 **Grafici Intelligenti** - Tipo di grafico automatico per i tuoi dati
    - 💰 **KPI Dinamici** - Metriche rilevate dal dataset
    - 🔍 **Analisi ML** - Qualità dati, correlazioni, anomalie
    - 📋 **Tabelle Interattive** - Filtri, sorting, ricerca
    - 🎨 **Layout Responsivo** - Perfetto su qualsiasi dispositivo
    - ♿ **Accessibile** - WCAG 2.1 AA compliant
    - 🔄 **Layout Dinamico** - Design sempre fresco ad ogni caricamento
    
    ### 📌 Formati Supportati
    - CSV (UTF-8, Latin1, ISO-8859-1)
    - Excel (XLSX, XLS)
    - JSON
    
    ### 🎯 Casi d'uso
    - 📈 **Vendite**: Data, Prodotto, Quantità, Prezzo, Regione
    - 👥 **Clienti**: Nome, Città, Spesa, # Acquisti, Status
    - 📢 **Marketing**: Click, Impressioni, Conversioni, Costo
    - 💼 **Finanza**: Entrate, Uscite, Profitto, Margine
    - ⚙️ **Operazioni**: KPI, Metriche, Target, Status
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.85rem;'>"
    "🤖 AI Dashboard Generator v4.0 | Responsive • Dynamic • Accessible"
    "</p>",
    unsafe_allow_html=True,
)
