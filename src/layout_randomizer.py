"""
Layout Randomizer - Randomizza il layout mantenendo qualità e coerenza
Fornisce freschezza visiva ad ogni caricamento della dashboard
"""

import random
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple
import pandas as pd


class LayoutRandomizer:
    """
    Randomizza layout della dashboard mantenendo:
    - Qualità dei dati mostrati
    - Varietà visiva
    - Coerenza stilistica
    """

    def __init__(self, seed: int = None):
        """
        Inizializza il randomizer

        Args:
            seed: Se fornito, rende il layout deterministico per l'utente
                  Se None, cambia ad ogni reload
        """
        if seed is None:
            # Cambia layout ogni ora (basato su timestamp)
            seed = int(datetime.now().timestamp() / 3600)

        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)

    def select_visible_kpis(
        self, available_metrics: List[Dict], num_kpis: int = None
    ) -> List[Dict]:
        """
        Seleziona quali KPI mostrare, intelligentemente

        Args:
            available_metrics: Lista di metriche disponibili
            num_kpis: Numero KPI da mostrare (default: random tra 3-8)

        Returns:
            Lista di KPI selezionati
        """
        if not available_metrics:
            return []

        # Seleziona numero KPI casuali (varia ad ogni reload)
        if num_kpis is None:
            num_kpis = random.choice([3, 4, 5, 6, 8])

        num_kpis = min(num_kpis, len(available_metrics))

        # Score ogni metrica
        scored = self._score_metrics(available_metrics)

        # Ordina per score (migliori metriche)
        sorted_metrics = sorted(scored, key=lambda x: x["score"], reverse=True)

        # Prendi top metric sempre
        if sorted_metrics:
            top_metric = sorted_metrics[0]
            remaining = sorted_metrics[1:]

            # Randomizza i rimanenti
            random.shuffle(remaining)

            selected = [top_metric] + remaining[: num_kpis - 1]
            return selected

        return []

    def select_chart_types(
        self, available_charts: List[Dict], num_charts: int
    ) -> List[Dict]:
        """
        Seleziona tipi di grafici mantenendo diversità

        Args:
            available_charts: Lista di grafici disponibili
            num_charts: Numero grafici da mostrare

        Returns:
            Lista di grafici selezionati
        """
        if not available_charts:
            return []

        num_charts = min(num_charts, len(available_charts))

        # Score grafici
        scored = self._score_charts(available_charts)

        # Filtra deboli
        good_charts = [c for c in scored if c["score"] >= 0.4]

        if not good_charts:
            good_charts = scored[:num_charts]

        # Diversifica tipi
        selected = self._diversify_chart_types(good_charts, num_charts)

        return selected

    def randomize_chart_arrangement(
        self, num_charts: int, num_columns: int
    ) -> List[Tuple[int, int]]:
        """
        Randomizza disposizione dei grafici nel grid

        Args:
            num_charts: Numero totale di grafici
            num_columns: Numero colonne disponibili

        Returns:
            Lista di tuple (colonna, dimensione) per ogni grafico
        """
        arrangements = []

        for i in range(num_charts):
            # Alcuni grafici più larghi (occupano 2 colonne)
            width = random.choice([1, 2]) if num_columns > 2 else 1

            # Limita larghezza al massimo disponibile
            width = min(width, num_columns)

            arrangements.append(width)

        return arrangements

    def select_color_scheme(self) -> Dict[str, str]:
        """
        Seleziona uno schema di colori dai predefiniti

        Returns:
            Dizionario con colori dello schema
        """
        schemes = [
            {  # Schema Blu-Viola (default)
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f59e0b",
            },
            {  # Schema Verde-Teal
                "primary": "#10b981",
                "secondary": "#14b8a6",
                "accent": "#f59e0b",
            },
            {  # Schema Rosso-Arancio
                "primary": "#ef4444",
                "secondary": "#f97316",
                "accent": "#fbbf24",
            },
            {  # Schema Indaco-Blu
                "primary": "#4f46e5",
                "secondary": "#3b82f6",
                "accent": "#06b6d4",
            },
        ]

        selected = random.choice(schemes)
        return selected

    def select_layout_template(self, num_charts: int) -> Dict[str, any]:
        """
        Seleziona uno dei template layout predefiniti

        Args:
            num_charts: Numero di grafici da mostrare

        Returns:
            Configurazione template
        """
        templates = [
            {  # Template A: Focus su trend
                "name": "trend-focus",
                "primary_chart": "line",
                "arrangement": "wide-first",
                "description": "Focus su trend temporali",
            },
            {  # Template B: Focus su composizione
                "name": "composition-focus",
                "primary_chart": "pie",
                "arrangement": "balanced",
                "description": "Focus su composizione",
            },
            {  # Template C: Focus su correlazioni
                "name": "correlation-focus",
                "primary_chart": "scatter",
                "arrangement": "grid",
                "description": "Focus su correlazioni",
            },
            {  # Template D: Layout bilanciato
                "name": "balanced",
                "primary_chart": "auto",
                "arrangement": "adaptive",
                "description": "Layout bilanciato",
            },
        ]

        selected = random.choice(templates)
        return selected

    def _score_metrics(self, metrics: List[Dict]) -> List[Dict]:
        """
        Assegna un punteggio intelligente a ogni metrica

        Fattori:
        - Completezza dati
        - Varianza (interessantezza)
        - Trend positivo
        - Rilevanza business
        """
        scored = []

        for metric in metrics:
            score = 0

            # Completezza: dati senza null sono preferiti
            completeness = metric.get("completeness", 1.0)
            score += completeness * 0.3

            # Varianza: data interessante se varia
            variance = metric.get("variance_score", 0.5)
            if variance > 0:  # Evita 0 / infinito
                score += min(variance, 1.0) * 0.3

            # Trend: trend positivi preferiti (business)
            trend = metric.get("trend_score", 0.5)
            score += trend * 0.2

            # Tipo dato: monetari e percentuali interessanti
            if metric.get("type") in ["monetary", "percentage"]:
                score += 0.2

            scored.append({**metric, "score": score})

        return scored

    def _score_charts(self, charts: List[Dict]) -> List[Dict]:
        """
        Assegna punteggio a ogni chart candidato

        Fattori:
        - Cardinale (minimo 3-4 valori unici)
        - Completezza dati
        - Varianza
        """
        scored = []

        for chart in charts:
            score = 0

            # Cardinale: no grafici con troppo pochi valori
            cardinality = chart.get("cardinality", 0)
            if cardinality > 3:
                score += 0.7
            elif cardinality > 1:
                score += 0.3

            # Completezza dati
            null_rate = chart.get("null_rate", 0)
            completeness = 1 - null_rate
            score += completeness * 0.2

            # Varianza
            variance = chart.get("variance", 0.5)
            score += min(variance / 100, 1.0) * 0.1

            scored.append({**chart, "score": score})

        return scored

    def _diversify_chart_types(self, charts: List[Dict], num_select: int) -> List[Dict]:
        """
        Seleziona grafici mantenendo varietà di tipo
        Max 2 dello stesso tipo
        """
        selected = []
        type_counts = {}

        for chart in charts:
            chart_type = chart.get("type", "unknown")

            # Limita a 2 dello stesso tipo
            if type_counts.get(chart_type, 0) < 2:
                selected.append(chart)
                type_counts[chart_type] = type_counts.get(chart_type, 0) + 1

            if len(selected) >= num_select:
                break

        return selected


