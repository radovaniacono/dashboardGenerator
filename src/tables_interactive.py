"""
Interactive Tables - Tabelle avanzate con filtri intelligenti
Supporta sorting, filtering, export e anomaly detection
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple, Any, Optional


class TableFilterSystem:
    """Sistema di filtri intelligente per tabelle"""

    def __init__(self, df: pd.DataFrame):
        """
        Inizializza sistema filtri

        Args:
            df: DataFrame sorgente
        """
        self.df = df
        self.filters = {}

    def get_filter_widget(
        self, column: str, column_type: str = None
    ) -> Tuple[str, Any]:
        """
        Crea widget di filtro appropriato al tipo di colonna

        Args:
            column: Nome colonna
            column_type: Tipo dato ('numeric', 'categorical', 'datetime', 'text')

        Returns:
            Tupla (filter_key, filter_value)
        """
        col1, col2 = st.columns([1, 3])

        with col1:
            st.write(f"**{column}**")

        # Detecta tipo se non specificato
        if column_type is None:
            if pd.api.types.is_numeric_dtype(self.df[column]):
                column_type = "numeric"
            elif pd.api.types.is_datetime64_any_dtype(self.df[column]):
                column_type = "datetime"
            elif self.df[column].nunique() < 10:
                column_type = "categorical"
            else:
                column_type = "text"

        with col2:
            if column_type == "numeric":
                return self._numeric_filter(column)
            elif column_type == "datetime":
                return self._datetime_filter(column)
            elif column_type == "categorical":
                return self._categorical_filter(column)
            else:
                return self._text_filter(column)

    def _numeric_filter(self, column: str) -> Tuple[str, Dict]:
        """Filtro per colonna numerica (range slider)"""
        min_val = float(self.df[column].min())
        max_val = float(self.df[column].max())

        filter_range = st.slider(
            f"Range {column}",
            min_val,
            max_val,
            (min_val, max_val),
            key=f"filter_{column}_numeric",
        )

        return (column, ("numeric", filter_range))

    def _datetime_filter(self, column: str) -> Tuple[str, Dict]:
        """Filtro per colonna data"""
        min_date = self.df[column].min()
        max_date = self.df[column].max()

        date_range = st.slider(
            f"Date range {column}",
            min_date,
            max_date,
            (min_date, max_date),
            key=f"filter_{column}_datetime",
        )

        return (column, ("datetime", date_range))

    def _categorical_filter(self, column: str) -> Tuple[str, Dict]:
        """Filtro per colonna categorica (multiselect)"""
        unique_values = self.df[column].dropna().unique()

        selected = st.multiselect(
            f"Select {column}",
            unique_values,
            default=list(unique_values),
            key=f"filter_{column}_categorical",
        )

        return (column, ("categorical", selected))

    def _text_filter(self, column: str) -> Tuple[str, Dict]:
        """Filtro per colonna testo (search)"""
        search_text = st.text_input(f"Search {column}", key=f"filter_{column}_text")

        return (column, ("text", search_text))

    def apply_filters(self, filters: Dict) -> pd.DataFrame:
        """
        Applica filtri al dataframe

        Args:
            filters: Dizionario filtri

        Returns:
            DataFrame filtrato
        """
        filtered_df = self.df.copy()

        for column, (filter_type, value) in filters.items():
            if filter_type == "numeric":
                min_val, max_val = value
                filtered_df = filtered_df[
                    (filtered_df[column] >= min_val) & (filtered_df[column] <= max_val)
                ]

            elif filter_type == "datetime":
                start_date, end_date = value
                filtered_df = filtered_df[
                    (filtered_df[column] >= start_date)
                    & (filtered_df[column] <= end_date)
                ]

            elif filter_type == "categorical":
                filtered_df = filtered_df[filtered_df[column].isin(value)]

            elif filter_type == "text":
                if value:  # Se c'è testo
                    filtered_df = filtered_df[
                        filtered_df[column]
                        .astype(str)
                        .str.contains(value, case=False, regex=False)
                    ]

        return filtered_df


class InteractiveTable:
    """Tabella interattiva con funzionalità avanzate"""

    def __init__(self, df: pd.DataFrame, title: str = None):
        """
        Inizializza tabella

        Args:
            df: DataFrame sorgente
            title: Titolo tabella
        """
        self.df = df
        self.title = title or "Dati"
        self.filter_system = TableFilterSystem(df)

    def render(self):
        """Renderizza tabella interattiva completa"""
        st.markdown("---")
        st.subheader(f"📋 {self.title}")

        # Control bar
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            search_term = st.text_input("🔍 Ricerca globale", key="table_search")

        with col2:
            show_stats = st.checkbox("📊 Statistiche", key="table_stats")

        with col3:
            export_format = st.selectbox(
                "📥 Export", ["CSV", "Excel", "JSON"], key="table_export"
            )

        with col4:
            if st.button("⬇️ Scarica", key="table_download"):
                self._download_data(export_format)

        # Ricerca globale
        filtered_df = self.df.copy()
        if search_term:
            mask = False
            for col in self.df.columns:
                mask |= (
                    self.df[col]
                    .astype(str)
                    .str.contains(search_term, case=False, regex=False)
                )
            filtered_df = self.df[mask]

        # Info
        st.info(f"📊 Mostra {len(filtered_df):,} di {len(self.df):,} record")

        # Tabella
        st.dataframe(filtered_df, use_container_width=True, hide_index=True, height=400)

        # Statistiche opzionali
        if show_stats:
            self._show_statistics(filtered_df)

    def _show_statistics(self, df: pd.DataFrame):
        """Mostra statistiche descrittive"""
        st.markdown("#### 📊 Statistiche Descrittive")

        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 0:
            st.dataframe(numeric_df.describe(), use_container_width=True)

    def _download_data(self, format: str):
        """Scarica dati in formato specificato"""
        try:
            if format == "CSV":
                csv = self.df.to_csv(index=False)
                st.download_button("Download CSV", csv, "data.csv", "text/csv")
            elif format == "Excel":
                self.df.to_excel("temp_data.xlsx", index=False)
                with open("temp_data.xlsx", "rb") as f:
                    st.download_button(
                        "Download Excel",
                        f,
                        "data.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
            elif format == "JSON":
                json_str = self.df.to_json(orient="records", indent=2)
                st.download_button(
                    "Download JSON", json_str, "data.json", "application/json"
                )
        except Exception as e:
            st.error(f"Errore download: {str(e)}")


def detect_outliers(df: pd.DataFrame, column: str) -> List[int]:
    """
    Detecta outlier in colonna usando metodo 3-sigma

    Args:
        df: DataFrame
        column: Nome colonna

    Returns:
        Lista di indici outlier
    """
    if column not in df.columns:
        return []

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
    outlier_indices = []

    for idx, val in data.items():
        if abs((val - mean) / std) > 3:
            outlier_indices.append(idx)

    return outlier_indices


def highlight_outlier_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggiunge colonna per evidenziare righe con outlier

    Args:
        df: DataFrame

    Returns:
        DataFrame con colonna _outlier_flag
    """
    df = df.copy()
    df["_outlier_flag"] = False

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        outlier_indices = detect_outliers(df, col)
        df.loc[outlier_indices, "_outlier_flag"] = True

    return df


