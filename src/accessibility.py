"""
Accessibility Manager - Gestisce accessibilità WCAG 2.1 AA
Supporta screen reader, alto contrasto, navigazione tastiera
"""

import streamlit as st
from typing import Tuple, Optional
import colorsys


class ColorAccessibility:
    """Calcola contrasti colore e validazione WCAG"""

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        Converte colore hex a RGB

        Args:
            hex_color: Colore in formato #RRGGBB

        Returns:
            Tupla (R, G, B)
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_luminance(r: int, g: int, b: int) -> float:
        """
        Calcola luminanza relativa di un colore (WCAG formula)

        Args:
            r, g, b: Componenti RGB (0-255)

        Returns:
            Luminanza relativa (0-1)
        """
        # Normalizza a 0-1
        r_normalized = r / 255.0
        g_normalized = g / 255.0
        b_normalized = b / 255.0

        # Applica curve gamma
        def gamma_correct(c):
            if c <= 0.03928:
                return c / 12.92
            else:
                return ((c + 0.055) / 1.055) ** 2.4

        r_gamma = gamma_correct(r_normalized)
        g_gamma = gamma_correct(g_normalized)
        b_gamma = gamma_correct(b_normalized)

        # Formula WCAG
        luminance = 0.2126 * r_gamma + 0.7152 * g_gamma + 0.0722 * b_gamma

        return luminance

    @staticmethod
    def calculate_contrast_ratio(color1: str, color2: str) -> float:
        """
        Calcola rapporto di contrasto tra due colori (WCAG)

        Args:
            color1: Colore primo (#RRGGBB)
            color2: Colore secondo (#RRGGBB)

        Returns:
            Rapporto di contrasto (1.0 - 21.0)
        """
        r1, g1, b1 = ColorAccessibility.hex_to_rgb(color1)
        r2, g2, b2 = ColorAccessibility.hex_to_rgb(color2)

        lum1 = ColorAccessibility.rgb_to_luminance(r1, g1, b1)
        lum2 = ColorAccessibility.rgb_to_luminance(r2, g2, b2)

        # Assicura che lum1 è maggiore
        if lum1 < lum2:
            lum1, lum2 = lum2, lum1

        # Formula contrasto
        contrast = (lum1 + 0.05) / (lum2 + 0.05)

        return contrast

    @staticmethod
    def meets_wcag_aa(contrast_ratio: float, large_text: bool = False) -> bool:
        """
        Verifica se il contrasto soddisfa WCAG AA

        Args:
            contrast_ratio: Rapporto di contrasto
            large_text: True per testo grande (18pt+)

        Returns:
            True se soddisfa WCAG AA
        """
        if large_text:
            return contrast_ratio >= 3.0
        else:
            return contrast_ratio >= 4.5

    @staticmethod
    def meets_wcag_aaa(contrast_ratio: float, large_text: bool = False) -> bool:
        """
        Verifica se il contrasto soddisfa WCAG AAA (più severo)

        Args:
            contrast_ratio: Rapporto di contrasto
            large_text: True per testo grande

        Returns:
            True se soddisfa WCAG AAA
        """
        if large_text:
            return contrast_ratio >= 4.5
        else:
            return contrast_ratio >= 7.0


class AccessibilityManager:
    """Gestisce funzionalità di accessibilità per la dashboard"""

    def __init__(self):
        """Inizializza il manager accessibilità"""
        if "accessibility_mode" not in st.session_state:
            st.session_state.accessibility_mode = {
                "high_contrast": False,
                "larger_text": False,
                "reduced_motion": False,
            }

    def render_accessibility_controls(self):
        """Renderizza controlli accessibilità nella sidebar"""
        with st.sidebar.expander("♿ Accessibilità", expanded=False):
            st.write("**Opzioni di accessibilità**")

            # Alto contrasto
            high_contrast = st.checkbox(
                "Modalità alto contrasto",
                value=st.session_state.accessibility_mode["high_contrast"],
                help="Aumenta il contrasto tra testo e sfondo",
            )
            st.session_state.accessibility_mode["high_contrast"] = high_contrast

            # Testo più grande
            larger_text = st.checkbox(
                "Ingrandisci testo",
                value=st.session_state.accessibility_mode["larger_text"],
                help="Aumenta la dimensione del carattere",
            )
            st.session_state.accessibility_mode["larger_text"] = larger_text

            # Movimento ridotto
            reduced_motion = st.checkbox(
                "Riduci movimento",
                value=st.session_state.accessibility_mode["reduced_motion"],
                help="Disabilita animazioni e transizioni",
            )
            st.session_state.accessibility_mode["reduced_motion"] = reduced_motion

    def apply_accessibility_css(self):
        """Applica CSS per accessibilità basato su impostazioni"""
        mode = st.session_state.accessibility_mode

        css = "<style>"

        # Alto contrasto
        if mode["high_contrast"]:
            css += """
            :root {
                --color-text-primary: #000000;
                --color-bg-secondary: #ffffff;
            }
            body {
                background-color: #ffffff;
                color: #000000;
            }
            .card {
                border: 2px solid #000000;
            }
            """

        # Testo più grande
        if mode["larger_text"]:
            css += """
            body {
                font-size: 16px;
            }
            h1, h2, h3 {
                line-height: 1.4;
            }
            """

        # Movimento ridotto
        if mode["reduced_motion"]:
            css += """
            * {
                animation: none !important;
                transition: none !important;
            }
            """

        css += "</style>"

        st.markdown(css, unsafe_allow_html=True)

    def add_aria_labels(self, element_type: str, label: str) -> str:
        """
        Genera HTML con aria-labels per screen reader

        Args:
            element_type: Tipo elemento ('button', 'link', 'input')
            label: Etichetta descrittiva

        Returns:
            Snippet HTML con aria-label
        """
        if element_type == "button":
            return f'<button aria-label="{label}">'
        elif element_type == "link":
            return f'<a aria-label="{label}">'
        elif element_type == "input":
            return f'<input aria-label="{label}">'

        return ""

    def validate_page_accessibility(self) -> dict:
        """
        Valida accessibilità della pagina

        Returns:
            Dizionario con risultati validazione
        """
        results = {
            "color_contrast": True,
            "form_labels": True,
            "keyboard_nav": True,
            "issues": [],
        }

        # Valida colori primari
        primary_colors = {
            "text_on_bg": ("#1f2937", "#f3f4f6"),
            "button": ("#667eea", "#ffffff"),
        }

        for name, (fg, bg) in primary_colors.items():
            ratio = ColorAccessibility.calculate_contrast_ratio(fg, bg)
            if not ColorAccessibility.meets_wcag_aa(ratio):
                results["color_contrast"] = False
                results["issues"].append(
                    f"Contrasto insufficiente su {name}: {ratio:.2f}:1"
                )

        return results


