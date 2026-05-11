"""
Global Filter System - Sistema di filtri globale applicato a tutta la dashboard
Sincronizza filtri tra sezioni e applica intelligentemente
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Dict, Tuple, Any, List, Optional


class GlobalFilterManager:
    """Gestisce filtri globali della dashboard"""

    def __init__(self):
        """Inizializza il manager filtri"""
        if "global_filters" not in st.session_state:
            st.session_state.global_filters = {}

        if "filter_reset_count" not in st.session_state:
            st.session_state.filter_reset_count = 0

    def add_filter(self, filter_key: str, filter_value: Any):
        """
        Aggiunge un filtro globale

        Args:
            filter_key: Chiave univoca del filtro
            filter_value: Valore del filtro
        """
        st.session_state.global_filters[filter_key] = filter_value

    def get_filter(self, filter_key: str) -> Any:
        """
        Recupera valore di un filtro

        Args:
            filter_key: Chiave del filtro

        Returns:
            Valore del filtro o None
        """
        return st.session_state.global_filters.get(filter_key)

    def remove_filter(self, filter_key: str):
        """
        Rimuove un filtro

        Args:
            filter_key: Chiave del filtro
        """
        if filter_key in st.session_state.global_filters:
            del st.session_state.global_filters[filter_key]

    def reset_all_filters(self):
        """Resetta tutti i filtri"""
        st.session_state.global_filters = {}
        st.session_state.filter_reset_count += 1

    def get_all_filters(self) -> Dict[str, Any]:
        """Restituisce tutti i filtri attivi"""
        return st.session_state.global_filters.copy()

    def has_active_filters(self) -> bool:
        """Verifica se ci sono filtri attivi"""
        return len(st.session_state.global_filters) > 0


class FilterBar:
    """Renderizza barra di filtri globale sticky"""

    def __init__(self, df: pd.DataFrame):
        """
        Inizializza filter bar

        Args:
            df: DataFrame sorgente
        """
        self.df = df
        self.manager = GlobalFilterManager()
        self._detect_columns_to_filter()

    def _detect_columns_to_filter(self):
        """Detecta quali colonne sono filtrabili"""
        self.numeric_cols = list(self.df.select_dtypes(include=["number"]).columns)
        self.categorical_cols = list(
            self.df.select_dtypes(include=["object", "category"]).columns
        )
        self.datetime_cols = list(self.df.select_dtypes(include=["datetime64"]).columns)

    def render(self):
        """Renderizza la barra di filtri"""
        st.markdown("---")
        st.subheader("🔍 Filtri Globali")

        with st.container(border=True):
            cols = st.columns([1, 1, 1, 0.5])

            # Filtro data (se esiste colonna temporale)
            if self.datetime_cols:
                with cols[0]:
                    st.write("**📅 Data**")
                    self._render_date_filter()

            # Filtro categoria
            if self.categorical_cols:
                with cols[1]:
                    st.write("**🏷️ Categoria**")
                    self._render_category_filter()

            # Filtro range numerico
            if self.numeric_cols:
                with cols[2]:
                    st.write("**🔢 Range**")
                    self._render_numeric_filter()

            # Pulsante reset
            with cols[3]:
                st.write("")  # Spacing
                if st.button("🔄 Reset", use_container_width=True):
                    self.manager.reset_all_filters()
                    st.rerun()

    def _render_date_filter(self):
        """Renderizza filtro data"""
        date_col = self.datetime_cols[0]

        min_date = self.df[date_col].min()
        max_date = self.df[date_col].max()

        if pd.isna(min_date) or pd.isna(max_date):
            st.write("No data available")
            return

        date_range = st.slider(
            "Date Range",
            min_date.date() if hasattr(min_date, "date") else min_date,
            max_date.date() if hasattr(max_date, "date") else max_date,
            (
                min_date.date() if hasattr(min_date, "date") else min_date,
                max_date.date() if hasattr(max_date, "date") else max_date,
            ),
            key="global_filter_date",
        )

        self.manager.add_filter("date_range", (date_col, date_range))

    def _render_category_filter(self):
        """Renderizza filtro categoria"""
        if not self.categorical_cols:
            return

        cat_col = st.selectbox(
            "Colonna", self.categorical_cols, key="filter_cat_select"
        )

        unique_values = self.df[cat_col].dropna().unique()

        selected = st.multiselect(
            "Valori",
            unique_values,
            default=list(unique_values),
            key=f"global_filter_cat_{cat_col}",
        )

        self.manager.add_filter("category_filter", (cat_col, selected))

    def _render_numeric_filter(self):
        """Renderizza filtro range numerico"""
        if not self.numeric_cols:
            return

        num_col = st.selectbox("Colonna", self.numeric_cols, key="filter_num_select")

        min_val = float(self.df[num_col].min())
        max_val = float(self.df[num_col].max())

        range_vals = st.slider(
            "Range",
            min_val,
            max_val,
            (min_val, max_val),
            key=f"global_filter_num_{num_col}",
        )

        self.manager.add_filter("numeric_filter", (num_col, range_vals))

    def apply_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applica tutti i filtri globali al dataframe

        Args:
            df: DataFrame sorgente

        Returns:
            DataFrame filtrato
        """
        filtered_df = df.copy()
        filters = self.manager.get_all_filters()

        # Filtro data
        if "date_range" in filters:
            date_col, (start_date, end_date) = filters["date_range"]
            if date_col in df.columns:
                filtered_df = filtered_df[
                    (pd.to_datetime(filtered_df[date_col]).dt.date >= start_date)
                    & (pd.to_datetime(filtered_df[date_col]).dt.date <= end_date)
                ]

        # Filtro categoria
        if "category_filter" in filters:
            cat_col, selected_values = filters["category_filter"]
            if cat_col in df.columns:
                filtered_df = filtered_df[filtered_df[cat_col].isin(selected_values)]

        # Filtro numerico
        if "numeric_filter" in filters:
            num_col, (min_val, max_val) = filters["numeric_filter"]
            if num_col in df.columns:
                filtered_df = filtered_df[
                    (filtered_df[num_col] >= min_val)
                    & (filtered_df[num_col] <= max_val)
                ]

        return filtered_df

    def show_active_filters(self):
        """Mostra i filtri attivi come pills"""
        if not self.manager.has_active_filters():
            st.info("Nessun filtro attivo")
            return

        st.markdown("#### Filtri Attivi:")

        filters = self.manager.get_all_filters()
        pill_html = '<div style="display: flex; gap: 8px; flex-wrap: wrap;">'

        for filter_key, filter_value in filters.items():
            if filter_key == "date_range":
                col_name, (start, end) = filter_value
                pill_html += f'<span style="background: #e3f2fd; padding: 6px 12px; border-radius: 20px; font-size: 12px;">📅 {col_name}: {start} to {end}</span>'

            elif filter_key == "category_filter":
                col_name, values = filter_value
                value_str = ", ".join(str(v)[:10] for v in values[:3])
                if len(values) > 3:
                    value_str += f" (+{len(values)-3})"
                pill_html += f'<span style="background: #f3e5f5; padding: 6px 12px; border-radius: 20px; font-size: 12px;">🏷️ {col_name}: {value_str}</span>'

            elif filter_key == "numeric_filter":
                col_name, (min_val, max_val) = filter_value
                pill_html += f'<span style="background: #fff3e0; padding: 6px 12px; border-radius: 20px; font-size: 12px;">🔢 {col_name}: {min_val:.0f} - {max_val:.0f}</span>'

        pill_html += "</div>"
        st.markdown(pill_html, unsafe_allow_html=True)