def create_summary_statistics(df: pd.DataFrame) -> Dict:
    """
    Crea summary statistiche del dataframe

    Args:
        df: DataFrame

    Returns:
        Dizionario con statistiche
    """
    return {
        "total_rows": len(df),
        "total_cols": len(df.columns),
        "numeric_cols": len(df.select_dtypes(include=[np.number]).columns),
        "categorical_cols": len(
            df.select_dtypes(include=["object", "category"]).columns
        ),
        "missing_pct": (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100),
        "duplicates": df.duplicated().sum(),
    }


def render_table_with_filters(
    df: pd.DataFrame, title: str = "Data", columns_to_show: List[str] = None
):
    """
    Renderizza tabella con sistema filtri completo

    Args:
        df: DataFrame
        title: Titolo tabella
        columns_to_show: Colonne da mostrare (default: tutte)
    """
    if columns_to_show is None:
        columns_to_show = list(df.columns)

    st.markdown("---")
    st.subheader(f"📋 {title}")

    # Sidebar filtri
    with st.expander("⚙️ Filtri Avanzati"):
        filter_system = TableFilterSystem(df)
        filters = {}

        for col in columns_to_show:
            key, value = filter_system.get_filter_widget(col)
            if value is not None:
                filters[key] = value

    # Applica filtri
    filtered_df = filter_system.apply_filters(filters)

    # Info
    st.info(f"Mostra {len(filtered_df):,} di {len(df):,} record")

    # Tabella
    st.dataframe(
        filtered_df[columns_to_show], use_container_width=True, hide_index=True
    )
