"""
Intelligent Chart Selector - Sceglie grafici intelligenti basati sui dati
Evita grafici vuoti o inadatti
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Dict, List
import streamlit as st


class ChartAnalyzer:
    """Analizza dati e raccomanda tipo di grafico"""

    @staticmethod
    def is_temporal(series: pd.Series) -> bool:
        """Verifica se serie è temporale"""
        return pd.api.types.is_datetime64_any_dtype(series)

    @staticmethod
    def is_numeric(series: pd.Series) -> bool:
        """Verifica se serie è numerica"""
        return pd.api.types.is_numeric_dtype(series)

    @staticmethod
    def is_categorical(series: pd.Series) -> bool:
        """Verifica se serie è categorica"""
        return pd.api.types.is_object_dtype(
            series
        ) or pd.api.types.is_categorical_dtype(series)

    @staticmethod
    def get_cardinality(series: pd.Series) -> int:
        """Numero valori unici"""
        return series.nunique()

    @staticmethod
    def get_null_rate(series: pd.Series) -> float:
        """Percentuale valori nulli"""
        return series.isnull().sum() / len(series)

    @staticmethod
    def get_variance(series: pd.Series) -> float:
        """Varianza normalizzata"""
        if not ChartAnalyzer.is_numeric(series):
            return 0
        clean = series.dropna()
        if len(clean) == 0 or clean.std() == 0:
            return 0
        return clean.var()

    @staticmethod
    def can_plot_series(series: pd.Series, min_cardinality: int = 2) -> bool:
        """
        Verifica se serie può essere plottata
        """
        # Troppi nulli
        if ChartAnalyzer.get_null_rate(series) > 0.8:
            return False

        # Troppo poca varietà
        cardinality = ChartAnalyzer.get_cardinality(series)
        if cardinality < min_cardinality:
            return False

        return True

    @staticmethod
    def recommend_chart_type(
        x_series: pd.Series = None, y_series: pd.Series = None, df: pd.DataFrame = None
    ) -> Optional[str]:
        """
        Raccomanda tipo di grafico in base ai dati

        Returns:
            'line', 'bar', 'pie', 'scatter', 'histogram', 'box', None
        """
        # Caso 1: Serie singola
        if y_series is not None and x_series is None:
            if ChartAnalyzer.is_categorical(y_series):
                return "bar"
            elif ChartAnalyzer.is_numeric(y_series):
                return "histogram"

        # Caso 2: X temporale, Y numerica
        if ChartAnalyzer.is_temporal(x_series) and ChartAnalyzer.is_numeric(y_series):
            return "line"

        # Caso 3: X categorica, Y numerica
        if ChartAnalyzer.is_categorical(x_series) and ChartAnalyzer.is_numeric(
            y_series
        ):
            cardinality = ChartAnalyzer.get_cardinality(x_series)
            if cardinality <= 5:
                return "pie"  # Poche categorie
            else:
                return "bar"  # Molte categorie

        # Caso 4: X e Y numeriche
        if ChartAnalyzer.is_numeric(x_series) and ChartAnalyzer.is_numeric(y_series):
            return "scatter"

        return None


class IntelligentChartBuilder:
    """Costruisce grafici intelligenti"""

    def __init__(self, df: pd.DataFrame):
        """
        Inizializza builder

        Args:
            df: DataFrame sorgente
        """
        self.df = df
        self.analyzer = ChartAnalyzer()

    def build_line_chart(self, x_col: str, y_col: str, title: str = None) -> go.Figure:
        """Crea line chart"""
        if title is None:
            title = f"{y_col} Over {x_col}"

        fig = px.line(
            self.df,
            x=x_col,
            y=y_col,
            title=title,
            markers=True,
            template="plotly_white",
        )

        fig.update_layout(
            hovermode="x unified", height=400, font=dict(family="IBM Plex Sans")
        )

        return fig

    def build_bar_chart(self, x_col: str, y_col: str, title: str = None) -> go.Figure:
        """Crea bar chart"""
        if title is None:
            title = f"{y_col} by {x_col}"

        fig = px.bar(self.df, x=x_col, y=y_col, title=title, template="plotly_white")

        fig.update_layout(height=400, font=dict(family="IBM Plex Sans"))

        return fig

    def build_pie_chart(
        self, labels_col: str, values_col: str, title: str = None
    ) -> go.Figure:
        """Crea pie chart"""
        if title is None:
            title = f"Distribution of {labels_col}"

        fig = px.pie(
            self.df,
            names=labels_col,
            values=values_col,
            title=title,
            template="plotly_white",
        )

        fig.update_layout(height=400, font=dict(family="IBM Plex Sans"))

        return fig

    def build_scatter_chart(
        self,
        x_col: str,
        y_col: str,
        size_col: str = None,
        color_col: str = None,
        title: str = None,
    ) -> go.Figure:
        """Crea scatter chart"""
        if title is None:
            title = f"{y_col} vs {x_col}"

        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            size=size_col,
            color=color_col,
            title=title,
            template="plotly_white",
        )

        fig.update_layout(height=400, font=dict(family="IBM Plex Sans"))

        return fig

    def build_histogram(
        self, col: str, nbins: int = 30, title: str = None
    ) -> go.Figure:
        """Crea histogram"""
        if title is None:
            title = f"Distribution of {col}"

        fig = px.histogram(
            self.df, x=col, nbins=nbins, title=title, template="plotly_white"
        )

        fig.update_layout(height=400, font=dict(family="IBM Plex Sans"))

        return fig

    def build_box_plot(
        self, y_col: str, x_col: str = None, title: str = None
    ) -> go.Figure:
        """Crea box plot"""
        if title is None:
            title = f"Distribution of {y_col}"

        fig = px.box(self.df, x=x_col, y=y_col, title=title, template="plotly_white")

        fig.update_layout(height=400, font=dict(family="IBM Plex Sans"))

        return fig

    def build_heatmap(
        self, x_col: str, y_col: str, z_col: str, title: str = None
    ) -> go.Figure:
        """Crea heatmap"""
        if title is None:
            title = f"Heatmap: {z_col}"

        pivot = self.df.pivot_table(
            index=y_col, columns=x_col, values=z_col, aggfunc="mean"
        )

        fig = go.Figure(data=go.Heatmap(z=pivot.values))
        fig.update_layout(title=title, height=400, font=dict(family="IBM Plex Sans"))

        return fig


def get_chart_candidates(df: pd.DataFrame) -> List[Dict]:
    """
    Genera lista di chart candidati dal dataframe

    Args:
        df: DataFrame sorgente

    Returns:
        Lista di configurazioni di chart possibili
    """
    candidates = []
    analyzer = ChartAnalyzer()

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    temporal_cols = df.select_dtypes(include=["datetime64"]).columns

    # Chart numeriche vs numeriche
    for i, col1 in enumerate(numeric_cols):
        for col2 in list(numeric_cols)[i + 1 :]:
            if analyzer.can_plot_series(df[col1]) and analyzer.can_plot_series(
                df[col2]
            ):
                candidates.append(
                    {
                        "type": "scatter",
                        "x": col1,
                        "y": col2,
                        "cardinality": analyzer.get_cardinality(df[col1]),
                        "score": 0.8,
                    }
                )

    # Chart temporali vs numeriche
    for temporal in temporal_cols:
        for numeric in numeric_cols:
            if analyzer.can_plot_series(df[temporal]) and analyzer.can_plot_series(
                df[numeric]
            ):
                candidates.append(
                    {
                        "type": "line",
                        "x": temporal,
                        "y": numeric,
                        "cardinality": analyzer.get_cardinality(df[temporal]),
                        "score": 0.9,
                    }
                )

    # Chart categoriche
    for cat in categorical_cols:
        if analyzer.can_plot_series(df[cat], min_cardinality=2):
            # Bar chart
            if len(numeric_cols) > 0:
                for num in numeric_cols:
                    candidates.append(
                        {
                            "type": "bar",
                            "x": cat,
                            "y": num,
                            "cardinality": analyzer.get_cardinality(df[cat]),
                            "score": 0.7,
                        }
                    )

            # Pie chart (solo se poche categorie)
            cardinality = analyzer.get_cardinality(df[cat])
            if cardinality <= 10 and len(numeric_cols) > 0:
                candidates.append(
                    {
                        "type": "pie",
                        "labels": cat,
                        "values": numeric_cols[0],
                        "cardinality": cardinality,
                        "score": 0.75,
                    }
                )

    return candidates


def render_intelligent_chart(df: pd.DataFrame, chart_config: Dict, col=None):
    """
    Renderizza un grafico intelligente

    Args:
        df: DataFrame
        chart_config: Configurazione del grafico
        col: Contenitore Streamlit (default: main)
    """
    if col is None:
        col = st

    builder = IntelligentChartBuilder(df)

    try:
        chart_type = chart_config.get("type")

        if chart_type == "scatter":
            fig = builder.build_scatter_chart(chart_config["x"], chart_config["y"])
        elif chart_type == "line":
            fig = builder.build_line_chart(chart_config["x"], chart_config["y"])
        elif chart_type == "bar":
            fig = builder.build_bar_chart(chart_config["x"], chart_config["y"])
        elif chart_type == "pie":
            fig = builder.build_pie_chart(
                chart_config["labels"], chart_config["values"]
            )
        else:
            return

        with col:
            st.plotly_chart(fig, use_container_width=True, key=hash(str(chart_config)))

    except Exception as e:
        with col:
            st.error(f"Errore nel rendering del grafico: {str(e)}")
