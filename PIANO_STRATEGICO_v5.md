# 📊 PIANO STRATEGICO - Dashboard Interattiva Professionale v5.0

**Data**: 12 Maggio 2026  
**Progetto**: AI Dashboard Generator - Integrazione Tableau + Export + Interattività Google  
**Versione**: 5.0  
**Status**: Piano Completo per Implementazione  

---

## 📋 INDICE GENERALE
1. [Descrizione Caratteristiche Dashboard](#1-descrizione-caratteristiche-dashboard)
2. [Calcolo Automatico KPI](#2-calcolo-automatico-kpi)
3. [Strutture Dashboard Dinamiche](#3-strutture-dashboard-dinamiche)
4. [Design Grafici Professionali](#4-design-grafici-professionali)
5. [Filtri Interattivi](#5-filtri-interattivi)
6. [Esportazione Tableau e PDF](#6-esportazione-tableau-e-pdf)
7. [Apertura Automatica su Google](#7-apertura-automatica-su-google)
8. [Rilevamento e Correzione Errori](#8-rilevamento-e-correzione-errori)
9. [Architettura Tecnica](#9-architettura-tecnica)
10. [Roadmap Implementazione](#10-roadmap-implementazione)

---

## 1. DESCRIZIONE CARATTERISTICHE DASHBOARD

### 🎯 Funzionalità Principali

#### 1.1 Caricamento Intelligente Dati
```
✅ Formati Supportati:
   • CSV, Excel (xlsx, xls), JSON
   • Caricamento drag-and-drop
   • Preview automatico dei dati
   • Validazione e pulizia automatica

✅ Riconoscimento Automatico:
   • Tipi di dati (numerico, categorie, date)
   • Colonne monetarie (€, $, £)
   • Percentuali e tassi
   • Coordinate geografiche
   • Timestamp e serie temporali
   • Booleani nascosti
```

#### 1.2 Analisi Intelligente con ML
```
✅ Algoritmi Implementati:
   • Random Forest: Identificazione variabili chiave
   • KMeans Clustering: Segmentazione automatica
   • Isolation Forest: Rilevamento anomalie
   • Analisi di correlazione: Relazioni tra variabili
   • Trend detection: Identificazione pattern temporali

✅ Output:
   • Top 5 variabili più influenti
   • Cluster segmentazione clienti/prodotti
   • Outliers anomali per investigazione
   • Correlazioni significative
   • Trend crescenti/decrescenti
```

#### 1.3 Dashboard Responsiva Dinamica
```
✅ Caratteristiche:
   • Layout che si adatta a mobile, tablet, desktop, ultrawide
   • Numero di colonne variabile (1-4) basato su viewport
   • Card e widget scalabili
   • Ordine degli elementi aleatorio ma bilanciato
   • Tema scuro/chiaro selezionabile
   • Font leggibili con contrasto ottimale

✅ Sezioni Principali:
   ┌────────────────────────────┐
   │ Header Informativo         │ (Titolo, fonte dati, data)
   ├────────────────────────────┤
   │ Filtri Globali             │ (1-2 filtri principali)
   ├────────────────────────────┤
   │ KPI Summary Grid           │ (4-8 KPI dinamici)
   ├────────────────────────────┤
   │ Grafici Intelligenti       │ (3-6 charts variabili)
   ├────────────────────────────┤
   │ Tabella Interattiva        │ (Con sort, filter, export)
   ├────────────────────────────┤
   │ Insights Testuali          │ (Hallmark punti chiave)
   └────────────────────────────┘
```

#### 1.4 Accessibilità Professionale
```
✅ WCAG 2.1 Level AA Compliance:
   • Contrasti colore ottimali
   • Dimensioni testo leggibili (min 14px)
   • Supporto screen reader
   • Navigazione da tastiera
   • Alt text per grafici
   • Skip links per sezioni
   • Descrizioni alternate per immagini

✅ Inclusività:
   • Palette colori daltonismo-friendly
   • Nessun colore solo come informazione
   • Testo esplicito oltre ai simboli
   • Font sans-serif per leggibilità
   • Spaziatura white space adeguata
```

---

## 2. CALCOLO AUTOMATICO KPI

### 📊 Architettura Sistema KPI

#### 2.1 Rilevamento Automatico Metriche

```python
# ALGORITMO DI RILEVAMENTO KPI
1. Scannerizzazione Colonne
   ├─ Identifica colonne numeriche (sum, avg, min, max)
   ├─ Identifica date (durata, range, frequenza)
   ├─ Identifica categorie (unique count, top category)
   ├─ Identifica percentuali (media, range)
   └─ Identifica booleani (true %, false %)

2. Classificazione Intelligente
   ├─ Colonna Monetaria?  → KPI Finanziario
   ├─ Colonna Percentuale? → KPI Efficienza
   ├─ Colonna Temporale?   → KPI Durata/Frequenza
   ├─ Colonna Volume?      → KPI Quantità
   └─ Colonna Qualità?     → KPI Completezza

3. Calcolo Trend
   ├─ Se dati temporali: trend %
   ├─ Se dati non temporali: differenza da media
   └─ Determinare ↑ (positivo), → (neutrale), ↓ (negativo)

4. Selezione Top KPI
   ├─ Varietà: max 8 KPI
   ├─ Priorità: variabili più significative
   └─ Bilanciamento: mix di metriche
```

#### 2.2 Tipi di KPI Dinamici

| Tipo KPI | Esempio | Formula | Visualizzazione |
|----------|---------|---------|-----------------|
| **Finanziario** | Ricavi Totali | SUM(ricavi) | €1.2M ↑ 12% |
| **Volume** | Transazioni | COUNT(*) | 5,432 → 0% |
| **Efficienza** | Conversion Rate | COUNT(conversioni)/COUNT(totali) | 23.4% ↑ 2.1% |
| **Durata** | Avg Ciclo Vendita | AVG(date_fine - date_inizio) | 14.2 giorni ↓ 1 g |
| **Qualità** | Completezza Dati | COUNT(non_null)/COUNT(totali) | 98% ↑ 2% |
| **Tendenza** | Crescita YoY | (Questo_anno - Anno_precedente)/Anno_precedente | +18% ↑ |
| **Categorico** | Top Categoria | ARGMAX(COUNT(*) by categoria) | Categoria A |
| **Composizione** | % by Categoria | COUNT(*) by categoria | Pie Chart |

#### 2.3 Implementazione Codice

```python
# src/kpi_calculator.py (NUOVO)

class KPICalculator:
    """Calcolo automatico di KPI intelligenti basato sui dati"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns
        self.categorical_cols = df.select_dtypes(include=['object']).columns
        self.date_cols = self._detect_temporal_columns()
        
    def calculate_all_kpis(self) -> List[KPI]:
        """Calcola automaticamente i KPI più significativi"""
        kpis = []
        
        # Step 1: Calcola tutti i KPI possibili
        for col in self.numeric_cols:
            kpis.extend(self._create_numeric_kpis(col))
        
        for col in self.categorical_cols:
            kpis.extend(self._create_categorical_kpis(col))
        
        for col in self.date_cols:
            kpis.extend(self._create_temporal_kpis(col))
        
        # Step 2: Ranking per significatività
        ranked_kpis = self._rank_by_significance(kpis)
        
        # Step 3: Selezione bilanciata (max 8)
        selected = self._select_balanced(ranked_kpis, max_count=8)
        
        # Step 4: Calcolo trend se possibile
        for kpi in selected:
            if self._has_temporal_dimension():
                kpi.trend = self._calculate_trend(kpi)
        
        return selected
    
    def _create_numeric_kpis(self, col_name: str) -> List[KPI]:
        """Crea KPI da colonne numeriche"""
        kpis = []
        col_data = self.df[col_name].dropna()
        
        # KPI Somma (se colonna monetaria)
        if self._is_monetary(col_name):
            kpis.append(KPI(
                name=f"Totale {col_name}",
                value=col_data.sum(),
                format="currency",
                icon="💰",
                description=f"Somma totale di {col_name}"
            ))
        
        # KPI Media
        kpis.append(KPI(
            name=f"Media {col_name}",
            value=col_data.mean(),
            format="number",
            icon="📊",
            description=f"Valore medio di {col_name}"
        ))
        
        # KPI Max/Min (se significativo)
        if col_data.max() - col_data.min() > col_data.std() * 3:
            kpis.append(KPI(
                name=f"Max {col_name}",
                value=col_data.max(),
                format="number",
                icon="📈",
                description=f"Valore massimo di {col_name}"
            ))
        
        return kpis
    
    def _calculate_trend(self, kpi: KPI) -> Dict:
        """Calcola trend % rispetto al periodo precedente"""
        # Se dati temporali disponibili
        if not self._has_temporal_dimension():
            return {"value": 0, "direction": "neutral"}
        
        # Divide dati in due periodi
        current_period = self._get_current_period_data()
        previous_period = self._get_previous_period_data()
        
        current_val = kpi.calculate(current_period)
        previous_val = kpi.calculate(previous_period)
        
        change_pct = ((current_val - previous_val) / previous_val) * 100 if previous_val != 0 else 0
        
        direction = "up" if change_pct > 0 else "down" if change_pct < 0 else "neutral"
        
        return {
            "value": abs(change_pct),
            "direction": direction,
            "text": f"{change_pct:+.1f}%"
        }

# Integrare nel file app.py:
from kpi_calculator import KPICalculator

if uploaded_file:
    df = pd.read_file(uploaded_file)
    kpi_calculator = KPICalculator(df)
    kpis = kpi_calculator.calculate_all_kpis()
    render_kpi_grid(kpis)
```

#### 2.4 Configurazione KPI per Dataset

```python
# Salvataggio configurazione KPI per dataset
SAVED_KPI_CONFIGS = {
    "sales_data.csv": {
        "kpis": ["Total Revenue", "Avg Order Value", "Conversion Rate", ...],
        "refresh_frequency": "daily",
        "alerts": {
            "Total Revenue": {"below": 50000, "action": "email"}
        }
    }
}
```

---

## 3. STRUTTURE DASHBOARD DINAMICHE

### 🎲 Sistema Layout Randomizzato

#### 3.1 Logica Variabilità

```
Obiettivo: Stesso dataset → Layout SEMPRE DIVERSO
          Mantenendo: Coerenza visiva, usabilità, accessibilità

┌─ SEZIONE KPI (Sempre presente, ordine variabile)
│  ├─ Numero KPI: 4-8 (casuale)
│  ├─ Ordine: Shuffle casuale
│  ├─ Colonne: 2, 3 o 4 (basato viewport + random)
│  └─ Colori: Gradient variabile ma accessibile
│
├─ SEZIONE CHARTS (3-6 grafici, ordine variabile)
│  ├─ Numero charts: Scelto in base ai dati
│  ├─ Ordine: Randomizzato
│  ├─ Posizioni colonne: 1, 2 o full-width
│  ├─ Tipo chart: Intelligente (vedi capitolo 4)
│  └─ Orientamento: Orizzontale vs Verticale
│
└─ SEZIONE TABLE (Sempre alla fine)
   ├─ Posizione: Bottom (coerente)
   ├─ Colonne visibili: Selezionate intelligentemente
   └─ Filtri: 1-3 filtri disponibili
```

#### 3.2 Implementazione LayoutRandomizer

```python
# src/layout_randomizer.py - Espandere

class AdvancedLayoutRandomizer:
    """Crea layout sempre diversi mantenendo UX coerente"""
    
    def __init__(self, num_kpis: int, num_charts: int, viewport_width: int):
        self.num_kpis = num_kpis
        self.num_charts = num_charts
        self.viewport_width = viewport_width
        self.seed = None  # Permette riproducibilità se necessario
    
    def generate_layout(self) -> Dict:
        """Genera configurazione layout casuale ma bilanciata"""
        
        layout = {
            "kpi_section": self._generate_kpi_layout(),
            "chart_section": self._generate_chart_layout(),
            "table_section": self._generate_table_layout(),
            "color_theme": self._select_color_theme(),
            "spacing": self._calculate_spacing()
        }
        
        return layout
    
    def _generate_kpi_layout(self) -> Dict:
        """Layout casuale per KPI grid"""
        # Numero colonne: basato viewport + randomness
        if self.viewport_width < 768:
            num_cols = random.choice([1, 2])
        elif self.viewport_width < 1200:
            num_cols = random.choice([2, 3])
        else:
            num_cols = random.choice([3, 4])
        
        # Ordine KPI casuale
        kpi_order = list(range(self.num_kpis))
        random.shuffle(kpi_order)
        
        return {
            "columns": num_cols,
            "order": kpi_order,
            "gap": random.choice([16, 20, 24]),  # Spacing variabile
            "animation": random.choice(["fade", "slide", "scale"])
        }
    
    def _generate_chart_layout(self) -> List[Dict]:
        """Layout casuale per charts"""
        charts = []
        remaining_charts = self.num_charts
        
        while remaining_charts > 0:
            # Scegli numero colonne per questo "row"
            cols = min(remaining_charts, random.choice([1, 2, 2, 2, 3]))
            
            charts.append({
                "width": cols,
                "charts": cols,
                "gap": random.choice([16, 20]),
                "height": random.choice([400, 450, 500])
            })
            
            remaining_charts -= cols
        
        # Shuffle rows ma mantieni almeno un chart completo per row
        return charts
    
    def _select_color_theme(self) -> Dict:
        """Seleziona tema colori casuale"""
        themes = [
            {
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f59e0b"
            },
            {
                "primary": "#3b82f6",
                "secondary": "#1e40af",
                "accent": "#10b981"
            },
            {
                "primary": "#6366f1",
                "secondary": "#4f46e5",
                "accent": "#ec4899"
            }
        ]
        return random.choice(themes)

# Utilizzo in app.py
randomizer = AdvancedLayoutRandomizer(
    num_kpis=len(kpis),
    num_charts=len(selected_charts),
    viewport_width=st.session_state.get('viewport_width', 1024)
)
layout_config = randomizer.generate_layout()
```

#### 3.3 Variabilità Bilanciata

```python
# Strategie per mantenere coerenza despite randomness

class LayoutBalancer:
    """Assicura che layout casuale rimane usabile"""
    
    @staticmethod
    def validate_layout(layout: Dict) -> bool:
        """Verifica che layout non è squilibrato"""
        checks = {
            "min_kpis_visible": layout["kpis"] >= 4,
            "charts_balanced": all(len(row) <= 3 for row in layout["charts"]),
            "reading_flow": layout["kpi_section"]["before_charts"] == True,
            "max_height": layout["total_height"] < 4000  # Max 4000px per non scrollare troppo
        }
        return all(checks.values())
    
    @staticmethod
    def adjust_spacing(cols: int) -> int:
        """Spacing adattativo basato su numero colonne"""
        spacing_map = {1: 24, 2: 20, 3: 16, 4: 12}
        return spacing_map.get(cols, 16)
```

#### 3.4 Seeding per Riproducibilità

```python
# Opzionale: permettere agli utenti di "salvare" un layout
class LayoutMemory:
    """Salva e ricarica layout preferiti"""
    
    def save_layout(self, layout_id: str, layout: Dict):
        """Salva layout con seed"""
        with open(f"layouts/{layout_id}.json", "w") as f:
            json.dump(layout, f)
    
    def load_layout(self, layout_id: str) -> Dict:
        """Carica layout salvato"""
        with open(f"layouts/{layout_id}.json", "r") as f:
            return json.load(f)
```

---

## 4. DESIGN GRAFICI PROFESSIONALI

### 🎨 Sistema Intelligente di Selezione Grafici

#### 4.1 Algoritmo Selezione Chart Type

```
LOGICA DI SELEZIONE:

1. ANALIZZA DATI
   ├─ Numero variabili: 1, 2, 3+
   ├─ Tipo dati: Numerico, Categorico, Temporale, Geografico
   ├─ Cardinality: Valori unici
   └─ Relationships: Correlazioni

2. GENERA CANDIDATI
   ├─ Per ogni combinazione di variabili
   └─ Suggerisci 3-5 chart types possibili

3. SCORE CANDIDATI
   ├─ Effettività visuale (quanto bene comunica il dato)
   ├─ Leggibilità (è chiaro il messaggio?)
   ├─ Novità (diverso dagli altri charts?)
   └─ Accessibilità (leggibile per colorblind?)

4. SELEZIONA TOP 5-6 CHARTS
   ├─ Best 1: Quello con score più alto
   ├─ Diversità: Non ripetere lo stesso type
   └─ Mix: Bilanciare temporali, comparativi, etc.
```

#### 4.2 Mapping Dati → Chart Type

| N. Variabili | Tipo Dato | Best Chart | Alternativa 1 | Alternativa 2 | Quando NO |
|--------------|-----------|-----------|---------------|---------------|-----------|
| 1 Num | Trend | Line Chart | Area Chart | Column Chart | Pie (no %!) |
| 1 Num | Distribuzione | Histogram | Box Plot | Violin Plot | Scatter |
| 1 Cat | Composizione | Donut | Pie | Bar | Line |
| 2 Num | Correlazione | Scatter | Bubble | Heatmap | Line |
| 1 Num + 1 Cat | Confronto | Bar | Column | Violin | Pie |
| 1 Num + 2 Cat | Faceted | Small Multiples | Grouped Bar | Heatmap | Single Bar |
| Num + Date | Trend | Line + Area | Combo | Step | Scatter |
| 2+ Cat | Network | Sankey | Chord | Sunburst | Pie |
| Geo + Num | Map | Choropleth | Bubble Map | Scatter Map | Heatmap |

#### 4.3 Implementazione Intelligente Charts

```python
# src/charts_intelligent.py - Espandere

class IntelligentChartBuilder:
    """Seleziona automaticamente il miglior chart per i dati"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.analyzer = DataAnalyzer(df)
    
    def generate_chart_suggestions(self, num_suggestions: int = 5) -> List[ChartSuggestion]:
        """Suggerisce i migliori chart per questo dataset"""
        
        # Step 1: Analizza dati disponibili
        data_profile = self.analyzer.profile()
        
        # Step 2: Genera candidati
        candidates = self._generate_candidates(data_profile)
        
        # Step 3: Score candidati
        scored = self._score_candidates(candidates)
        
        # Step 4: Seleziona diversi
        selected = self._select_diverse(scored, num_suggestions)
        
        return selected
    
    def _score_candidates(self, candidates: List[ChartCandidate]) -> List[Tuple]:
        """Score cada candidato chart"""
        scored = []
        
        for candidate in candidates:
            score = {
                "effectiveness": self._rate_effectiveness(candidate),
                "readability": self._rate_readability(candidate),
                "novelty": self._rate_novelty(candidate),
                "accessibility": self._rate_accessibility(candidate),
                "data_fit": self._rate_data_fit(candidate)
            }
            
            # Weighted score
            total = (
                score["effectiveness"] * 0.30 +
                score["readability"] * 0.25 +
                score["novelty"] * 0.15 +
                score["accessibility"] * 0.20 +
                score["data_fit"] * 0.10
            )
            
            scored.append((candidate, total, score))
        
        # Sort by total score
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def _rate_effectiveness(self, candidate: ChartCandidate) -> float:
        """Quanto efficacemente comunica il dato"""
        
        rules = {
            ("1_numeric", "trend"): ("line", 1.0),
            ("1_numeric", "distribution"): ("histogram", 0.95),
            ("1_categorical", "composition"): ("donut", 0.95),
            ("2_numeric", "correlation"): ("scatter", 1.0),
            # ... altre regole
        }
        
        key = (candidate.data_profile, candidate.intent)
        if key in rules:
            best_chart, score = rules[key]
            if candidate.chart_type == best_chart:
                return score
        
        return 0.5  # Score base per others
    
    def _rate_accessibility(self, candidate: ChartCandidate) -> float:
        """Leggibilità per persone daltoniche"""
        
        chart_accessibility = {
            "line": 1.0,
            "bar": 0.95,
            "scatter": 0.9,
            "pie": 0.5,  # Difficile per daltonismi
            "heatmap": 0.6  # Richiede patterns oltre colori
        }
        
        base_score = chart_accessibility.get(candidate.chart_type, 0.7)
        
        # Ajusta se usa patterns oltre ai colori
        if candidate.uses_patterns:
            base_score = min(1.0, base_score + 0.2)
        
        return base_score

# Render chart dinamico
def render_intelligent_chart(suggestion: ChartSuggestion, df: pd.DataFrame):
    """Renderizza chart con dati corretti"""
    
    fig = None
    
    if suggestion.chart_type == "line":
        fig = go.Figure(data=[
            go.Scatter(x=df[suggestion.x_col], y=df[suggestion.y_col], mode='lines')
        ])
    
    elif suggestion.chart_type == "bar":
        fig = go.Figure(data=[
            go.Bar(x=df[suggestion.x_col], y=df[suggestion.y_col])
        ])
    
    # ... altri types
    
    # Applica styling professionale
    fig.update_layout(
        template="plotly_white",
        font=dict(family="IBM Plex Sans", size=12),
        hovermode="x unified",
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

#### 4.4 Styling Professionale

```python
# Palette colori consistency
PROFESSIONAL_COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#3b82f6"
}

# Gradient colori per serie
GRADIENT_PALETTES = {
    "blue_purple": ["#667eea", "#764ba2"],
    "green_emerald": ["#10b981", "#059669"],
    "warm": ["#f59e0b", "#d97706", "#b45309"]
}

# Hover templates
HOVER_TEMPLATE = """
<b>%{customdata[0]}</b><br>
Valore: %{y:,.2f}<br>
<extra></extra>
"""
```

---

## 5. FILTRI INTERATTIVI

### 🎯 Sistema Filtri Avanzati

#### 5.1 Tipi di Filtri

```
FILTRI PRINCIPALI:
│
├─ Filtro 1: Select (Singolo o Multiplo)
│  └─ Es: "Categoria: [Vendite, Marketing, HR]"
│
├─ Filtro 2: Range Slider (Intervallo)
│  └─ Es: "Ricavi: [€10k - €100k]"
│
├─ Filtro 3: Date Range (Opzionale se dati temporali)
│  └─ Es: "Periodo: [01/01/2024 - 31/12/2024]"
│
└─ Filtro 4: Search/Text (Per grandi liste)
   └─ Es: "Cerca cliente: [Apple, Amazon, ...]"

CARATTERISTICHE:
✅ Salvataggio stato filtri in sessione
✅ URL parameters per condividibilità
✅ Reset button per azzerare
✅ Contatori elementi attivi
✅ Applicazione live (no "Apply" button)
```

#### 5.2 Implementazione Filtri

```python
# src/filter_system.py - Espandere

class AdvancedFilterManager:
    """Gestisce filtri globali intelligenti"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.active_filters = {}
    
    def render_filter_bar(self):
        """Renderizza barra filtri intelligente"""
        
        # Rileva colonne filtrabili
        filterable_cols = self._detect_filterable_columns()
        
        # Limita a max 3 filtri
        selected_cols = self._select_top_filters(filterable_cols, max_count=3)
        
        with st.container():
            cols = st.columns(len(selected_cols) + 1)  # +1 per reset
            
            for idx, col_name in enumerate(selected_cols):
                with cols[idx]:
                    filter_value = self._render_single_filter(col_name)
                    if filter_value is not None:
                        self.active_filters[col_name] = filter_value
            
            # Reset button
            with cols[-1]:
                if st.button("🔄 Reset Filtri"):
                    self.active_filters = {}
                    st.rerun()
    
    def _render_single_filter(self, col_name: str):
        """Renderizza singolo filtro appropriato"""
        
        col_data = self.df[col_name]
        col_dtype = col_data.dtype
        unique_count = col_data.nunique()
        
        # Scegli tipo filtro basato su dati
        if col_dtype in ['object', 'category']:
            if unique_count <= 10:
                # Multiselect
                return st.multiselect(
                    label=col_name,
                    options=col_data.unique(),
                    default=col_data.unique()[:1].tolist()
                )
            else:
                # Search select
                return st.selectbox(
                    label=col_name,
                    options=col_data.unique()
                )
        
        elif col_dtype in ['int64', 'float64']:
            # Slider range
            min_val, max_val = col_data.min(), col_data.max()
            return st.slider(
                label=col_name,
                min_value=float(min_val),
                max_value=float(max_val),
                value=(float(min_val), float(max_val))
            )
        
        elif pd.api.types.is_datetime64_any_dtype(col_dtype):
            # Date range
            dates = pd.to_datetime(col_data)
            return st.date_input(
                label=col_name,
                value=(dates.min(), dates.max()),
                min_value=dates.min(),
                max_value=dates.max()
            )
        
        return None
    
    def apply_filters(self) -> pd.DataFrame:
        """Applica tutti i filtri attivi"""
        
        filtered_df = self.df.copy()
        
        for col_name, filter_value in self.active_filters.items():
            if isinstance(filter_value, list):
                # Multiselect filter
                filtered_df = filtered_df[filtered_df[col_name].isin(filter_value)]
            
            elif isinstance(filter_value, tuple) and len(filter_value) == 2:
                # Range filter (numeric o date)
                filtered_df = filtered_df[
                    (filtered_df[col_name] >= filter_value[0]) &
                    (filtered_df[col_name] <= filter_value[1])
                ]
            
            elif isinstance(filter_value, str):
                # Search filter
                filtered_df = filtered_df[filtered_df[col_name].str.contains(filter_value, case=False)]
        
        return filtered_df
    
    def _detect_filterable_columns(self) -> List[str]:
        """Identifica colonne adatte come filtri"""
        
        filterable = []
        
        for col in self.df.columns:
            col_data = self.df[col]
            
            # Categorie: max 20 valori unici
            if col_data.dtype == 'object' and col_data.nunique() <= 20:
                filterable.append(col)
            
            # Numeriche: se hanno pattern categorico
            elif col_data.dtype in ['int64', 'float64']:
                # Non includere colonne con 1000+ valori unici
                if col_data.nunique() <= 1000:
                    filterable.append(col)
            
            # Date: sempre filtrabili
            elif pd.api.types.is_datetime64_any_dtype(col_data):
                filterable.append(col)
        
        return filterable

# Uso in app.py
@st.cache_data
def get_filtered_data():
    filter_manager = AdvancedFilterManager(df)
    filter_manager.render_filter_bar()
    return filter_manager.apply_filters()

filtered_df = get_filtered_data()
```

#### 5.3 Esperienza Utente Filtri

```python
# Indicatori visivi
with st.container(border=True):
    
    # Mostra numero record
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🔍 Filtri Attivi")
    with col2:
        st.metric("Record", len(filtered_df), f"{len(df) - len(filtered_df)} esclusi")
    
    # Filtri bar
    filter_manager.render_filter_bar()
    
    # Stato filtri
    if filter_manager.active_filters:
        st.info(f"✅ Filtri applicati: {len(filter_manager.active_filters)}")
```

---

## 6. ESPORTAZIONE TABLEAU E PDF

### 📦 Sistema Export Professionale

#### 6.1 Esportazione Tableau (.twbx)

```python
# src/tableau_exporter.py (NUOVO)

class TableauExporter:
    """Esporta dashboard in formato Tableau compatibile"""
    
    def __init__(self, df: pd.DataFrame, kpis: List[KPI], charts: List[Chart]):
        self.df = df
        self.kpis = kpis
        self.charts = charts
        self.temp_dir = tempfile.mkdtemp()
    
    def export_to_tableau(self, filename: str = "dashboard.twbx") -> str:
        """
        Crea file Tableau (.twbx) completamente funzionale
        
        Struttura file:
        dashboard.twbx
        ├── datafiles/
        │   └── data_source.csv (i dati)
        ├── dashboard.twb (XML del dashboard)
        └── worksheets/ (singoli worksheets)
            ├── kpi_summary.twb
            ├── chart_1.twb
            └── chart_2.twb
        """
        
        # Step 1: Salva dati
        data_path = self._export_data()
        
        # Step 2: Crea dashboard TWB
        dashboard_xml = self._generate_dashboard_twb()
        
        # Step 3: Crea worksheets
        worksheet_xmls = self._generate_worksheets()
        
        # Step 4: Crea package TWBX
        twbx_path = self._package_twbx(dashboard_xml, worksheet_xmls, data_path, filename)
        
        return twbx_path
    
    def _export_data(self) -> str:
        """Salva dati come CSV per Tableau"""
        csv_path = os.path.join(self.temp_dir, "data.csv")
        self.df.to_csv(csv_path, index=False, encoding='utf-8')
        return csv_path
    
    def _generate_dashboard_twb(self) -> str:
        """Crea dashboard XML Tableau"""
        
        twb_template = """<?xml version='1.0' encoding='utf-8'?>
<workbook source-build='10.0.0' xmlns='http://tableauserver.com/api' xmlns:user='http://tableauserver.com/api/user'>
  <preferences/>
  <datasources>
    <datasource caption="Data Source" name="datasource0" inline="true" version="10.0">
      <connection class="sqlserver" dbname="data.csv" server="."/>
    </datasource>
  </datasources>
  <worksheets>
{worksheets}
  </worksheets>
  <dashboard name="Main Dashboard">
{dashboard_zones}
  </dashboard>
</workbook>
"""
        
        # Genera placeholder per worksheets
        worksheets_str = "\n    ".join([
            f'<worksheet name="sheet{i}"/>' for i in range(len(self.charts) + 1)
        ])
        
        # Genera layout dashboard
        dashboard_zones = self._generate_dashboard_zones()
        
        twb_xml = twb_template.format(
            worksheets=worksheets_str,
            dashboard_zones=dashboard_zones
        )
        
        return twb_xml
    
    def _generate_dashboard_zones(self) -> str:
        """Crea zone del dashboard in XML"""
        zones = []
        y_position = 0
        
        # Zone KPI
        zones.append(f"""    <zone name="kpi_zone" type="layout" h="{100}" w="{960}" x="0" y="{y_position}">
      <zone-objects>
        <zone-object name="kpi_sheet"/>
      </zone-objects>
    </zone>""")
        
        y_position += 150
        
        # Zone Charts
        col_width = 480
        x_position = 0
        
        for i, chart in enumerate(self.charts):
            if i % 2 == 0:
                x_position = 0
            else:
                x_position = col_width
            
            zones.append(f"""    <zone name="chart_{i}" type="layout" h="400" w="{col_width}" x="{x_position}" y="{y_position}">
      <zone-objects>
        <zone-object name="chart_{i}"/>
      </zone-objects>
    </zone>""")
            
            if (i + 1) % 2 == 0:
                y_position += 450
        
        return "\n".join(zones)
    
    def _generate_worksheets(self) -> Dict[str, str]:
        """Crea XML per ogni worksheet"""
        worksheets = {}
        
        # Worksheet KPI
        worksheets["kpi_sheet"] = self._generate_kpi_worksheet()
        
        # Worksheet per ogni chart
        for i, chart in enumerate(self.charts):
            worksheets[f"chart_{i}"] = self._generate_chart_worksheet(chart)
        
        return worksheets
    
    def _generate_kpi_worksheet(self) -> str:
        """Crea worksheet per KPI summary"""
        # Tableau XML per KPI
        kpi_marks = "\n".join([
            f'      <mark><text>{kpi.name}: {kpi.value}</text></mark>'
            for kpi in self.kpis[:4]  # Max 4 KPI per non affollare
        ])
        
        return f"""<?xml version='1.0' encoding='utf-8'?>
<worksheet name="kpi_summary">
  <layout type="horizontal" param="1">
{kpi_marks}
  </layout>
</worksheet>"""
    
    def _generate_chart_worksheet(self, chart: Chart) -> str:
        """Crea worksheet per singolo chart"""
        # Dipende dal tipo chart
        return f"""<?xml version='1.0' encoding='utf-8'?>
<worksheet name="{chart.name}">
  <table>
    <column caption="{chart.x_axis}" datatype="string" name="[{chart.x_axis}]"/>
    <column caption="{chart.y_axis}" datatype="real" name="[{chart.y_axis}]"/>
  </table>
  <layout type="vertical">
    <pane name="Rows">
      <mark class='Automatic'/>
    </pane>
  </layout>
</worksheet>"""
    
    def _package_twbx(self, dashboard_xml: str, worksheets: Dict, data_path: str, filename: str) -> str:
        """Crea package TWBX (ZIP)"""
        
        twbx_path = os.path.join(self.temp_dir, filename)
        
        with zipfile.ZipFile(twbx_path, 'w', zipfile.ZIP_DEFLATED) as twbx:
            # Aggiungi dashboard XML
            twbx.writestr("dashboard.twb", dashboard_xml)
            
            # Aggiungi worksheets
            for sheet_name, sheet_xml in worksheets.items():
                twbx.writestr(f"worksheets/{sheet_name}.twb", sheet_xml)
            
            # Aggiungi dati
            twbx.write(data_path, "datafiles/data.csv")
        
        return twbx_path

# Uso in app.py
if st.button("📊 Esporta a Tableau"):
    exporter = TableauExporter(df, kpis, charts)
    twbx_path = exporter.export_to_tableau()
    
    with open(twbx_path, "rb") as f:
        st.download_button(
            label="⬇️ Scarica Tableau Dashboard",
            data=f.read(),
            file_name=f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.twbx",
            mime="application/zip"
        )
```

#### 6.2 Esportazione PDF Professionale

```python
# src/pdf_generator.py - Migliorare

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib import colors

class ProfessionalPDFGenerator:
    """Genera PDF professional con dashboard mockup e guida Tableau"""
    
    def __init__(self, df: pd.DataFrame, kpis: List[KPI], charts: List[Chart]):
        self.df = df
        self.kpis = kpis
        self.charts = charts
    
    def generate_pdf(self, filename: str = "dashboard_guide.pdf") -> str:
        """
        Genera PDF con:
        1. Dashboard screenshot
        2. KPI Summary
        3. Guida step-by-step per Tableau
        4. Campi calcolati suggeriti
        5. Dati di riferimento
        """
        
        pdf_path = filename
        doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Contenuti PDF
        story = []
        styles = getSampleStyleSheet()
        
        # 1. Cover Page
        story.extend(self._create_cover_page(styles))
        story.append(PageBreak())
        
        # 2. Executive Summary
        story.extend(self._create_executive_summary(styles))
        story.append(PageBreak())
        
        # 3. KPI Cards
        story.extend(self._create_kpi_section(styles))
        story.append(PageBreak())
        
        # 4. Charts Overview
        story.extend(self._create_charts_section(styles))
        story.append(PageBreak())
        
        # 5. Tableau Step-by-Step Guide
        story.extend(self._create_tableau_guide(styles))
        
        # Build PDF
        doc.build(story)
        
        return pdf_path
    
    def _create_cover_page(self, styles) -> List:
        """Crea prima pagina"""
        elements = []
        
        title = Paragraph(
            "📊 Dashboard Analytics Report",
            styles['Title']
        )
        
        subtitle = Paragraph(
            f"Generated on {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles['Normal']
        )
        
        elements.extend([
            Spacer(1, 2*inch),
            title,
            Spacer(1, 0.2*inch),
            subtitle
        ])
        
        return elements
    
    def _create_executive_summary(self, styles) -> List:
        """Crea sommario esecutivo"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", styles['Heading1']))
        
        # Key metrics
        summary_text = f"""
        <b>Dataset Analysis:</b><br/>
        • Total Records: {len(self.df):,}<br/>
        • Total Columns: {len(self.df.columns)}<br/>
        • Date Range: {self._get_date_range()}<br/>
        <br/>
        <b>Key Findings:</b><br/>
        """
        
        for idx, kpi in enumerate(self.kpis[:5], 1):
            summary_text += f"• {kpi.name}: {kpi.value}<br/>"
        
        elements.append(Paragraph(summary_text, styles['Normal']))
        
        return elements
    
    def _create_kpi_section(self, styles) -> List:
        """Crea sezione KPI"""
        elements = []
        
        elements.append(Paragraph("Key Performance Indicators", styles['Heading1']))
        
        kpi_data = []
        for kpi in self.kpis:
            kpi_data.append([
                kpi.name,
                str(kpi.value),
                kpi.description or ""
            ])
        
        kpi_table = Table(kpi_data, colWidths=[2*inch, 1.5*inch, 3*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(kpi_table)
        
        return elements
    
    def _create_charts_section(self, styles) -> List:
        """Crea sezione charts"""
        elements = []
        
        elements.append(Paragraph("Visualizations Overview", styles['Heading1']))
        
        for idx, chart in enumerate(self.charts, 1):
            elements.append(
                Paragraph(f"{idx}. {chart.name}", styles['Heading2'])
            )
            
            # Chart image (da salvare prima)
            if hasattr(chart, 'image_path') and os.path.exists(chart.image_path):
                elements.append(Image(chart.image_path, width=6*inch, height=3*inch))
            
            elements.append(
                Paragraph(chart.description or "Chart visualization", styles['Normal'])
            )
            
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_tableau_guide(self, styles) -> List:
        """Crea guida Tableau step-by-step"""
        elements = []
        
        elements.append(Paragraph("Tableau Implementation Guide", styles['Heading1']))
        
        guide_steps = [
            ("1. Prepare Data", [
                "• Download the CSV file provided",
                "• Open Tableau Prep",
                "• Load CSV as input"
            ]),
            ("2. Create Data Source", [
                f"• Create connection to uploaded CSV",
                f"• Identify key dimensions: {', '.join(self.df.columns[:3])}",
                f"• Identify key measures: {', '.join([col for col in self.df.select_dtypes(include=['number']).columns[:3]])}"
            ]),
            ("3. Build Worksheets", [
                f"• Create {len(self.charts)} worksheets for each visualization",
                "• Configure axes and aggregations",
                "• Apply color schemes for consistency"
            ]),
            ("4. Calculate Fields", [
                "• Add calculated fields for metrics",
                "• Create parameters for interactivity",
                "• Set up filters"
            ]),
            ("5. Assemble Dashboard", [
                "• Combine worksheets into single dashboard",
                "• Configure interactions between visualizations",
                "• Add filters to dashboard"
            ])
        ]
        
        for step_title, substeps in guide_steps:
            elements.append(Paragraph(step_title, styles['Heading2']))
            substep_text = "<br/>".join(substeps)
            elements.append(Paragraph(substep_text, styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _get_date_range(self) -> str:
        """Estrae range date dai dati"""
        date_cols = self.df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            col = date_cols[0]
            return f"{self.df[col].min()} to {self.df[col].max()}"
        return "N/A"
```

#### 6.3 Zipping Export

```python
# Crea cartella zippata con tutti i file

class ExportPackager:
    """Pacchetto tutti i file di export"""
    
    def create_export_package(self, df: pd.DataFrame, kpis: List[KPI], 
                            charts: List[Chart]) -> str:
        """Crea ZIP con Tableau, PDF, CSV, e documentazione"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"dashboard_export_{timestamp}.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            
            # 1. Tableau file
            tableau_exporter = TableauExporter(df, kpis, charts)
            tableau_path = tableau_exporter.export_to_tableau()
            zf.write(tableau_path, "dashboard.twbx")
            
            # 2. PDF guide
            pdf_gen = ProfessionalPDFGenerator(df, kpis, charts)
            pdf_path = pdf_gen.generate_pdf()
            zf.write(pdf_path, "guide.pdf")
            
            # 3. Dati originali
            csv_path = tempfile.NamedTemporaryFile(suffix='.csv', delete=False).name
            df.to_csv(csv_path, index=False)
            zf.write(csv_path, "data.csv")
            
            # 4. Metadati
            metadata = {
                "exported_at": datetime.now().isoformat(),
                "num_records": len(df),
                "num_columns": len(df.columns),
                "num_kpis": len(kpis),
                "num_charts": len(charts)
            }
            zf.writestr("metadata.json", json.dumps(metadata, indent=2))
            
            # 5. README
            readme = self._create_readme()
            zf.writestr("README.md", readme)
        
        return zip_filename
    
    def _create_readme(self) -> str:
        return """
# Dashboard Export Package

## Contenuto

1. **dashboard.twbx** - File Tableau completo, pronto per aprire in Tableau Desktop o caricare su Tableau Online
2. **guide.pdf** - Guida completa per ricreate il dashboard in Tableau
3. **data.csv** - Dati sorgente in formato CSV
4. **metadata.json** - Informazioni su dataset e dashboard

## Come Usare

### Su Tableau Desktop
1. Apri Tableau Desktop
2. File > Open > dashboard.twbx
3. Il dashboard è pronto con dati e configurazioni

### Su Tableau Online (Free o a pagamento)
1. Accedi a https://online.tableau.com
2. Create > Workbook from file
3. Carica il file dashboard.twbx
4. Pubblica e condividi il link

## Supporto
Per problemi con il dashboard, consulta guide.pdf.
"""
```

---

## 7. APERTURA AUTOMATICA SU GOOGLE

### 🌐 Integrazione con Google Cloud

#### 7.1 Deployment su Google Cloud Run

```python
# Configurazione per deployer su Google Cloud Run

# requirements.txt (aggiungere)
google-cloud-storage>=2.0.0
google-auth>=2.0.0

# main.py per Cloud Run
from google.cloud import storage
from flask import Flask, render_template, request, send_file
import streamlit.cli as cli

app = Flask(__name__)

@app.route('/dashboard', methods=['GET'])
def serve_dashboard():
    """Serve dashboard Streamlit"""
    # Streamlit richiede di esser servito tramite subprocess
    cli.main(['run', 'app.py', '--logger.level=error'])
    return render_template('dashboard.html')

@app.route('/export/tableau', methods=['POST'])
def export_tableau():
    """Endpoint per esportare a Tableau"""
    # Logic per esportare
    ...

@app.route('/export/zip', methods=['GET'])
def download_export():
    """Scarica ZIP con tutti i file"""
    zip_path = "dashboard_export.zip"
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

#### 7.2 Apertura Automatica Browser

```python
# src/google_integration.py (NUOVO)

import webbrowser
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleDashboardManager:
    """Gestisce l'apertura automatica del dashboard su Google"""
    
    def __init__(self, service_account_key: str = None):
        """
        Args:
            service_account_key: Path al JSON con credenziali Google Cloud
        """
        self.service_account_key = service_account_key
        self.dashboard_url = None
    
    def open_dashboard_in_browser(self, dashboard_url: str = "http://localhost:8501"):
        """Apre il dashboard nel browser predefinito"""
        
        webbrowser.open_new_tab(dashboard_url)
        
        return {
            "status": "success",
            "message": f"Dashboard aperto in browser",
            "url": dashboard_url
        }
    
    def publish_to_google_sites(self, dashboard_html: str, site_name: str):
        """
        Pubblica il dashboard su una pagina Google Sites
        Richiede autenticazione OAuth2
        """
        
        try:
            # Autenticazione
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_key,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            
            # Crea documento Google
            drive_service = build('drive', 'v3', credentials=credentials)
            
            file_metadata = {
                'name': f'{site_name} Dashboard',
                'mimeType': 'text/html'
            }
            
            # Upload to Google Drive
            file = drive_service.files().create(
                body=file_metadata,
                media_body=dashboard_html,
                fields='id, webViewLink'
            ).execute()
            
            sharing_link = file.get('webViewLink')
            
            return {
                "status": "success",
                "message": "Dashboard pubblicato su Google",
                "url": sharing_link,
                "file_id": file.get('id')
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def create_shared_link(self, google_drive_file_id: str) -> str:
        """Crea link condivisibile per dashboard"""
        return f"https://drive.google.com/file/d/{google_drive_file_id}/view?usp=sharing"

# Utilizzo in app.py
if st.button("🌐 Apri Dashboard nel Browser"):
    manager = GoogleDashboardManager()
    result = manager.open_dashboard_in_browser()
    st.success(result['message'])

if st.button("📤 Pubblica su Google Drive"):
    manager = GoogleDashboardManager(service_account_key="path/to/key.json")
    # Converti Streamlit app a HTML
    dashboard_html = convert_streamlit_to_html(st)
    result = manager.publish_to_google_sites(dashboard_html, "My Dashboard")
    if result['status'] == 'success':
        st.success(f"✅ Aperto qui: {result['url']}")
```

#### 7.3 HTML Export per Google Pages

```python
# Converti Streamlit a HTML statico

class StreamlitToHTML:
    """Esporta dashboard Streamlit a HTML statico"""
    
    @staticmethod
    def export_dashboard(app_state: Dict) -> str:
        """Crea HTML versione del dashboard"""
        
        html_template = """
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Interactive Dashboard</title>
            <link rel="stylesheet" href="https://cdn.plot.ly/plotly-latest.min.js">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'IBM Plex Sans', sans-serif; background: #f9fafb; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }
                .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
                .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
                .kpi-card { background: white; padding: 1.5rem; border-left: 4px solid #667eea; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                .kpi-title { color: #6b7280; font-size: 0.875rem; font-weight: 500; }
                .kpi-value { font-size: 2rem; font-weight: bold; color: #1f2937; }
                .chart-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 2rem; }
                .chart { background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                .filter-bar { background: white; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                button { background: #667eea; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; }
                button:hover { background: #5568d3; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Interactive Dashboard</h1>
                <p>Real-time Data Analysis and Visualization</p>
            </div>
            
            <div class="container">
                {filters}
                {kpi_cards}
                {charts}
            </div>
            
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <script>
                {interactive_js}
            </script>
        </body>
        </html>
        """
        
        return html_template
```

---

## 8. RILEVAMENTO E CORREZIONE ERRORI

### 🛠️ Sistema Robusto di Error Handling

#### 8.1 Rilevamento Errori Automatico

```python
# src/error_handler.py (NUOVO)

import logging
from typing import Tuple, Optional
import traceback

class DashboardErrorHandler:
    """Rileva e corregge automaticamente errori nei file e dati"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.errors_found = []
        self.corrections_applied = []
    
    def validate_and_repair_file(self, file_path: str) -> Tuple[bool, pd.DataFrame, List[str]]:
        """
        Valida file e applica correzioni automatiche
        
        Returns:
            (is_valid, dataframe, list_of_corrections_applied)
        """
        
        corrections = []
        
        try:
            # Step 1: Carica file
            df = self._load_file_safely(file_path)
            
            # Step 2: Rileva problemi comuni
            issues = self._detect_common_issues(df)
            
            # Step 3: Applica correzioni
            for issue_type, details in issues:
                fixed_df, correction_msg = self._fix_issue(df, issue_type, details)
                if fixed_df is not None:
                    df = fixed_df
                    corrections.append(correction_msg)
            
            # Step 4: Validazione finale
            final_checks = self._final_validation(df)
            if not final_checks['valid']:
                return False, df, corrections + [final_checks['message']]
            
            return True, df, corrections
        
        except Exception as e:
            self.logger.error(f"Critical error in file validation: {str(e)}")
            return False, None, [f"Error: {str(e)}"]
    
    def _load_file_safely(self, file_path: str) -> pd.DataFrame:
        """Carica file con gestione errori"""
        
        ext = Path(file_path).suffix.lower()
        
        try:
            if ext == '.csv':
                return pd.read_csv(file_path, encoding='utf-8')
            elif ext in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            elif ext == '.json':
                return pd.read_json(file_path)
            else:
                raise ValueError(f"File type {ext} non supportato")
        
        except UnicodeDecodeError:
            # Prova encodings alternativi
            self.logger.warning("UTF-8 decoding failed, trying alternatives")
            for encoding in ['latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    return pd.read_csv(file_path, encoding=encoding)
                except:
                    continue
            raise ValueError("File encoding non determinabile")
    
    def _detect_common_issues(self, df: pd.DataFrame) -> List[Tuple]:
        """Rileva problemi comuni nei dati"""
        
        issues = []
        
        # 1. Colonne duplicate
        if df.columns.duplicated().any():
            issues.append(('duplicate_columns', df.columns[df.columns.duplicated()].tolist()))
        
        # 2. Righe duplicate
        if df.duplicated().any():
            issues.append(('duplicate_rows', df.duplicated().sum()))
        
        # 3. Valori mancanti
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            issues.append(('missing_values', missing_cols))
        
        # 4. Colonne vuote
        empty_cols = [col for col in df.columns if df[col].isnull().all()]
        if empty_cols:
            issues.append(('empty_columns', empty_cols))
        
        # 5. Anomalie tipologia dati
        for col in df.columns:
            if self._detect_type_mismatch(df, col):
                issues.append(('type_mismatch', col))
        
        # 6. Outliers estremi
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            outliers = self._detect_outliers(df[col])
            if outliers['count'] > 0:
                issues.append(('outliers', (col, outliers)))
        
        return issues
    
    def _fix_issue(self, df: pd.DataFrame, issue_type: str, 
                   details) -> Tuple[Optional[pd.DataFrame], str]:
        """Applica correzioni automatiche"""
        
        if issue_type == 'duplicate_columns':
            # Rimuovi colonne duplicate
            df = df.loc[:, ~df.columns.duplicated()]
            return df, f"✅ Rimosse {len(details)} colonne duplicate"
        
        elif issue_type == 'duplicate_rows':
            # Rimuovi righe duplicate
            df = df.drop_duplicates()
            return df, f"✅ Rimosse {details} righe duplicate"
        
        elif issue_type == 'missing_values':
            # Strategie di imputazione
            for col in details:
                if df[col].dtype in ['int64', 'float64']:
                    # Colonne numeriche: usa mediana
                    df[col].fillna(df[col].median(), inplace=True)
                    action = f"imputazione con mediana"
                else:
                    # Colonne categoriche: usa moda
                    df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
                    action = f"imputazione con moda"
            
            return df, f"✅ Riempiti valori mancanti in {len(details)} colonne ({action})"
        
        elif issue_type == 'empty_columns':
            # Rimuovi colonne completamente vuote
            df = df.drop(columns=details)
            return df, f"✅ Rimosse {len(details)} colonne vuote"
        
        elif issue_type == 'type_mismatch':
            # Converti tipi dati
            col = details
            if df[col].dtype == 'object':
                # Prova a convertire a numerico
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    return df, f"✅ Colonna {col} convertita a numerico"
                except:
                    pass
                
                # Prova a convertire a data
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    return df, f"✅ Colonna {col} convertita a data"
                except:
                    pass
        
        elif issue_type == 'outliers':
            col, outlier_data = details
            # Sostituisci outliers con limite (capping)
            lower_bound = outlier_data['q1'] - 1.5 * (outlier_data['q3'] - outlier_data['q1'])
            upper_bound = outlier_data['q3'] + 1.5 * (outlier_data['q3'] - outlier_data['q1'])
            
            df[col] = df[col].clip(lower_bound, upper_bound)
            return df, f"✅ {outlier_data['count']} outliers in {col} corretti"
        
        return None, "❌ Impossibile applicare correzione"
    
    def _final_validation(self, df: pd.DataFrame) -> Dict:
        """Validazione finale prima di accettare i dati"""
        
        checks = {
            'has_data': len(df) > 0,
            'has_columns': len(df.columns) > 0,
            'valid_dtypes': self._validate_dtypes(df)
        }
        
        valid = all(checks.values())
        
        return {
            'valid': valid,
            'message': 'Validazione superata' if valid else 'Validazione fallita',
            'details': checks
        }
    
    def _detect_type_mismatch(self, df: pd.DataFrame, col: str) -> bool:
        """Rileva se colonna ha tipo dati sbagliato"""
        
        col_data = df[col].dropna()
        
        if col_data.dtype == 'object':
            # Se colonna è object, controlla se potrebbe essere altro
            sample = col_data.head(10)
            
            # Prova numerico
            try:
                pd.to_numeric(sample)
                return True  # Potrebbe essere numerico
            except:
                pass
            
            # Prova data
            try:
                pd.to_datetime(sample)
                return True  # Potrebbe essere data
            except:
                pass
        
        return False
    
    def _detect_outliers(self, series: pd.Series) -> Dict:
        """Rileva outliers usando IQR method"""
        
        if series.dtype not in ['int64', 'float64']:
            return {'count': 0}
        
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = (series < lower_bound) | (series > upper_bound)
        
        return {
            'count': outliers.sum(),
            'q1': Q1,
            'q3': Q3,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
    
    def _validate_dtypes(self, df: pd.DataFrame) -> bool:
        """Verifica che i tipi dati siano validi"""
        return True  # Placeholder

# Utilizzo in app.py
error_handler = DashboardErrorHandler()
is_valid, df, corrections = error_handler.validate_and_repair_file(uploaded_file.path)

if not is_valid:
    st.error("❌ File non valido e impossibile da correggere automaticamente")
    for correction in corrections:
        st.warning(correction)
else:
    if corrections:
        st.info("⚙️ Correzioni applicate:")
        for correction in corrections:
            st.success(correction)
```

#### 8.2 User-Friendly Error Messages

```python
class ErrorMessageFormatter:
    """Formatta messaggi d'errore in modo amichevole"""
    
    ERROR_MESSAGES = {
        'file_not_found': '📁 File non trovato. Verifica il percorso e riprova.',
        'encoding_error': '🔤 Problema di codifica file. Prova a salvare il file come UTF-8.',
        'invalid_format': '📊 Formato file non supportato. Usa CSV, Excel o JSON.',
        'empty_file': '📭 Il file è vuoto. Assicurati di avere dati validi.',
        'no_numeric_data': '🔢 Nessun dato numerico trovato. Aggiungi colonne numeriche.',
        'all_nan_column': '❌ Una o più colonne sono completamente vuote.',
        'memory_error': '💾 Dataset troppo grande. Prova a caricare un file più piccolo.',
    }
    
    @staticmethod
    def format_error(error_type: str, context: Dict = None) -> str:
        """Restituisce messaggio d'errore user-friendly"""
        
        base_message = ErrorMessageFormatter.ERROR_MESSAGES.get(
            error_type, 
            "❌ Errore sconosciuto"
        )
        
        if context:
            for key, value in context.items():
                base_message = base_message.replace(f"{{{key}}}", str(value))
        
        return base_message
```

---

## 9. ARCHITETTURA TECNICA

### 📐 Stack Tecnologico

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Streamlit UI + HTML/CSS/JavaScript                  │   │
│  │  Plotly.js per Charts Interattivi                    │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│              Application Layer (Streamlit App)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  app.py                                              │   │
│  │  ├─ File Upload & Preview                           │   │
│  │  ├─ Filter Manager                                  │   │
│  │  ├─ Dashboard Rendering                             │   │
│  │  └─ Export Orchestration                            │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                     Logic Layer (src/)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ML_Analyzer         → Feature detection + Trends   │   │
│  │  KPI_Calculator      → Automatic KPI identification │   │
│  │  Dashboard_Generator → Dashboard assembly           │   │
│  │  Charts_Intelligent  → Chart selection algorithm    │   │
│  │  Layout_Randomizer   → Dynamic layout generation    │   │
│  │  Filter_System       → Filter logic                 │   │
│  │  Error_Handler       → Validation + Repairs         │   │
│  │  Tableau_Exporter    → TWBX generation              │   │
│  │  PDF_Generator       → Professional PDF             │   │
│  │  Google_Integration  → Cloud deployment             │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                      Data Layer                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  pandas - Data manipulation + analysis               │   │
│  │  scikit-learn - ML algorithms                        │   │
│  │  numpy - Numerical computing                         │   │
│  │  plotly - Interactive visualizations                 │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                  Storage & Export                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Local: CSV, JSON                                    │   │
│  │  Tableau: TWBX (zipped structure)                    │   │
│  │  Report: PDF professional                            │   │
│  │  Cloud: Google Drive, Google Cloud Storage           │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│              External Services (Optional)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Google Cloud Run - Hosting                          │   │
│  │  Tableau Online - Dashboard hosting                  │   │
│  │  Google Drive - File storage                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 📦 Dipendenze Principali

```txt
# requirements.txt (Versione 5.0)

# Frontend & UI
streamlit>=1.28.0
streamlit-option-menu>=0.3.2

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Machine Learning
scikit-learn>=1.3.0
scipy>=1.11.0

# Visualization
plotly>=5.17.0
matplotlib>=3.7.0
seaborn>=0.12.0

# File Handling
openpyxl>=3.1.0
xlrd>=2.0.0
python-dateutil>=2.8.2

# Export & Generation
reportlab>=4.0.0
python-pptx>=0.6.21

# Cloud Integration
google-cloud-storage>=2.0.0
google-cloud-run>=0.4.0
google-auth>=2.0.0

# Utilities
python-dotenv>=1.0.0
requests>=2.31.0
```

---

## 10. ROADMAP IMPLEMENTAZIONE

### ✅ Phase 1: Consolidamento Base (Settimana 1-2)
- [x] Estendere KPI Calculator
- [ ] Implementare Layout Randomizer avanzato
- [ ] Migliorare Intelligent Chart Selection
- [ ] Aggiungiamo Accessibility features

### 🚀 Phase 2: Export Avanzato (Settimana 3-4)
- [ ] Tableau Exporter (TWBX generation)
- [ ] PDF Generator professionale
- [ ] Zip Packager
- [ ] Error Handler robust

### 🌐 Phase 3: Cloud Integration (Settimana 5-6)
- [ ] Google Cloud Setup
- [ ] Dashboard Auto-Open
- [ ] Google Sites Integration
- [ ] URL Sharing

### 🔧 Phase 4: Polish & Testing (Settimana 7-8)
- [ ] End-to-end testing
- [ ] User acceptance testing
- [ ] Performance optimization
- [ ] Documentation completa

---

## 📊 Metriche di Successo

| Metrica | Target | Status |
|---------|--------|--------|
| Tempo caricamento dashboard | < 3 secondi | ⏳ |
| KPI detection accuracy | > 95% | ⏳ |
| Export success rate | 99% | ⏳ |
| Error detection rate | > 98% | ⏳ |
| User satisfaction | > 4.5/5 | ⏳ |
| Tableau compatibility | 100% | ⏳ |

---

## 🎓 Conclusione

Questo piano strategico fornisce una **roadmap completa** per trasformare il tuo progetto in una **soluzione professionale e robusta** per la generazione di dashboard. 

**Key Takeaways:**
1. ✅ Sistema automatico di KPI detection basato su ML
2. ✅ Layout dinamico che cambia ad ogni caricamento
3. ✅ Selezione intelligente di grafici professionale
4. ✅ Filtri interattivi per user engagement
5. ✅ Export Tableau + PDF + Zip completo
6. ✅ Integrazione Google per accesso cloud
7. ✅ Error handling automatico e user-friendly
8. ✅ Accessibilità professionale (WCAG 2.1)

**Prossimi Passi:**
→ Inizia con Phase 1: KPI Calculator
→ Espandi Layout Randomizer
→ Implementa Error Handler
→ Testa end-to-end
→ Pubblica su Google Cloud

---

**Creato il**: 12 Maggio 2026
**Versione**: 5.0 - Piano Strategico Completo
**Autore**: AI Dashboard Architect