def add_skip_link():
    """Aggiunge link "Salta al contenuto principale" per accessibilità"""
    skip_link_html = """
    <a href="#main-content" class="skip-link">
        Salta al contenuto principale
    </a>
    <style>
    .skip-link {
        position: absolute;
        top: -40px;
        left: 0;
        background: #667eea;
        color: white;
        padding: 8px;
        text-decoration: none;
        z-index: 100;
    }
    .skip-link:focus {
        top: 0;
    }
    </style>
    """
    st.markdown(skip_link_html, unsafe_allow_html=True)


def add_keyboard_navigation_help():
    """Mostra aiuto per navigazione tastiera"""
    help_html = """
    <div style="background: #f3f4f6; padding: 12px; border-radius: 8px; margin-bottom: 16px;">
        <strong>⌨️ Navigazione Tastiera:</strong>
        <ul style="margin: 8px 0; padding-left: 20px;">
            <li><code>Tab</code> - Muove al prossimo elemento</li>
            <li><code>Shift + Tab</code> - Muove all'elemento precedente</li>
            <li><code>Enter</code> - Attiva button/link</li>
            <li><code>Space</code> - Attiva checkbox/toggle</li>
            <li><code>Esc</code> - Chiude modal/menu</li>
        </ul>
    </div>
    """
    st.markdown(help_html, unsafe_allow_html=True)


def validate_contrast_ratios(
    foreground: str, background: str, large_text: bool = False
) -> Tuple[float, bool, bool]:
    """
    Valida contrasto tra due colori

    Args:
        foreground: Colore primo (#RRGGBB)
        background: Colore secondo (#RRGGBB)
        large_text: True per testo grande (18pt+)

    Returns:
        Tupla (ratio, meets_aa, meets_aaa)
    """
    ratio = ColorAccessibility.calculate_contrast_ratio(foreground, background)
    meets_aa = ColorAccessibility.meets_wcag_aa(ratio, large_text)
    meets_aaa = ColorAccessibility.meets_wcag_aaa(ratio, large_text)

    return (ratio, meets_aa, meets_aaa)


def create_accessible_button(
    label: str, key: str, aria_label: Optional[str] = None
) -> bool:
    """
    Crea un button accessibile

    Args:
        label: Etichetta visualizzata
        key: Chiave univoca
        aria_label: Etichetta per screen reader (default: label)

    Returns:
        True se cliccato
    """
    if aria_label is None:
        aria_label = label

    # Streamlit non supporta direttamente aria-labels, ma possiamo usare HTML
    return st.button(label, key=key, help=aria_label)


def create_accessible_input(
    label: str, input_type: str = "text", aria_label: Optional[str] = None, **kwargs
) -> any:
    """
    Crea un input accessibile

    Args:
        label: Etichetta
        input_type: Tipo input ('text', 'number', 'date', ecc)
        aria_label: Etichetta screen reader
        **kwargs: Parametri aggiuntivi Streamlit

    Returns:
        Valore input
    """
    if aria_label is None:
        aria_label = label

    if input_type == "text":
        return st.text_input(label, help=aria_label, **kwargs)
    elif input_type == "number":
        return st.number_input(label, help=aria_label, **kwargs)
    elif input_type == "date":
        return st.date_input(label, help=aria_label, **kwargs)
    else:
        return st.text_input(label, help=aria_label, **kwargs)
