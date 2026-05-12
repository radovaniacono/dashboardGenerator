"""
Layout Randomizer - Randomizza il layout mantenendo qualità e coerenza
Fornisce freschezza visiva ad ogni caricamento della dashboard
"""

import random
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple, Optional
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


class AdvancedLayoutRandomizer:
    """
    Versione avanzata del Layout Randomizer con controlli di coerenza
    Crea layout sempre diversi mantenendo UX coerente
    """

    def __init__(
        self, num_kpis: int = 0, num_charts: int = 0, viewport_width: int = 1024
    ):
        """
        Inizializza il randomizer avanzato

        Args:
            num_kpis: Numero KPI disponibili
            num_charts: Numero charts disponibili
            viewport_width: Larghezza viewport in pixel
        """
        self.num_kpis = num_kpis
        self.num_charts = num_charts
        self.viewport_width = viewport_width
        self.seed = int(datetime.now().timestamp() / 3600)
        random.seed(self.seed)

    def generate_layout(self) -> Dict:
        """
        Genera configurazione layout completa, casuale ma bilanciata

        Returns:
            Dizionario con configurazione layout
        """
        layout = {
            "kpi_section": self._generate_kpi_layout(),
            "chart_section": self._generate_chart_layout(),
            "table_section": self._generate_table_layout(),
            "color_theme": self._select_color_theme(),
            "spacing": self._calculate_spacing(),
            "animations": self._select_animations(),
            "seed": self.seed,
        }

        return layout

    def _generate_kpi_layout(self) -> Dict:
        """Genera layout casuale per KPI grid"""

        # Numero colonne basato su viewport
        if self.viewport_width < 768:
            num_cols = random.choice([1, 2])
        elif self.viewport_width < 1200:
            num_cols = random.choice([2, 3])
        else:
            num_cols = random.choice([3, 4])

        # Numero KPI da mostrare (4-8)
        num_display = (
            random.randint(4, min(8, self.num_kpis)) if self.num_kpis > 0 else 4
        )

        # Ordine casuale
        kpi_order = list(range(min(num_display, self.num_kpis)))
        random.shuffle(kpi_order)

        return {
            "columns": num_cols,
            "order": kpi_order,
            "count": num_display,
            "gap": random.choice([16, 20, 24]),
            "animation": random.choice(["fade", "slide", "scale"]),
            "card_height": random.choice(["auto", "150px", "180px"]),
        }

    def _generate_chart_layout(self) -> List[Dict]:
        """Genera layout casuale per charts"""

        charts = []
        remaining_charts = self.num_charts

        while remaining_charts > 0:
            # Numero colonne per questa riga
            if self.viewport_width < 768:
                cols = 1
            elif self.viewport_width < 1200:
                cols = min(remaining_charts, random.choice([1, 2]))
            else:
                cols = min(remaining_charts, random.choice([2, 2, 3]))

            charts.append(
                {
                    "columns": cols,
                    "gap": random.choice([16, 20]),
                    "height": random.choice([400, 450, 500]),
                    "aspect_ratio": random.choice(["auto", "16/9", "4/3"]),
                }
            )

            remaining_charts -= cols

        return charts

    def _generate_table_layout(self) -> Dict:
        """Genera layout per tabella"""

        return {
            "position": "bottom",
            "visible_rows": random.choice([10, 15, 20]),
            "striped": random.choice([True, False]),
            "hover_effect": True,
            "pagination": True,
        }

    def _select_color_theme(self) -> Dict[str, str]:
        """Seleziona tema colori casuale ma accessibile"""

        themes = [
            {
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f59e0b",
                "success": "#10b981",
                "danger": "#ef4444",
                "name": "blue-purple",
            },
            {
                "primary": "#3b82f6",
                "secondary": "#1e40af",
                "accent": "#10b981",
                "success": "#059669",
                "danger": "#dc2626",
                "name": "blue-green",
            },
            {
                "primary": "#6366f1",
                "secondary": "#4f46e5",
                "accent": "#ec4899",
                "success": "#10b981",
                "danger": "#ef4444",
                "name": "indigo-pink",
            },
            {
                "primary": "#10b981",
                "secondary": "#059669",
                "accent": "#f59e0b",
                "success": "#34d399",
                "danger": "#ef4444",
                "name": "green-amber",
            },
        ]

        return random.choice(themes)

    def _calculate_spacing(self) -> Dict[str, int]:
        """Calcola spacing adattativo"""

        return {
            "header_margin": random.choice([20, 24, 28]),
            "section_gap": random.choice([32, 40, 48]),
            "element_padding": random.choice([12, 16, 20]),
            "border_radius": random.choice([8, 10, 12]),
        }

    def _select_animations(self) -> Dict[str, str]:
        """Seleziona animazioni"""

        return {
            "entrance": random.choice(["fade-in", "slide-up", "zoom-in"]),
            "interaction": random.choice(["subtle", "smooth", "playful"]),
            "transition_speed": random.choice(["fast", "normal", "slow"]),
        }

    def validate_layout(self, layout: Dict) -> bool:
        """Valida che layout sia equilibrato e usabile"""

        checks = {
            "min_kpis_visible": layout["kpi_section"]["count"] >= 4,
            "charts_present": len(layout["chart_section"]) > 0,
            "reading_flow": True,  # KPI prima di charts
            "max_height": self._calculate_total_height(layout) < 5000,
        }

        return all(checks.values())

    def _calculate_total_height(self, layout: Dict) -> int:
        """Calcola altezza totale della pagina"""

        total = 100  # Header
        total += 60  # Filter bar
        total += layout["kpi_section"]["count"] * 150 / layout["kpi_section"]["columns"]

        for chart in layout["chart_section"]:
            total += chart["height"]

        total += 400  # Table

        return int(total)