def get_random_layout_seed() -> int:
    """
    Ottiene seed deterministico basato su tempo
    Cambia ogni ora

    Returns:
        Numero seed
    """
    return int(datetime.now().timestamp() / 3600)


def is_layout_changed() -> bool:
    """
    Verifica se il layout è cambiato dall'ultimo reload
    (seed è cambiato)

    Returns:
        True se seed è nuovo
    """
    current_seed = get_random_layout_seed()

    if "last_layout_seed" not in globals():
        return True

    return current_seed != globals()["last_layout_seed"]


def create_dynamic_kpi_grid(metrics: List[Dict], layout_engine) -> Dict:
    """
    Crea grid dinamica per KPI con numero colonne adattato

    Args:
        metrics: Lista metriche disponibili
        layout_engine: Motore layout responsivo

    Returns:
        Configurazione grid
    """
    randomizer = LayoutRandomizer()

    # Numero di KPI da mostrare
    kpi_range = layout_engine.get_kpi_range()
    num_kpis = random.randint(kpi_range[0], kpi_range[1])

    # Seleziona KPI
    selected_kpis = randomizer.select_visible_kpis(metrics, num_kpis)

    # Numero colonne
    num_cols = layout_engine.get_kpi_columns()

    return {
        "kpis": selected_kpis,
        "num_cols": num_cols,
        "num_kpis": len(selected_kpis),
        "randomizer": randomizer,
    }


def create_dynamic_chart_grid(charts: List[Dict], layout_engine) -> Dict:
    """
    Crea grid dinamica per charts con numero e disposizione variabili

    Args:
        charts: Lista grafici disponibili
        layout_engine: Motore layout responsivo

    Returns:
        Configurazione grid
    """
    randomizer = LayoutRandomizer()

    # Numero di chart da mostrare
    num_cols = layout_engine.get_chart_columns()
    max_charts = num_cols * 3  # Max 3 righe
    num_charts = random.randint(max(2, num_cols), min(max_charts, len(charts)))

    # Seleziona charts
    selected_charts = randomizer.select_chart_types(charts, num_charts)

    # Disposizione
    arrangement = randomizer.randomize_chart_arrangement(len(selected_charts), num_cols)

    # Template
    template = randomizer.select_layout_template(num_charts)

    return {
        "charts": selected_charts,
        "num_cols": num_cols,
        "arrangement": arrangement,
        "template": template,
        "randomizer": randomizer,
    }
