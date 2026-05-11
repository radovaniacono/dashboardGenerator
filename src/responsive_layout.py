"""
Responsive Layout Engine - Gestisce il layout responsivo della dashboard
Adatta automaticamente il layout in base alla risoluzione dello schermo
"""

import streamlit as st
from typing import Dict, Tuple, List


class ResponsiveLayoutConfig:
    """Configurazioni di layout per ogni breakpoint"""

    BREAKPOINTS = {
        "xl": 1920,  # Extra Large
        "lg": 1366,  # Large
        "md": 768,  # Medium
        "sm": 375,  # Small
        "xs": 0,  # Extra Small
    }

    CHART_COLUMNS = {"xl": 4, "lg": 3, "md": 2, "sm": 1, "xs": 1}

    KPI_COLUMNS = {"xl": 4, "lg": 3, "md": 2, "sm": 1, "xs": 1}

    KPI_RANGE = {
        "xl": (5, 8),  # Min, Max KPI visibili
        "lg": (4, 6),
        "md": (3, 4),
        "sm": (2, 3),
        "xs": (1, 2),
    }


class ResponsiveLayoutEngine:
    """
    Motore di layout responsivo intelligente
    Detecta viewport e fornisce configurazioni appropriate
    """

    def __init__(self):
        self.config = ResponsiveLayoutConfig()
        self.current_breakpoint = self._detect_breakpoint()

    def _detect_breakpoint(self) -> str:
        """
        Detecta il breakpoint corrente
        Per ora usa una media standard, ma può essere esteso con JS
        """
        # In produzione, integra con script JS per viewport reale
        # Per ora usa cookie o guess dalla config Streamlit
        if "viewport_width" in st.session_state:
            width = st.session_state["viewport_width"]
        else:
            # Default conservative
            width = 1366

        for breakpoint in ["xl", "lg", "md", "sm", "xs"]:
            if width >= self.config.BREAKPOINTS[breakpoint]:
                return breakpoint
        return "xs"

    def get_breakpoint(self) -> str:
        """Restituisce il breakpoint corrente"""
        return self._detect_breakpoint()

    def get_chart_columns(self, breakpoint: str = None) -> int:
        """
        Ottiene numero colonne per i grafici

        Args:
            breakpoint: Nome breakpoint (default: current)

        Returns:
            Numero di colonne (1-4)
        """
        bp = breakpoint or self.get_breakpoint()
        return self.config.CHART_COLUMNS.get(bp, 1)

    def get_kpi_columns(self, breakpoint: str = None) -> int:
        """
        Ottiene numero colonne per i KPI

        Args:
            breakpoint: Nome breakpoint (default: current)

        Returns:
            Numero di colonne (1-4)
        """
        bp = breakpoint or self.get_breakpoint()
        return self.config.KPI_COLUMNS.get(bp, 1)

    def get_kpi_range(self, breakpoint: str = None) -> Tuple[int, int]:
        """
        Ottiene range di KPI da mostrare

        Args:
            breakpoint: Nome breakpoint (default: current)

        Returns:
            Tupla (min_kpis, max_kpis)
        """
        bp = breakpoint or self.get_breakpoint()
        return self.config.KPI_RANGE.get(bp, (2, 3))

    def get_layout_config(self, breakpoint: str = None) -> Dict:
        """
        Restituisce configurazione completa di layout

        Args:
            breakpoint: Nome breakpoint (default: current)

        Returns:
            Dizionario con tutte le configurazioni
        """
        bp = breakpoint or self.get_breakpoint()

        return {
            "breakpoint": bp,
            "chart_columns": self.get_chart_columns(bp),
            "kpi_columns": self.get_kpi_columns(bp),
            "kpi_range": self.get_kpi_range(bp),
            "is_mobile": bp in ["sm", "xs"],
            "is_tablet": bp == "md",
            "is_desktop": bp in ["lg", "xl"],
        }

    def render_responsive_css(self):
        """
        Renderizza CSS responsivo per il layout
        """
        css = """
        <style>
        :root {
            --color-primary: #667eea;
            --color-secondary: #764ba2;
            --color-success: #10b981;
            --color-danger: #ef4444;
            --color-warning: #f59e0b;
            --color-bg-primary: #ffffff;
            --color-bg-secondary: #f3f4f6;
            --color-text-primary: #1f2937;
            --color-text-secondary: #6b7280;
            
            --spacing-xs: 4px;
            --spacing-sm: 8px;
            --spacing-md: 16px;
            --spacing-lg: 24px;
            --spacing-xl: 32px;
            
            --radius-sm: 4px;
            --radius-md: 8px;
            --radius-lg: 12px;
        }
        
        body {
            font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--color-text-primary);
            background-color: var(--color-bg-secondary);
            line-height: 1.6;
        }
        
        /* Grid Responsive */
        .responsive-grid {
            display: grid;
            gap: var(--spacing-lg);
            width: 100%;
        }
        
        /* Extra Large (1920px+) */
        @media (min-width: 1920px) {
            .responsive-grid.chart-grid {
                grid-template-columns: repeat(4, 1fr);
            }
            .responsive-grid.kpi-grid {
                grid-template-columns: repeat(4, 1fr);
            }
            .responsive-grid.metric-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        /* Large (1366px-1919px) */
        @media (min-width: 1366px) and (max-width: 1919px) {
            .responsive-grid.chart-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            .responsive-grid.kpi-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            .responsive-grid.metric-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        /* Medium (768px-1365px) */
        @media (min-width: 768px) and (max-width: 1365px) {
            .responsive-grid.chart-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .responsive-grid.kpi-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .responsive-grid.metric-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Small (375px-767px) */
        @media (max-width: 767px) {
            .responsive-grid.chart-grid {
                grid-template-columns: 1fr;
            }
            .responsive-grid.kpi-grid {
                grid-template-columns: 1fr;
            }
            .responsive-grid.metric-grid {
                grid-template-columns: 1fr;
            }
            
            /* Compatta filtri su mobile */
            .filter-bar {
                display: flex;
                flex-direction: column;
                gap: var(--spacing-sm);
            }
            
            .filter-item {
                width: 100%;
            }
        }
        
        /* Card Styles */
        .card {
            background: var(--color-bg-primary);
            border-radius: var(--radius-md);
            padding: var(--spacing-lg);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* KPI Card */
        .kpi-card {
            background: var(--color-bg-primary);
            border-left: 4px solid var(--color-primary);
            border-radius: var(--radius-md);
            padding: var(--spacing-lg);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .kpi-card.positive {
            border-left-color: var(--color-success);
        }
        
        .kpi-card.negative {
            border-left-color: var(--color-danger);
        }
        
        .kpi-card.neutral {
            border-left-color: var(--color-primary);
        }
        
        .kpi-card.warning {
            border-left-color: var(--color-warning);
        }
        
        /* Typography */
        .text-mono {
            font-family: 'IBM Plex Mono', monospace;
        }
        
        .text-center {
            text-align: center;
        }
        
        .text-muted {
            color: var(--color-text-secondary);
        }
        
        /* Accessibility */
        :focus {
            outline: 3px solid var(--color-primary);
            outline-offset: 2px;
        }
        
        /* Dark Mode Support */
        @media (prefers-color-scheme: dark) {
            body {
                background-color: #1f2937;
                color: #f3f4f6;
            }
            
            .card {
                background: #374151;
            }
            
            .kpi-card {
                background: #374151;
            }
        }
        
        /* Reduced Motion Support */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation: none !important;
                transition: none !important;
            }
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def get_col_widths(self) -> List[float]:
        """
        Restituisce i pesi relativi delle colonne
        Utile per st.columns() con pesi dinamici

        Returns:
            Lista di pesi per st.columns()
        """
        bp = self.get_breakpoint()
        cols = self.get_chart_columns(bp)

        if cols == 1:
            return [1]
        elif cols == 2:
            return [1, 1]
        elif cols == 3:
            return [1, 1, 1]
        else:  # 4
            return [1, 1, 1, 1]


def inject_viewport_detector():
    """
    Injetta script JS per detectare viewport width
    Richiede streamlit_js_eval o simile
    """
    js_code = """
    <script>
    try {
        const width = window.innerWidth;
        window.parent.streamlit.setComponentValue(width);
    } catch (e) {
        console.log('Viewport detection failed:', e);
    }
    </script>
    """
    # Questo richiede estensione Streamlit custom
    # Per ora uso fallback
    st.markdown("<!-- Viewport detection loaded -->", unsafe_allow_html=True)


def create_responsive_columns(
    num_cols: int = None, vertical_spacing: bool = True
) -> list:
    """
    Crea colonne responsive in base al breakpoint

    Args:
        num_cols: Numero colonne desiderate (opzionale)
        vertical_spacing: Aggiunge spacing verticale tra colonne

    Returns:
        Lista di colonne Streamlit
    """
    engine = ResponsiveLayoutEngine()

    if num_cols is None:
        num_cols = engine.get_chart_columns()
    else:
        num_cols = min(num_cols, engine.get_chart_columns())

    cols = st.columns(num_cols)

    if vertical_spacing:
        st.markdown("")  # Spacing

    return cols
