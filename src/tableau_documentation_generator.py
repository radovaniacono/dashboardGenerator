"""
Tableau Documentation Generator - Crea guide automatiche per ricreate i grafici su Tableau
Genera documentazione passo-passo con istruzioni per ogni tipo di grafico
"""

import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime


class TableauDocumentationGenerator:
    """Genera documentazione Tableau automatica basata sulla dashboard creata"""

    def __init__(self, df: pd.DataFrame, title: str = "Dashboard"):
        """
        Inizializza il generatore di documentazione

        Args:
            df: DataFrame con i dati
            title: Titolo della dashboard
        """
        self.df = df
        self.title = title
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def generate_tableau_guide(
        self, charts: List[Dict] = None, kpis: List[Dict] = None
    ) -> str:
        """
        Genera una guida completa per creare la dashboard su Tableau

        Args:
            charts: Lista di grafici con info
            kpis: Lista di KPI

        Returns:
            str: Documentazione Markdown completa
        """
        guide = f"""# 📊 GUIDA TABLEAU - Come Ricreate Questa Dashboard

**Dashboard**: {self.title}  
**Data Generazione**: {self.timestamp}  
**Righe Dati**: {len(self.df):,}  
**Colonne**: {len(self.df.columns)}

---

## 📋 Indice

1. [Preparazione Dati](#preparazione-dati)
2. [Creazione KPI](#creazione-kpi)
3. [Grafici Passo-Passo](#grafici-passo-passo)
4. [Tips & Tricks](#tips--tricks)

---

## 🔧 Preparazione Dati

### Step 1: Importare il Dataset

1. Apri **Tableau Desktop**
2. Clicca su **Connect → File → CSV**
3. Seleziona il file `data.csv` dalla cartella export
4. Tableau caricherà il dataset automaticamente

**⚠️ Importante**: Verifica che i tipi di dato siano corretti:

| Colonna | Tipo Atteso | Come Fare |
|---------|------------|----------|
| Date/Time | Data | Clicca sulla colonna → Change Data Type → Date |
| Valori monetari | Numero | Clicca sulla colonna → Change Data Type → Number |
| Categorie | Testo | Clicca sulla colonna → Change Data Type → String |

---

## 💰 Creazione KPI

### Come Creare KPI Dinamici su Tableau

"""

        # Aggiungi sezione KPI se forniti
        if kpis:
            guide += self._generate_kpi_section(kpis)
        else:
            guide += self._generate_generic_kpi_section()

        # Aggiungi sezione grafici
        guide += "\n---\n\n## 📈 Grafici Passo-Passo\n\n"

        if charts:
            for i, chart in enumerate(charts, 1):
                chart_type = chart.get("type", "Unknown").lower()
                guide += self._generate_chart_guide(chart, i)
        else:
            guide += self._generate_all_chart_types_guide()

        # Aggiungi tips
        guide += self._generate_tips_section()

        return guide

    def _generate_kpi_section(self, kpis: List[Dict]) -> str:
        """Genera sezione KPI basata su KPI effettivi"""
        section = ""

        for i, kpi in enumerate(kpis, 1):
            name = kpi.get("name", f"KPI {i}")
            value = kpi.get("value", "N/A")
            description = kpi.get("description", "")

            section += f"""
### KPI {i}: {name}

**Valore**: {value}  
**Descrizione**: {description}

**Come Creare su Tableau**:

1. Clicca su **Analysis → Create Calculated Field**
2. Nome: `{name}`
3. Formula:
   ```
   SUM([Campo Rilevante])
   ```
4. Clicca **OK**
5. Trascina il campo calcolato su **Text** nella vista
6. Formatta con Number Format (se monetario)

---
"""
        return section

    def _generate_generic_kpi_section(self) -> str:
        """Genera sezione KPI generica con best practices"""
        return """
### KPI 1: Totale Vendite

**Come Creare**:

1. Analysis → Create Calculated Field
2. Nome: `Total Sales`
3. Formula: `SUM([Sales])`
4. Clicca OK
5. Trascina su Text nella vista
6. Formatta a numero con separatore migliaia

### KPI 2: Media per Transazione

**Come Creare**:

1. Analysis → Create Calculated Field
2. Nome: `Avg Transaction`
3. Formula: `AVG([Sales])`
4. Clicca OK
5. Trascina su Text

### KPI 3: Numero Transazioni

**Come Creare**:

1. Analysis → Create Calculated Field
2. Nome: `Count Orders`
3. Formula: `COUNT([Order ID])`
4. Clicca OK
5. Trascina su Text

---
"""

    def _generate_chart_guide(self, chart: Dict, index: int) -> str:
        """Genera guida per un singolo grafico"""
        chart_type = chart.get("type", "Unknown").lower()
        x_field = chart.get("x_field", "Categoria")
        y_field = chart.get("y_field", "Valore")
        description = chart.get("description", "")

        guides = {
            "line": self._guide_line_chart,
            "bar": self._guide_bar_chart,
            "scatter": self._guide_scatter_chart,
            "pie": self._guide_pie_chart,
            "heatmap": self._guide_heatmap,
            "bubble": self._guide_bubble_chart,
            "histogram": self._guide_histogram,
            "boxplot": self._guide_boxplot,
            "treemap": self._guide_treemap,
            "radar": self._guide_radar,
            "violin": self._guide_violin,
            "area": self._guide_area_chart,
        }

        guide_func = guides.get(chart_type, self._guide_generic_chart)
        return guide_func(index, x_field, y_field, description)

    def _guide_line_chart(
        self, index: int, x_field: str, y_field: str, desc: str
    ) -> str:
        return f"""
### Grafico {index}: Linea (Trend nel Tempo)

**Tipo**: Line Chart  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Mostrare trend temporali"}

**Come Creare su Tableau**:

**Step 1: Prepara i Dati**
- Devi avere una colonna DATA e una colonna di VALORI numerici
- Esempio: Data (Asse X) vs Vendite (Asse Y)

**Step 2: Crea la Visualizzazione**
1. Clicca su **Rows** → Trascina il campo DATA
2. Clicca su **Columns** → Trascina il campo VALORI
3. Tableau assegna automaticamente il grafico
4. Se non è una linea, clicca su **Mark Type** → scegli **Line**

**Step 3: Formattazione**
```
Color: Blu gradiente
Size: Medio
Label: Mostra valori
Tooltip: Includi Data e Valore
```

**Step 4: Personalizza**
- Right-click sulla linea → Format → Colors
- Scegli "Sequential" per trend crescenti
- Aggiungi trend line: Analysis → Trend Line

---
"""

    def _guide_bar_chart(
        self, index: int, x_field: str, y_field: str, desc: str
    ) -> str:
        return f"""
### Grafico {index}: Barre (Confronto Categorie)

**Tipo**: Bar Chart  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Confrontare valori tra categorie"}

**Come Creare su Tableau**:

**Step 1: Setup Base**
1. Trascina categoria (es. "Regione") su **Rows**
2. Trascina valore numerico (es. "Vendite") su **Columns**
3. Tableau crea automaticamente il bar chart

**Step 2: Ordina e Filtra**
- Right-click sul campo ROWS → Sort → By Field (discendente)
- Clicca **Filters** → aggiungi filtri per categorie

**Step 3: Colori**
1. Trascina il campo categoria anche su **Color**
2. Scegli una palette di colori (Hue, Saturation, etc.)
3. Regola brightness per leggibilità

**Step 4: Etichette**
- Clicca **Label** → scegli **Show Mark Labels**
- Format → Numeri con separatore migliaia

---
"""

    def _guide_scatter_chart(
        self, index: int, x_field: str, y_field: str, desc: str
    ) -> str:
        return f"""
### Grafico {index}: Scatter Plot (Correlazione)

**Tipo**: Scatter Plot  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Mostrare correlazione tra due variabili"}

**Come Creare su Tableau**:

**Step 1: Setup**
1. Trascina prima variabile su **Columns** (asse X)
2. Trascina seconda variabile su **Rows** (asse Y)
3. Mark Type → **Circle**

**Step 2: Aggiungi Dimensioni**
- Trascina una terza colonna su **Size** per rappresentare grandezza
- Trascina una categoria su **Color** per raggruppare

**Step 3: Analisi Correlazione**
- Analysis → Trend Line → Linear
- Questo mostra la retta di regressione

**Step 4: Interattività**
- Aggiungi tooltip con info dettagliate
- Customers → Fields → Trascina su Tooltip

---
"""

    def _guide_pie_chart(
        self, index: int, x_field: str, y_field: str, desc: str
    ) -> str:
        return f"""
### Grafico {index}: Torta (Composizione)

**Tipo**: Pie Chart  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Mostrare composizione percentuale"}

**Come Creare su Tableau**:

**Step 1: Base**
1. Trascina categoria su **Rows**
2. Trascina valore su **Columns**
3. Mark Type → **Pie**

**Step 2: Personalizza**
- Trascina categoria anche su **Color** per fette colorate
- Clicca **Label** → **Show Mark Labels**
- Format → Aggiungi %

**Step 3: Limita Fette**
- Filtro sulla top 5 categorie
- Altre raggruppate come "Altro"

**⚠️ Nota**: Massimo 5-7 fette per leggibilità!

---
"""

    def _guide_heatmap(self, index: int, x_field: str, y_field: str, desc: str) -> str:
        return f"""
### Grafico {index}: Heatmap (Matrice)

**Tipo**: Heatmap  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Mostrare intensità valori in matrice"}

**Come Creare su Tableau**:

**Step 1: Setup**
1. Trascina prima categoria su **Columns**
2. Trascina seconda categoria su **Rows**
3. Trascina valore su **Color**
4. Mark Type → **Square**

**Step 2: Scala Colori**
- Color → Edit Colors
- Scegli "Diverging" per contrasto
- Es: Blu (basso) → Rosso (alto)

**Step 3: Etichette**
- Label → Show Mark Labels
- Format → 0 decimali

**Step 4: Interattività**
- Aggiungi Tooltip con valore esatto

---
"""

    def _guide_bubble_chart(
        self, index: int, x_field: str, y_field: str, desc: str
    ) -> str:
        return f"""
### Grafico {index}: Bubble Chart (3+ Dimensioni)

**Tipo**: Bubble Chart  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Mostrare 3+ dimensioni simultaneamente"}

**Come Creare su Tableau**:

**Step 1: Setup**
1. Trascina var. 1 su **Columns**
2. Trascina var. 2 su **Rows**
3. Trascina var. 3 su **Size**
4. Mark Type → **Circle**

**Step 2: Colore**
- Trascina var. 4 su **Color** (opzionale)
- Crea legenda aggiuntiva

**Step 3: Formato**
- Size → Edit Sizes
- Regola min/max per visibilità
- Aggiungi Stroke (bordo) per separare bolle

---
"""

    def _guide_histogram(
        self, index: int, x_field: str, y_field: str, desc: str
    ) -> str:
        return f"""
### Grafico {index}: Istogramma (Distribuzione)

**Tipo**: Histogram  
**Dati**: {x_field}  
**Uso**: {desc or "Mostrare distribuzione di una variabile"}

**Come Creare su Tableau**:

**Step 1: Setup**
1. Clicca destro sul campo numerico
2. Create Bin (crea intervalli)
3. Size of bins: 10 (regola se necessario)

**Step 2: Visualizzazione**
1. Trascina il bin su **Columns**
2. Trascina COUNT su **Rows**
3. Mark Type → **Bar**

**Step 3: Formattazione**
- Color: singolo colore (grigio/blu)
- Aggiungi label su barre

---
"""

    def _guide_boxplot(self, index: int, x_field: str, y_field: str, desc: str) -> str:
        return f"""
### Grafico {index}: Box Plot (Quartili e Outlier)

**Tipo**: Box Plot  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Identificare outlier e distribuzione"}

**Come Creare su Tableau**:

**Step 1: Setup**
1. Trascina categoria su **Rows**
2. Trascina valore numerico su **Columns**
3. Mark Type → **Box Plot** (o Bar con opzione Analytics)

**Step 2: Analisi**
- Tableau mostra automaticamente: min, Q1, mediana, Q3, max
- I pallini sono gli outlier

**Step 3: Personalizzazione**
- Color → distingui outlier
- Aggiungi Tooltip per dettagli

---
"""

    def _guide_treemap(self, index: int, x_field: str, y_field: str, desc: str) -> str:
        return f"""
### Grafico {index}: Treemap (Gerarchia)

**Tipo**: Treemap  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Mostrare gerarchia e proporzioni"}

**Come Creare su Tableau**:

**Step 1: Setup**
1. Trascina categoria principale su **Rows**
2. Trascina sub-categoria su **Color**
3. Trascina valore su **Size**
4. Mark Type → **Square**

**Step 2: Formato**
- Color palette: Sequential o Categorical
- Aggiungi label con valore

**Step 3: Drill-down**
- Right-click → Add Filter
- Permette agli utenti di filtrare

---
"""

    def _guide_radar(self, index: int, x_field: str, y_field: str, desc: str) -> str:
        return f"""
### Grafico {index}: Radar Chart (Profili)

**Tipo**: Radar Chart  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Confrontare profili multidimensionali"}

**Come Creare su Tableau**:

**Step 1: Setup Base**
1. Create Calculated Field: `Order Index`
   Formula: `INDEX()`
2. Trascina su **Columns** e **Rows** (crea griglia)

**Step 2: Dati Radar**
1. Trascina categorie su **Rows**
2. Trascina valore su **Columns**
3. Formatta come Dual Axis

**Step 3: Trasforma in Radar**
1. Mark Type → Line
2. Coordinate → Polar (cambio in Analysis pane)

---
"""

    def _guide_violin(self, index: int, x_field: str, y_field: str, desc: str) -> str:
        return f"""
### Grafico {index}: Violin Plot (Densità Distribuzione)

**Tipo**: Violin Plot  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Mostrare densità e forma della distribuzione"}

**Come Creare su Tableau**:

**Step 1: Setup**
1. Trascina categoria su **Rows**
2. Trascina variabile continua su **Columns**
3. Mark Type → Area

**Step 2: Personalizzazione**
- Color → distintivo per categoria
- Aggiungi density plot con Analytics

---
"""

    def _guide_area_chart(
        self, index: int, x_field: str, y_field: str, desc: str
    ) -> str:
        return f"""
### Grafico {index}: Area Chart (Trend Cumulato)

**Tipo**: Area Chart  
**Dati**: {x_field} vs {y_field}  
**Uso**: {desc or "Mostrare trend con riempimento cumulato"}

**Come Creare su Tableau**:

**Step 1: Setup**
1. Trascina tempo su **Columns**
2. Trascina valore su **Rows**
3. Trascina categoria su **Color**
4. Mark Type → **Area**

**Step 2: Stacking**
- Assicurati che sia impostato "Stacked"
- Menu Mark → Area → Full

**Step 3: Personalizzazione**
- Transparency: 0.7 per visibilità sottostanti
- Color palette: armonica

---
"""

    def _guide_generic_chart(
        self, index: int, x_field: str, y_field: str, desc: str
    ) -> str:
        return f"""
### Grafico {index}: Personalizzato

**Dati**: {x_field} vs {y_field}  
**Descrizione**: {desc or "Grafico personalizzato"}

**Procedura Generale**:
1. Trascina campo su **Columns** o **Rows**
2. Scegli **Mark Type** appropriato
3. Personalizza colori e etichette
4. Aggiungi filtri se necessario

---
"""

    def _generate_all_chart_types_guide(self) -> str:
        """Genera guida per tutti i tipi di grafico"""
        return """
### Grafico 1: Linea (Trend)

**Come Creare**:
1. Columns: Data/Tempo
2. Rows: Valore numerico
3. Mark Type: Line
4. Color: Univoco o per categoria

---

### Grafico 2: Barre (Confronto)

**Come Creare**:
1. Rows: Categoria
2. Columns: Valore
3. Mark Type: Bar
4. Sort discendente

---

### Grafico 3: Scatter (Correlazione)

**Come Creare**:
1. Columns: Var 1
2. Rows: Var 2
3. Mark Type: Circle
4. Size: Var 3 (opzionale)

---

### Grafico 4: Pie (Composizione)

**Come Creare**:
1. Rows: Categoria
2. Columns: Valore
3. Mark Type: Pie
4. Label: Percentuali

---

### Grafico 5: Heatmap (Matrice)

**Come Creare**:
1. Columns: Cat 1
2. Rows: Cat 2
3. Color: Valore
4. Mark Type: Square

---
"""

    def _generate_tips_section(self) -> str:
        """Genera sezione con tips & tricks"""
        return """
---

## 💡 Tips & Tricks Tableau

### Colori

**Palette Consigliate**:
- **Sequenziale** (per trend): Blu → Bianco → Rosso
- **Categorica** (per categorie): Hue 10
- **Divergente** (contrasto): Rosso-Blu

**Come Applicare**:
1. Color → Edit Colors
2. Scegli palette
3. Adjust → Hue saturation/Lightness

### Filtri Interattivi

1. Trascina campo su **Filters**
2. Clicca su filtro → **Show Filter**
3. Scegli tipo:
   - **Wildcard** (testo)
   - **Range** (numeri)
   - **List** (categorie)

### Dashboard Interattivo

1. Crea **Dashboard**
2. Trascina 2+ grafici
3. Right-click → **Use as Filter**
4. Seleziona cosa filtrare

### Performance

**Per dataset grandi (>1M righe)**:
- Aggiungi filtri temporali
- Usa **Extract** (salva localmente)
- Limita grafici per dashboard

### Esportare

1. File → Export Image (PNG)
2. File → Export Data (CSV)
3. File → Print (PDF)

---

## 📞 Supporto e Risorse

**Documentazione Ufficiale**: https://help.tableau.com/current/pro/desktop/en-us/
**Community**: https://community.tableau.com/
**Formazione**: Tableau Learning Portal

---

**Documento Generato Automaticamente**  
*Conserva questo file per referenza durante la creazione su Tableau*
"""

    def export_to_file(
        self, charts: List[Dict] = None, kpis: List[Dict] = None, filepath: str = None
    ) -> str:
        """
        Esporta documentazione in file Markdown

        Args:
            charts: Lista di grafici
            kpis: Lista di KPI
            filepath: Path dove salvare (default: tableau_guide.md)

        Returns:
            str: Path al file creato
        """
        if filepath is None:
            filepath = (
                f"tableau_guide_{self.timestamp.replace('/', '_').replace(':', '')}.md"
            )

        guide = self.generate_tableau_guide(charts, kpis)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(guide)

        return filepath


# ============================================================================
# FUNZIONE HELPER
# ============================================================================


def generate_tableau_documentation(
    df: pd.DataFrame,
    charts: List[Dict] = None,
    kpis: List[Dict] = None,
    title: str = "Dashboard",
) -> str:
    """
    Helper function per generare documentazione Tableau

    Args:
        df: DataFrame con dati
        charts: Lista di grafici
        kpis: Lista di KPI
        title: Titolo dashboard

    Returns:
        str: Documentazione Markdown
    """
    generator = TableauDocumentationGenerator(df, title)
    return generator.generate_tableau_guide(charts, kpis)
