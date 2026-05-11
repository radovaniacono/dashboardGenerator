"""
KPI Cards - Componenti per visualizzazione metriche
Supporta vari stili e layout dinamici
"""

import streamlit as st
from typing import Dict, List, Optional
import pandas as pd


class KPICard:
    """Rappresentazione di una metrica KPI"""

    def __init__(
        self,
        title: str,
        value: any,
        icon: str = "📊",
        trend: Optional[float] = None,
        unit: str = "",
        color: str = "neutral",
    ):
        """
        Inizializza una KPI card

        Args:
            title: Titolo della metrica
            value: Valore numerico
            icon: Emoji/icona
            trend: Variazione percentuale (opzionale)
            unit: Unità di misura (%, $, ecc)
            color: Colore ('positive', 'negative', 'neutral', 'warning')
        """
        self.title = title
        self.value = value
        self.icon = icon
        self.trend = trend
        self.unit = unit
        self.color = color

        # Determina colore da trend se non specificato
        if self.color == "neutral" and trend is not None:
            if trend > 0:
                self.color = "positive"
            elif trend < 0:
                self.color = "negative"
            else:
                self.color = "neutral"

    def get_color_class(self) -> str:
        """Restituisce classe CSS del colore"""
        return self.color

    def get_trend_icon(self) -> str:
        """Restituisce icona del trend"""
        if self.trend is None:
            return ""
        elif self.trend > 0:
            return "↑"
        elif self.trend < 0:
            return "↓"
        else:
            return "→"

    def format_value(self) -> str:
        """Formatta il valore per visualizzazione"""
        if isinstance(self.value, (int, float)):
            # Arrotonda numeri grandi
            if self.value >= 1000000:
                return f"{self.value/1000000:.1f}M"
            elif self.value >= 1000:
                return f"{self.value/1000:.1f}K"
            else:
                return f"{self.value:,.0f}"
        return str(self.value)

    def render(self, container=None):
        """
        Renderizza la KPI card

        Args:
            container: Contenitore Streamlit (default: main)
        """
        if container is None:
            container = st

        with container.container(border=True):
            # Header
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {self.icon} {self.title}")
            with col2:
                if self.trend is not None:
                    trend_color = (
                        "🟢" if self.trend > 0 else "🔴" if self.trend < 0 else "⚪"
                    )
                    st.markdown(
                        f"<div style='text-align: right'>{trend_color}</div>",
                        unsafe_allow_html=True,
                    )

            # Valore
            value_html = f"""
            <h2 style='
                font-family: IBM Plex Mono;
                font-size: 2.5rem;
                font-weight: bold;
                margin: 0.5rem 0;
                color: #1f2937;
            '>{self.format_value()} {self.unit}</h2>
            """
            st.markdown(value_html, unsafe_allow_html=True)

            # Trend
            if self.trend is not None:
                trend_text = f"{abs(self.trend):.1f}% vs periodo precedente"
                st.markdown(
                    f"<p style='color: #6b7280; margin: 0'>{self.get_trend_icon()} {trend_text}</p>",
                    unsafe_allow_html=True,
                )


def render_kpi_grid(
    kpis: List[KPICard], num_columns: int = 3, show_spacing: bool = True
):
    """
    Renderizza una griglia di KPI

    Args:
        kpis: Lista di KPICard
        num_columns: Numero di colonne
        show_spacing: Mostra spacing tra card
    """
    if not kpis:
        st.warning("Nessun KPI da mostrare")
        return

    # Crea righe
    for i in range(0, len(kpis), num_columns):
        cols = st.columns(num_columns)

        for j, col in enumerate(cols):
            if i + j < len(kpis):
                with col:
                    kpis[i + j].render()

        if show_spacing and i + num_columns < len(kpis):
            st.markdown("")


def create_kpi_from_metric(
    metric_name: str,
    metric_value: float,
    metric_trend: float = None,
    metric_type: str = "numeric",
) -> KPICard:
    """
    Factory per creare KPI da metrica

    Args:
        metric_name: Nome della metrica
        metric_value: Valore numerico
        metric_trend: Trend %
        metric_type: Tipo ('monetary', 'percentage', 'numeric', 'count')

    Returns:
        KPICard configurato
    """
    # Mappa icone per tipo
    icon_map = {
        "monetary": "💰",
        "percentage": "📊",
        "count": "🔢",
        "numeric": "📈",
    }

    # Mappa unità
    unit_map = {
        "monetary": "$",
        "percentage": "%",
        "count": "",
        "numeric": "",
    }

    icon = icon_map.get(metric_type, "📊")
    unit = unit_map.get(metric_type, "")

    return KPICard(
        title=metric_name, value=metric_value, icon=icon, trend=metric_trend, unit=unit
    )


def render_kpi_summary(df: pd.DataFrame, ml_analyzer):
    """
    Renderizza summary KPI intelligente da dataframe

    Args:
        df: DataFrame sorgente
        ml_analyzer: MLAnalyzer per insights
    """
    st.markdown("---")
    st.subheader("💰 Key Performance Indicators")

    kpis = []

    # KPI 1: Numero righe
    kpis.append(KPICard(title="Dataset Size", value=len(df), icon="📊", unit="righe"))

    # KPI 2: Numero colonne
    kpis.append(
        KPICard(title="Dimensioni", value=len(df.columns), icon="📐", unit="colonne")
    )

    # KPI 3: Completezza
    total_cells = len(df) * len(df.columns)
    non_null_cells = df.count().sum()
    completeness = (non_null_cells / total_cells * 100) if total_cells > 0 else 0
    kpis.append(KPICard(title="Qualità Dati", value=completeness, icon="�️", unit="%"))

    # KPI 4: Metriche numeriche
    numeric_cols = (
        len(ml_analyzer.numeric_cols) if hasattr(ml_analyzer, "numeric_cols") else 0
    )
    kpis.append(KPICard(title="Colonne Numeriche", value=numeric_cols, icon="�"))

    # Renderizza grid
    render_kpi_grid(kpis, num_columns=4)


def highlight_outliers(df: pd.DataFrame, column: str) -> list:
    """
    Identifica outlier in una colonna
    Usa metodo 3-sigma

    Args:
        df: DataFrame
        column: Nome colonna

    Returns:
        Lista di indici outlier
    """
    if column not in df.columns:
        return []

    # Solo su colonne numeriche
    if not pd.api.types.is_numeric_dtype(df[column]):
        return []

    data = df[column].dropna()

    if len(data) == 0:
        return []

    mean = data.mean()
    std = data.std()

    if std == 0:
        return []

    # 3-sigma rule
    threshold = 3
    outliers = []

    for idx, val in data.items():
        if abs((val - mean) / std) > threshold:
            outliers.append(idx)

    return outliers


def mark_outliers_in_table(df: pd.DataFrame, numeric_cols: list = None) -> pd.DataFrame:
    """
    Aggiunge colonna di flag per outlier
    Utile per evidenziazione in tabelle

    Args:
        df: DataFrame
        numeric_cols: Colonne numeriche da controllare

    Returns:
        DataFrame con colonna _outlier
    """
    df = df.copy()
    df["_is_outlier"] = False

    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[float, int]).columns

    for col in numeric_cols:
        outlier_indices = highlight_outliers(df, col)
        df.loc[outlier_indices, "_is_outlier"] = True

    return df
