"""
KPI Calculator - Calcolo automatico e intelligente di KPI
Rileva automaticamente le metriche più significative basate sui dati
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")


class KPI:
    """Rappresentazione di una singola metrica KPI"""

    def __init__(
        self,
        name: str,
        value: any,
        format_type: str = "number",
        icon: str = "📊",
        description: str = "",
        significance_score: float = 0.5,
        is_temporal: bool = False,
        previous_value: Optional[float] = None,
    ):
        self.name = name
        self.value = value
        self.format_type = format_type
        self.icon = icon
        self.description = description
        self.significance_score = significance_score
        self.is_temporal = is_temporal
        self.previous_value = previous_value
        self.trend_value = None
        self.trend_direction = None
        self.trend_text = None

        # Calcola trend se disponibile
        if previous_value is not None and isinstance(value, (int, float)):
            self._calculate_trend()

    def _calculate_trend(self):
        """Calcola trend percentuale rispetto a valore precedente"""
        if self.previous_value == 0:
            self.trend_value = 0
            self.trend_direction = "neutral"
        else:
            change_pct = (
                (self.value - self.previous_value) / abs(self.previous_value)
            ) * 100
            self.trend_value = abs(change_pct)
            self.trend_direction = (
                "up" if change_pct > 0 else "down" if change_pct < 0 else "neutral"
            )
            self.trend_text = f"{change_pct:+.1f}%"

    def format_value(self) -> str:
        """Formatta il valore per visualizzazione"""
        if not isinstance(self.value, (int, float)):
            return str(self.value)

        if self.format_type == "currency":
            if self.value >= 1000000:
                return f"€{self.value/1000000:.1f}M"
            elif self.value >= 1000:
                return f"€{self.value/1000:.1f}K"
            else:
                return f"€{self.value:,.0f}"

        elif self.format_type == "percentage":
            return f"{self.value:.1f}%"

        elif self.format_type == "decimal":
            return f"{self.value:.2f}"

        elif self.format_type == "integer":
            return f"{int(self.value):,}"

        elif self.format_type == "duration":
            # Giorni, ore, etc.
            if isinstance(self.value, timedelta):
                return f"{self.value.days} giorni"
            return str(self.value)

        else:  # number
            if self.value >= 1000000:
                return f"{self.value/1000000:.1f}M"
            elif self.value >= 1000:
                return f"{self.value/1000:.1f}K"
            else:
                return f"{int(self.value):,}"

    def to_dict(self) -> Dict:
        """Converte KPI a dizionario"""
        return {
            "name": self.name,
            "value": self.value,
            "formatted_value": self.format_value(),
            "format_type": self.format_type,
            "icon": self.icon,
            "description": self.description,
            "significance_score": self.significance_score,
            "trend_value": self.trend_value,
            "trend_direction": self.trend_direction,
            "trend_text": self.trend_text,
        }


class KPICalculator:
    """Calcola automaticamente i KPI più significativi da un dataset"""

    def __init__(self, df: pd.DataFrame, ml_analyzer=None):
        """
        Inizializza il calcolatore KPI

        Args:
            df: DataFrame con i dati
            ml_analyzer: Istanza di MLAnalyzer (opzionale, per info sui tipi di colonne)
        """
        self.df = df
        self.ml_analyzer = ml_analyzer

        # Tipi di colonne
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        self.date_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

        # Se disponibile ML analyzer, usa le sue rilevazioni
        if ml_analyzer:
            self.monetary_cols = ml_analyzer.monetary_cols
            self.percentage_cols = ml_analyzer.percentage_cols
            self.boolean_cols = ml_analyzer.boolean_cols
        else:
            self.monetary_cols = self._detect_monetary_columns()
            self.percentage_cols = self._detect_percentage_columns()
            self.boolean_cols = self._detect_boolean_columns()

    def calculate_all_kpis(self, max_kpis: int = 8) -> List[KPI]:
        """
        Calcola automaticamente tutti i KPI significativi

        Args:
            max_kpis: Massimo numero di KPI da restituire

        Returns:
            Lista di KPI ordinati per significatività
        """
        all_kpis = []

        # Step 1: Calcola KPI da colonne numeriche
        for col in self.numeric_cols:
            all_kpis.extend(self._calculate_numeric_kpis(col))

        # Step 2: Calcola KPI da colonne categoriche
        for col in self.categorical_cols:
            all_kpis.extend(self._calculate_categorical_kpis(col))

        # Step 3: Calcola KPI da colonne temporali
        for col in self.date_cols:
            all_kpis.extend(self._calculate_temporal_kpis(col))

        # Step 4: Ranking per significatività
        ranked_kpis = sorted(all_kpis, key=lambda x: x.significance_score, reverse=True)

        # Step 5: Selezione bilanciata (elimina duplicati concettuali)
        selected = self._select_balanced_kpis(ranked_kpis, max_count=max_kpis)

        return selected

    def _calculate_numeric_kpis(self, col_name: str) -> List[KPI]:
        """Crea KPI da colonne numeriche"""
        kpis = []
        col_data = self.df[col_name].dropna()

        if len(col_data) == 0:
            return kpis

        # KPI Somma (se colonna monetaria o rappresenta totale)
        if col_name in self.monetary_cols:
            total_value = col_data.sum()
            kpis.append(
                KPI(
                    name=f"Totale {col_name}",
                    value=total_value,
                    format_type="currency",
                    icon="💰",
                    description=f"Somma totale di {col_name}",
                    significance_score=0.95,
                )
            )

        # KPI Media
        mean_value = col_data.mean()
        kpis.append(
            KPI(
                name=f"Media {col_name}",
                value=mean_value,
                format_type="decimal" if col_name in self.percentage_cols else "number",
                icon="📊",
                description=f"Valore medio di {col_name}",
                significance_score=0.85,
            )
        )

        # KPI Max (se significativamente diverso dal Min)
        max_val = col_data.max()
        min_val = col_data.min()

        if max_val - min_val > col_data.std() * 2:
            kpis.append(
                KPI(
                    name=f"Max {col_name}",
                    value=max_val,
                    format_type=(
                        "currency" if col_name in self.monetary_cols else "number"
                    ),
                    icon="📈",
                    description=f"Valore massimo di {col_name}",
                    significance_score=0.70,
                )
            )

        # KPI Count (numero record non-null)
        count_value = len(col_data)
        kpis.append(
            KPI(
                name=f"Count {col_name}",
                value=count_value,
                format_type="integer",
                icon="📝",
                description=f"Numero di valori in {col_name}",
                significance_score=0.60,
            )
        )

        # KPI Percentuale (se colonna percentuale)
        if col_name in self.percentage_cols:
            pct_value = col_data.mean()
            kpis.append(
                KPI(
                    name=f"Media {col_name}",
                    value=pct_value,
                    format_type="percentage",
                    icon="📊",
                    description=f"Percentuale media di {col_name}",
                    significance_score=0.80,
                )
            )

        return kpis

    def _calculate_categorical_kpis(self, col_name: str) -> List[KPI]:
        """Crea KPI da colonne categoriche"""
        kpis = []
        col_data = self.df[col_name].dropna()

        if len(col_data) == 0:
            return kpis

        # KPI Top Categoria (la più frequente)
        value_counts = col_data.value_counts()
        if len(value_counts) > 0:
            top_category = value_counts.index[0]
            top_count = value_counts.iloc[0]

            kpis.append(
                KPI(
                    name=f"Top {col_name}",
                    value=f"{top_category} ({top_count})",
                    format_type="string",
                    icon="🎯",
                    description=f"Categoria più frequente in {col_name}",
                    significance_score=0.75,
                )
            )

        # KPI Unique Count (numero di categorie diverse)
        unique_count = col_data.nunique()
        kpis.append(
            KPI(
                name=f"Varietà {col_name}",
                value=unique_count,
                format_type="integer",
                icon="🔀",
                description=f"Numero di categorie diverse in {col_name}",
                significance_score=0.65,
            )
        )

        # KPI Booleani (se è colonna booleana)
        if col_name in self.boolean_cols:
            true_count = (col_data == True).sum() + (
                col_data.astype(str).str.lower() == "true"
            ).sum()
            false_count = len(col_data) - true_count
            pct_true = (true_count / len(col_data)) * 100 if len(col_data) > 0 else 0

            kpis.append(
                KPI(
                    name=f"% True {col_name}",
                    value=pct_true,
                    format_type="percentage",
                    icon="✅",
                    description=f"Percentuale di True in {col_name}",
                    significance_score=0.70,
                )
            )

        return kpis

    def _calculate_temporal_kpis(self, col_name: str) -> List[KPI]:
        """Crea KPI da colonne temporali"""
        kpis = []
        col_data = pd.to_datetime(self.df[col_name]).dropna()

        if len(col_data) == 0:
            return kpis

        # KPI Range temporale
        min_date = col_data.min()
        max_date = col_data.max()
        date_range = max_date - min_date

        kpis.append(
            KPI(
                name=f"Range {col_name}",
                value=f"{min_date.strftime('%d/%m/%Y')} → {max_date.strftime('%d/%m/%Y')}",
                format_type="string",
                icon="📅",
                description=f"Range temporale di {col_name}",
                significance_score=0.80,
            )
        )

        # KPI Durata in giorni
        durata_giorni = date_range.days
        kpis.append(
            KPI(
                name=f"Durata {col_name}",
                value=durata_giorni,
                format_type="duration",
                icon="⏱️",
                description=f"Numero di giorni nel range di {col_name}",
                significance_score=0.75,
            )
        )

        # KPI Frequenza (record per giorno)
        if durata_giorni > 0:
            freq_per_day = len(col_data) / durata_giorni
            kpis.append(
                KPI(
                    name=f"Frequenza {col_name}",
                    value=freq_per_day,
                    format_type="decimal",
                    icon="📊",
                    description=f"Record al giorno in {col_name}",
                    significance_score=0.65,
                )
            )

        return kpis

    def _detect_monetary_columns(self) -> List[str]:
        """Rileva colonne monetarie"""
        monetary = []
        for col in self.numeric_cols:
            col_lower = col.lower()
            if any(
                term in col_lower
                for term in [
                    "price",
                    "cost",
                    "revenue",
                    "sales",
                    "amount",
                    "prezzo",
                    "costo",
                    "ricavo",
                    "vendita",
                    "importo",
                    "valore",
                ]
            ):
                monetary.append(col)
        return monetary

    def _detect_percentage_columns(self) -> List[str]:
        """Rileva colonne percentuali"""
        percentage = []
        for col in self.numeric_cols:
            col_lower = col.lower()
            if any(
                term in col_lower
                for term in ["percent", "rate", "ratio", "%", "percentuale", "tasso"]
            ):
                percentage.append(col)
            elif self.df[col].max() <= 100 and self.df[col].min() >= 0:
                percentage.append(col)
        return percentage

    def _detect_boolean_columns(self) -> List[str]:
        """Rileva colonne booleane"""
        boolean = []
        for col in self.categorical_cols:
            unique_vals = self.df[col].dropna().nunique()
            if unique_vals <= 2:
                boolean.append(col)
        return boolean

    def _select_balanced_kpis(
        self, ranked_kpis: List[KPI], max_count: int = 8
    ) -> List[KPI]:
        """
        Seleziona KPI bilanciati (evita duplicati concettuali)

        Esempio: Se "Totale Revenue" è selezionato, non include "Media Revenue"
        """
        selected = []
        col_names_used = set()

        for kpi in ranked_kpis:
            if len(selected) >= max_count:
                break

            # Estrai nome colonna dal KPI
            col_name = self._extract_column_name(kpi.name)

            # Se già abbiamo un KPI da questa colonna, verifica diversità
            if col_name in col_names_used:
                # Accetta solo se è un tipo diverso (es. Total vs Mean)
                if not self._is_conceptually_similar(selected, kpi):
                    selected.append(kpi)
                    col_names_used.add(col_name)
            else:
                selected.append(kpi)
                col_names_used.add(col_name)

        return selected

    def _extract_column_name(self, kpi_name: str) -> str:
        """Estrae il nome della colonna dal nome del KPI"""
        # Rimuovi prefissi comuni
        for prefix in [
            "Totale ",
            "Media ",
            "Max ",
            "Count ",
            "Top ",
            "Varietà ",
            "Range ",
            "Durata ",
            "Frequenza ",
            "% ",
        ]:
            if kpi_name.startswith(prefix):
                return kpi_name[len(prefix) :]
        return kpi_name

    def _is_conceptually_similar(self, selected_kpis: List[KPI], new_kpi: KPI) -> bool:
        """Verifica se nuovo KPI è concettualmente simile a quelli già selezionati"""
        new_col = self._extract_column_name(new_kpi.name)

        for kpi in selected_kpis:
            kpi_col = self._extract_column_name(kpi.name)

            if kpi_col == new_col:
                # Se dalla stessa colonna, controlla se è lo stesso tipo
                # "Media" e "Totale" sono diversi, ma "Media" e "Media" sono uguali
                if kpi.name.split()[0] == new_kpi.name.split()[0]:
                    return True

        return False

    def get_kpi_summary(self, max_kpis: int = 8) -> Dict:
        """Restituisce un sommario con tutti i KPI principali"""
        kpis = self.calculate_all_kpis(max_kpis)

        return {
            "kpis": [kpi.to_dict() for kpi in kpis],
            "total_kpis": len(kpis),
            "data_quality": self._assess_data_quality(),
            "timestamp": datetime.now().isoformat(),
        }

    def _assess_data_quality(self) -> Dict:
        """Valuta la qualità dei dati"""
        total_cells = self.df.shape[0] * self.df.shape[1]
        null_cells = self.df.isnull().sum().sum()
        completeness = (
            ((total_cells - null_cells) / total_cells) * 100 if total_cells > 0 else 0
        )

        return {
            "completeness_pct": completeness,
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "numeric_columns": len(self.numeric_cols),
            "categorical_columns": len(self.categorical_cols),
            "temporal_columns": len(self.date_cols),
        }