class LayoutBalancer:
    """Assicura che layout casuale rimane equilibrato e usabile"""

    @staticmethod
    def validate_kpi_layout(num_kpis: int, num_cols: int) -> bool:
        """Verifica che KPI layout non sia squilibrato"""
        # KPI per colonna non deve essere troppo pochi o troppi
        kpis_per_col = num_kpis / num_cols
        return 1 <= kpis_per_col <= 4

    @staticmethod
    def adjust_spacing(num_cols: int) -> int:
        """Spacing adattativo basato su numero colonne"""
        spacing_map = {1: 24, 2: 20, 3: 16, 4: 12}
        return spacing_map.get(num_cols, 16)

    @staticmethod
    def validate_chart_distribution(charts: List[Dict], viewport_width: int) -> bool:
        """Verifica che charts siano distribuiti equilibratamente"""

        # Almeno 1 chart per riga
        for row in charts:
            if row["columns"] < 1:
                return False

        # Non più di 3 colonne su mobile
        if viewport_width < 768:
            return all(row["columns"] <= 1 for row in charts)

        return True


class LayoutMemory:
    """Permette agli utenti di salvare e ricaricare layout preferiti"""

    def __init__(self, storage_path: str = ".layout_cache"):
        self.storage_path = storage_path
        self.layouts = {}

    def save_layout(self, layout_id: str, layout: Dict) -> bool:
        """Salva un layout con ID"""
        try:
            self.layouts[layout_id] = {
                "layout": layout,
                "created_at": datetime.now().isoformat(),
            }
            return True
        except Exception as e:
            print(f"Errore salvataggio layout: {e}")
            return False

    def load_layout(self, layout_id: str) -> Optional[Dict]:
        """Carica un layout precedentemente salvato"""
        if layout_id in self.layouts:
            return self.layouts[layout_id]["layout"]
        return None

    def delete_layout(self, layout_id: str) -> bool:
        """Elimina un layout salvato"""
        if layout_id in self.layouts:
            del self.layouts[layout_id]
            return True
        return False

    def list_saved_layouts(self) -> List[str]:
        """Elenca tutti i layout salvati"""
        return list(self.layouts.keys())