def create_quick_filters(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Crea filtri rapidi da widget Streamlit

    Args:
        df: DataFrame

    Returns:
        Dizionario con filtri
    """
    filters = {}

    col1, col2, col3, col4 = st.columns(4)

    numeric_cols = df.select_dtypes(include=["number"]).columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    # Filtro 1: Numero valori
    with col1:
        if numeric_cols:
            col_name = numeric_cols[0]
            range_val = st.slider(
                f"{col_name}",
                float(df[col_name].min()),
                float(df[col_name].max()),
                (float(df[col_name].min()), float(df[col_name].max())),
            )
            filters[f"{col_name}_range"] = range_val

    # Filtro 2: Categoria
    with col2:
        if categorical_cols:
            col_name = categorical_cols[0]
            unique_vals = df[col_name].dropna().unique()
            selected = st.multiselect(
                f"{col_name}", unique_vals, default=list(unique_vals)
            )
            filters[col_name] = selected

    # Filtri aggiuntivi
    with col3:
        if len(numeric_cols) > 1:
            col_name = numeric_cols[1]
            range_val = st.slider(
                f"{col_name}",
                float(df[col_name].min()),
                float(df[col_name].max()),
                (float(df[col_name].min()), float(df[col_name].max())),
            )
            filters[f"{col_name}_range"] = range_val

    # Reset button
    with col4:
        st.write("")
        if st.button("🔄 Reset Filtri"):
            st.session_state.clear()
            st.rerun()

    return filters
