# 📊 SPECIFICA DI DESIGN DASHBOARD - VERSIONE 4.0
**Data**: 11 Maggio 2026  
**Progetto**: AI Data Engineer Dashboard Generator - Redesign Completo  
**Versione**: 4.0  
**Obiettivo**: Trasformare una dashboard confusa in una soluzione intuitiva, responsive e dinamica

---

## 📋 INDICE
1. [Visione Generale](#visione-generale)
2. [Principi di Design](#principi-di-design)
3. [Architettura Layout](#architettura-layout)
4. [Componenti UI](#componenti-ui)
5. [Sistema Responsivo](#sistema-responsivo)
6. [Dinamica e Variabilità](#dinamica-e-variabilità)
7. [Tabelle Interactive](#tabelle-interactive)
8. [Accessibilità](#accessibilità)
9. [Usabilità Multi-livello](#usabilità-multi-livello)
10. [Implementazione Tecnica](#implementazione-tecnica)

---

## 🎯 VISIONE GENERALE

### Obiettivi Principali
La dashboard v4.0 deve trasformare il modo in cui gli utenti interagiscono con i dati:

✅ **Intuitività**: Ogni elemento ha uno scopo chiaro, nessuna confusione  
✅ **Dinamismo**: Layout che cambia ad ogni caricamento, mantenendo coerenza visiva  
✅ **Responsività**: Perfetto su mobile, tablet, desktop, ultrawide  
✅ **Accessibilità**: Usabile da chiunque, indipendentemente dalle competenze tecniche  
✅ **Interattività**: Filtri dinamici, zoom, drill-down sui dati  
✅ **Performance**: Caricamento rapido, nessun lag nelle interazioni  

### Target Utenti
1. **Principianti**: Non tech-savvy, preferiscono visualizzazioni semplici
2. **Intermediate**: Analisti junior con discreta familiarità con i dati
3. **Expert**: Data scientist, analisti senior che cercano insights profonde

---

## 🎨 PRINCIPI DI DESIGN

### 1. Gerarchia Visuale Chiara
```
┌─────────────────────────────────────────────────┐
│  HEADER PRINCIPALE                              │
│  (Titolo, Metadati, Data Upload)               │
├─────────────────────────────────────────────────┤
│  SEZIONE CONTROLS (Filtri globali)             │
├─────────────────────────────────────────────────┤
│  SEZIONE INSIGHTS (Blocchi dinamici)           │
│  (Layout variabile 1-4 colonne)                │
├─────────────────────────────────────────────────┤
│  SEZIONE CHARTS (Grafici intelligenti)         │
│  (Disposizione casuale ma bilanciata)          │
├─────────────────────────────────────────────────┤
│  SEZIONE TABLES (Tabelle con filtri)           │
└─────────────────────────────────────────────────┘
```

### 2. Palette Colori
**Colori Primari**:
- Blu Primario: `#667eea` (Affidabilità, informazione)
- Viola Accento: `#764ba2` (Creatività, innovazione)
- Verde Successo: `#10b981` (Positivo, buono)
- Rosso Avvertimento: `#ef4444` (Negativo, attenzione)
- Arancio Info: `#f59e0b` (Neutrale, attenzione)
- Grigio Sfondo: `#f3f4f6` (Neutrale, pulizia)

**Utilizzo**:
- KPI Positivi: Verde
- KPI Negativi: Rosso
- KPI Neutrali: Blu
- Background Cards: Bianco con bordo sinistro colorato
- Hover Effects: Ombra leggera + lift di 2px

### 3. Tipografia
- **Header 1** (Titoli sezioni): IBM Plex Sans, 28px, Bold, `#1f2937`
- **Header 2** (Sottotitoli): IBM Plex Sans, 20px, SemiBold, `#374151`
- **Header 3** (Label): IBM Plex Sans, 16px, Medium, `#4b5563`
- **Body**: IBM Plex Sans, 14px, Regular, `#6b7280`
- **Label dati**: IBM Plex Mono, 13px, Regular, `#374151`
- **Numeri KPI**: IBM Plex Mono, 32px, Bold, `#1f2937`

### 4. Spacing System
Basato su scale di 8px:
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px

### 5. Border Radius
- Piccoli elementi: 4px
- Cards: 8px
- Dialog/Modal: 12px

---

## 🏗️ ARCHITETTURA LAYOUT

### Layout Grid Adattivo

La dashboard usa un sistema di grid CSS che si adatta automaticamente:

```
Desktop (1920px+):     3-4 colonne
Laptop (1366px):       2-3 colonne  
Tablet (768px):        1-2 colonne
Mobile (375px):        1 colonna
```

### Struttura a Sezioni

#### SEZIONE 1: Header Principale
```
┌─────────────────────────────────────────┐
│ 🤖 AI Dashboard Generator v4.0          │
│                                         │
│ Dataset: "sales_data.csv" (15.2 MB)    │
│ Righe: 12,450 | Colonne: 24 | Carica:  │
│ File Info: CSV | Encoding: UTF-8       │
│                                         │
│ Ultimo aggiornamento: 2 min fa          │
└─────────────────────────────────────────┘
```
**Componenti**:
- Logo + Titolo versione
- Nome file caricato
- Metadati dataset (dimensioni, encoding)
- Timestamp ultimo aggiornamento
- Pulsante Quick Actions (Download, Share, Refresh)

#### SEZIONE 2: Control Bar (Filtri Globali)
```
┌────────────┬──────────────┬─────────┬──────────┐
│ 📅 Data    │ 🏷️ Categoria│ 🔢 Range│ 🔄 Reset │
│ Range Pick │ Multi-Select │ Slider  │ Button   │
└────────────┴──────────────┴─────────┴──────────┘
```
**Caratteristiche**:
- Filtri sticky in alto (rimanenti visibili durante scroll)
- UI compatta su mobile
- Applicazione filtri in tempo reale (con debounce su range)
- Pulsante Reset visibile sempre

#### SEZIONE 3: KPI Metrics (Layout Dinamico)
**Variazione 1 (1 colonna)**:
```
┌─────────────────────┐
│ 💰 Ricavi Totali   │
│ $1,234,567         │
│ ↑ 12.5% vs mese    │
└─────────────────────┘
┌─────────────────────┐
│ 📊 Ordini Completati│
│ 2,456              │
│ ↑ 8.3% vs mese     │
└─────────────────────┘
```

**Variazione 2 (2 colonne)**:
```
┌──────────────────┬──────────────────┐
│ 💰 Ricavi Totali │ 📊 Ordini        │
│ $1,234,567       │ 2,456            │
│ ↑ 12.5%          │ ↑ 8.3%           │
└──────────────────┴──────────────────┘
```

**Variazione 3 (3 colonne)**:
```
┌──────────────┬──────────────┬──────────────┐
│ 💰 Ricavi    │ 📊 Ordini    │ 👥 Clienti   │
│ $1.2M        │ 2,456        │ 234          │
│ ↑ 12.5%      │ ↑ 8.3%       │ ↓ 2.1%       │
└──────────────┴──────────────┴──────────────┘
```

**Variazione 4 (4 colonne)**:
```
┌─────────┬─────────┬─────────┬─────────┐
│ Ricavi  │ Ordini  │ Clienti │ AOV     │
│ $1.2M   │ 2,456   │ 234     │ $501    │
│ ↑12.5%  │ ↑8.3%   │ ↓2.1%   │ ↑15.2%  │
└─────────┴─────────┴─────────┴─────────┘
```

**Algoritmo Dinamico di Selezione**:
```python
# Numero di KPI visibili: 3-8 (varia ogni caricamento)
num_kpis = random.choice([3, 4, 6, 8])

# Colonne rispetto alla risoluzione:
if viewport_width >= 1920:
    cols = [4, 2, 2, 3, 4]  # Possibili configurazioni
elif viewport_width >= 1366:
    cols = [3, 2, 3, 2]
else:
    cols = [2, 1, 2]

# Selezione configurazione casuale
selected_cols = random.choice(cols)
selected_kpis = select_top_kpis(num_kpis)  # Intelligente: sceglie i KPI più rilevanti
```

#### SEZIONE 4: Charts Intelligenti (Disposizione Dinamica)
**Principi**:
1. **Nessun grafico vuoto**: Se i dati non supportano un grafico, usa una tabella
2. **Varietà visiva**: Alternanza tra bar, line, pie, scatter, heatmap
3. **Profondità di insight**: Grafici ordinati per rilevanza
4. **Responsive**: Charts si impilano su mobile

**Configurazioni Layout (cambiano ogni caricamento)**:

**Configurazione A**: Focus su trend
```
┌─────────────────────────────────────┐
│  📈 Trend Ricavi (Line Chart)       │
│  [Grafico ampio, tutta larghezza]   │
├─────────────┬───────────────────────┤
│ 📊 Categ    │  🎯 Top 10 Prodotti  │
│ (Pie Chart) │  (Bar Horiz Chart)   │
└─────────────┴───────────────────────┘
```

**Configurazione B**: Focus su correlazioni
```
┌──────────────────┬──────────────────┐
│  📊 X vs Y       │  🔥 Heatmap      │
│  (Scatter)       │  (Correlazioni)  │
├──────────────────┴──────────────────┤
│  📈 Distribuzione Valori             │
│  (Box Plot)                          │
└──────────────────────────────────────┘
```

**Configurazione C**: Focus su composizione
```
┌──────────────────────────────────────┐
│  📊 Composizione Categoria (Stacked)│
├──────────────────┬───────────────────┤
│  🎯 Top Values   │  📉 Bottom Values │
│  (Bar)           │  (Bar)            │
└──────────────────┴───────────────────┘
```

#### SEZIONE 5: Tabelle Interactive con Filtri
```
┌─────────────────────────────────────────┐
│ 📋 Dati Dettagliati                     │
├─────────────────────────────────────────┤
│ [Filtri inline]  [Ricerca]  [Export]    │
├─────────────────────────────────────────┤
│ Colonna 1 | Colonna 2 | Colonna 3 | ... │
├─────────────────────────────────────────┤
│ Dato 1    | Dato 2    | Dato 3    | ... │
│ Dato 4    | Dato 5    | Dato 6    | ... │
│ ...                                     │
├─────────────────────────────────────────┤
│ [Prev] 1 2 3 4 5 [Next] | Pagina 1/234  │
└─────────────────────────────────────────┘
```

**Funzionalità Tabella**:
- Filtri colonna (per tipo: testo, numerico, data)
- Sorting multi-colonna
- Ricerca globale (regex support)
- Paginazione adattiva (10, 25, 50, 100 righe)
- Export singola colonna o full dataset
- Evidenziazione righe sospette (valori outlier)
- Tooltips per colonne lunghe
- Selezione multipla righe con azioni batch

---

## 🎯 COMPONENTI UI

### KPI Card (Metrica Singola)
```
┌─────────────────────────────────┐
│ 💰 Ricavi Totali               │
│                                 │
│ $1,234,567                      │
│ ↑ 12.5% vs periodo precedente   │
│                                 │
│ [Visualizza dettagli →]         │
└─────────────────────────────────┘
```

**Varianti**:
- **Positivo**: Bordo verde, freccia su
- **Negativo**: Bordo rosso, freccia giù
- **Neutro**: Bordo blu, nessuna freccia
- **Attenzione**: Bordo arancio, punto esclamativo

**CSS**:
```css
.kpi-card {
  background: white;
  border-left: 4px solid var(--color);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

### Filter Pill
```
[📅 Data] [Filter Icon] [Clear X]
```
- Mostra filtri attivi come pills removibili
- Mostra numero record filtrati
- Design compatto su mobile

### Chart Container
```
┌────────────────────────────────┐
│ 📈 Titolo Grafico              │
│ [Info] [Fullscreen] [Download]│
├────────────────────────────────┤
│                                │
│  [Grafico Plotly]              │
│  (Interactive hover)           │
│                                │
└────────────────────────────────┘
```

**Interazioni**:
- Hover: Mostra valori esatti
- Click legend: Toggle serie
- Fullscreen: Ingrandisce grafico
- Download: Salva come PNG/SVG

### Table Toolbar
```
[Ricerca 🔍] [Filtri ⚙️] [Export ↓] [Colonne 👁️]
```
- Ricerca globale con match highlighting
- Filtri per colonna (dropdown/range/date picker)
- Export multi-formato (CSV, Excel, JSON)
- Toggle visibilità colonne

---

## 📱 SISTEMA RESPONSIVO

### Breakpoints Definiti
```
Extra Large (xl):  ≥ 1920px    → 4 colonne charts, 4 KPI
Large (lg):        1366-1919px → 3 colonne charts, 3 KPI
Medium (md):       768-1365px  → 2 colonne charts, 2 KPI
Small (sm):        375-767px   → 1 colonna charts, 1-2 KPI
Extra Small (xs):  < 375px     → 1 colonna charts, stacked KPI
```

### Layout Fluido per Charts
```python
# Logica di disposizione
def calculate_chart_layout(num_charts, viewport_width):
    if viewport_width >= 1920:
        # 4 colonne: 2x2, 2x2, ecc.
        return {'cols': 4, 'arrangement': '2-2-2-2'}
    elif viewport_width >= 1366:
        # 3 colonne: 1-2, 2-1, ecc.
        return {'cols': 3, 'arrangement': '1-2-1-2-1'}
    elif viewport_width >= 768:
        # 2 colonne: 1-1, 2, 1-1
        return {'cols': 2, 'arrangement': '1-1-2-1-1'}
    else:
        # 1 colonna: stacked
        return {'cols': 1, 'arrangement': '1-1-1-1'}
```

### Modifica Header su Mobile
```
Desktop:
┌──────────────────────────────────────┐
│ 🤖 AI Dashboard v4.0 | Info | Actions│
└──────────────────────────────────────┘

Mobile:
┌─────────────────┐
│ 🤖 AI Dash v4.0 │
│ Info | Actions  │
└─────────────────┘
```

### Tabella Responsive
**Desktop**: Tabella classica orizzontale
**Mobile**: Card view verticalizzato
```
┌─────────────────────┐
│ Nome Cliente        │
│ > Acme Inc          │
├─────────────────────┤
│ Email              │
│ contact@acme.com   │
├─────────────────────┤
│ Stato              │
│ Attivo             │
└─────────────────────┘
```

---

## ⚡ DINAMICA E VARIABILITÀ

### Algoritmo di Randomizzazione Controllata

**Goal**: Dashboard sempre fresca ma coerente

```python
import random
import hashlib
from datetime import datetime

class DashboardLayoutEngine:
    def __init__(self, seed=None):
        # Se seed=None, usa timestamp per variabilità
        # Se seed=hash(user_id), rende deterministica per utente
        self.seed = seed or int(datetime.now().timestamp() / 3600)
        random.seed(self.seed)
    
    def select_kpi_metrics(self, available_metrics: list, count: int = None):
        """
        Seleziona quali KPI mostrare
        """
        # Intelligente: priorità a metriche rilevanti
        scored_metrics = self._score_metrics(available_metrics)
        sorted_metrics = sorted(scored_metrics, key=lambda x: x['score'], reverse=True)
        
        # Randomizza però mantieni top metric sempre
        count = count or random.choice([3, 4, 6, 8])
        top_metric = sorted_metrics[0]
        remaining = sorted_metrics[1:]
        random.shuffle(remaining)
        
        selected = [top_metric] + remaining[:count-1]
        return selected
    
    def select_chart_arrangement(self, num_charts: int, viewport_width: int):
        """
        Seleziona disposizione dei grafici
        """
        # Definisci possibili arrangiamenti per breakpoint
        arrangements = {
            1920: ['2-2-2', '3-2-2', '4-1-2', '2-3-2'],
            1366: ['1-2-1-2', '2-1-2-1', '3-2-1', '1-3-2'],
            768: ['1-1-2-1', '2-1-1-2', '1-2-1'],
            0: ['1-1-1-1']
        }
        
        # Trova breakpoint appropriato
        breakpoint = next(bp for bp in sorted(arrangements.keys()) 
                         if viewport_width >= bp)
        
        possible = arrangements[breakpoint]
        selected = random.choice(possible)
        return self._parse_arrangement(selected)
    
    def select_chart_types(self, available_charts: list, num_charts: int):
        """
        Seleziona tipi di grafici mantenendo diversità
        """
        chart_types = ['line', 'bar', 'pie', 'scatter', 'heatmap', 'box']
        
        # Assicura diversità: non + di 2 dello stesso tipo
        selected = []
        type_counts = {}
        
        available_scored = self._score_charts(available_charts)
        random.shuffle(available_scored)
        
        for chart in available_scored:
            chart_type = chart['type']
            if type_counts.get(chart_type, 0) < 2:
                selected.append(chart)
                type_counts[chart_type] = type_counts.get(chart_type, 0) + 1
                
            if len(selected) >= num_charts:
                break
        
        return selected
    
    def _score_metrics(self, metrics):
        """
        Punteggio intelligente: correlazione con business goal,
        varianza, trend positivo, ecc.
        """
        # Implementazione specifica per ogni metrica
        scored = []
        for metric in metrics:
            score = 0
            # Varianza: metriche con buona varianza sono più interessanti
            score += metric.get('variance_score', 0) * 0.3
            # Trend: trend positivi sono preferiti
            score += metric.get('trend_score', 0) * 0.3
            # Completezza: dati completi preferiti
            score += (1 - metric.get('missing_rate', 0)) * 0.4
            
            scored.append({**metric, 'score': score})
        
        return scored
    
    def _score_charts(self, charts):
        """
        Punteggio grafici: quelli con dati significativi preferiti
        """
        scored = []
        for chart in charts:
            score = 0
            # Cardinale: no grafico se solo 1-2 valori
            if chart.get('cardinality', 0) > 3:
                score += 0.7
            # Completezza: no grafico con troppi null
            score += (1 - chart.get('null_rate', 0)) * 0.3
            
            scored.append({**chart, 'score': score})
        
        return [c for c in scored if c['score'] > 0.3]  # Filtra deboli
```

### Timing di Refresh Dinamico
```python
# Mantieni cache ma varia presentazione
@st.cache_data(ttl=3600)  # Cache per 1 ora
def analyze_and_recommend(df):
    """Analisi che rimane stabile per periodo"""
    return ml_analyzer.analyze(df)

# Ma layout varia ad ogni reload
if st.button("🔄 Refresh Layout"):
    st.session_state['layout_seed'] = None
    st.rerun()
```

---

## 📋 TABELLE INTERACTIVE

### Tabella Intelligente - Sezione Completa

#### 1. Header Tabella con Controlli
```
┌──────────────────────────────────────────────────────┐
│ 📋 Dati Dettagliati (2,456 record)                  │
│                                                       │
│ [Ricerca] [⚙️ Filtri] [📊 Statistiche] [↓ Export]   │
│                                                       │
│ Filtri attivi: [Stato: Attivo ✕] [Data: >2026 ✕]   │
└──────────────────────────────────────────────────────┘
```

#### 2. Corpo Tabella
```
┌─────────┬────────────┬──────────┬────────┬─────────┐
│ Seleziona│ Cliente    │ Data     │ Importo│ Stato   │
├─────────┼────────────┼──────────┼────────┼─────────┤
│ ☐       │ Acme Inc   │ 2026-05-11│$1.2K  │🟢 Attivo│
│ ☐       │ Tech Corp  │ 2026-05-10│$2.1K  │🟢 Attivo│
│ ☐       │ Startup XY │ 2026-05-09│$0.8K  │🟡 Pend. │
│ ☐       │ Global Ltd │ 2026-05-08│$3.4K  │🔴 Clos. │
└─────────┴────────────┴──────────┴────────┴─────────┘
```

**Caratteristiche Colonne**:
- **Ordinamento**: Click header per sort asc/desc
- **Drag**: Trascinare colonne per riordinarle
- **Resize**: Trascinare bordo colonna per allargare
- **Tooltip**: Hover su celle lunghe per vedere testo completo
- **Highlighting**: Outlier (valori > 3σ) in giallo

#### 3. Filtri Intelligenti per Tipo

**Colonna Testo**:
```
[Ricerca "Client..."]  [≠ Not equal] [= Contains]
```

**Colonna Numerica**:
```
[Min] [Max] [Equals] [Range Slider]
```

**Colonna Data**:
```
[Da Data] [A Data] [Custom Range]
```

**Colonna Categorica**:
```
[✓ Valore1] [✓ Valore2] [✓ Valore3] [Tutti] [Nessuno]
```

#### 4. Azioni Batch
```
[Selezionati 3 record]
[✎ Modifica] [📧 Email] [📥 Esporta] [🗑️ Elimina]
```

#### 5. Paginazione Intelligente
```
[Prev] 
  1 2 3 ... 12 13 [14] 15 16 ... 230 231
[Next]

Mostra: [10 ▼] record per pagina
```

#### 6. Statistiche Colonna
```
┌────────────────────────────┐
│ Statistiche Colonna        │
├────────────────────────────┤
│ Media:        $1,562       │
│ Mediana:      $1,200       │
│ Min:          $100         │
│ Max:          $5,000       │
│ Std Dev:      $1,234       │
│ Valori Null:  12 (0.5%)    │
└────────────────────────────┘
```

#### 7. Esportazione Dati
```
[Formato: CSV ▼]  [Includerti: Tutte le colonne ▼]
[Ordine: Corrente ▼]  [Righe: Filtrate ▼]

[📥 Esporta]
```

---

## ♿ ACCESSIBILITÀ

### WCAG 2.1 Compliance (Level AA)

#### 1. Contrasti Colore
```
✓ Testo su sfondo: 4.5:1 per corpo, 3:1 per heading
✓ KPI numeri: 7:1 (molto alto per leggibilità)
✓ Bordi grafici: 3:1 minimo
```

#### 2. Navigazione Tastiera
```
[Tab]         → Muove tra elementi
[Shift+Tab]   → Indietro
[Enter]       → Attiva button/link
[Space]       → Attiva checkbox/toggle
[Arrow Keys]  → Muove in selectbox
[Esc]         → Chiude modal/tooltip
```

**Esempio**:
```python
# Sezione filtri navigabile
with st.form(key='filters_form'):
    date_filter = st.date_input(
        "Data",
        help="Seleziona range di date (AccessKey: Alt+D)"
    )
    category_filter = st.multiselect(
        "Categoria",
        options=[...],
        help="Seleziona una o più categorie (AccessKey: Alt+C)"
    )
    submitted = st.form_submit_button("Applica Filtri")
```

#### 3. Screen Reader Support
```html
<!-- Ogni elemento ha aria-label -->
<button aria-label="Ripristina filtri">🔄 Reset</button>

<!-- Tabelle hanno associazioni header-cell -->
<table role="grid">
    <thead>
        <tr>
            <th id="col-cliente">Cliente</th>
            <th id="col-importo">Importo</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td headers="col-cliente">Acme Inc</td>
            <td headers="col-importo">$1,200</td>
        </tr>
    </tbody>
</table>
```

#### 4. Colori Significativi Secondari
```
❌ Non usare colore come unico indicatore
✓ Combina con iconografia e testo

Cattivo:  Ricavi sono aumentati  [barre rosse/verdi]
Buono:   Ricavi ↑ 12.5%          [✓ Verde + ↑ Freccia]
         Ordini ↓ 3.2%           [✗ Rosso + ↓ Freccia]
```

#### 5. Font Sizes Leggibili
```
Minimo assoluto: 12px
Preferibile: 14px corpo, 16px heading, 24px titoli
```

#### 6. Focus Indicators Chiari
```css
:focus {
    outline: 3px solid #667eea;
    outline-offset: 2px;
}
```

#### 7. Rispetto Preferenze Sistema
```python
# Rispetta dark mode preferenze
@media (prefers-color-scheme: dark) {
    body { background: #1f2937; color: #f3f4f6; }
}

# Rispetta preferenza movimento ridotto
@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}
```

---

## 👥 USABILITÀ MULTI-LIVELLO

### Profili Utente e Loro Percorsi

#### Profilo 1: Principiante (Non-tech)
**Caratteristiche**: Conosce poco di dati, cerca risposte rapide

**Interfaccia Semplificata**:
```
┌──────────────────────────────────────┐
│ 🤖 Analisi Automatica                │
│                                      │
│ Carica i tuoi dati:  [Scegli File]   │
│                      [Carica]         │
│                                      │
│ ────────────────────────────────────  │
│                                      │
│ 📊 INSIGHTS PRINCIPALI                │
│                                      │
│ Cosa è cambiato rispetto a ieri:    │
│ ✓ Ricavi +12.5%                     │
│ ✓ Nuovi Clienti +3                  │
│ ✗ Restituzione +1.2%                │
│                                      │
│ 📈 Grafici Automatici                │
│ [Grafico 1]  [Grafico 2]             │
│ [Grafico 3]  [Grafico 4]             │
│                                      │
│ [📥 Scarica Report] [Ricevi Email]   │
└──────────────────────────────────────┘
```

**Funzionalità Chiave**:
- Mode "Guida" con spiegazioni
- Pulsante "Cosa significava?" su ogni metrica
- Assistente AI che spiega i dati in linguaggio naturale
- Rapporto automatico email
- Opzione "Mostra di più" per avanzato

#### Profilo 2: Intermediate (Analista)
**Caratteristiche**: Conosce analisi dati, cerca dettagli e controllo

**Interfaccia Standard** (quella descritta sopra):
```
┌──────────────────────────────────────┐
│ 🤖 AI Dashboard Generator v4.0       │
│                                      │
│ [Carica Dati] [Ultimo Caricamento]   │
│                                      │
│ ┌─ Filtri ────────────────────────┐ │
│ │ 📅 Data: [Range Picker]         │ │
│ │ 🏷️  Categoria: [Multi-select]   │ │
│ │ 🔢 Importo: [Min] [Max] [Slider]│ │
│ │                [🔄 Reset Filtri]│ │
│ └──────────────────────────────────┘ │
│                                      │
│ 📊 KPI DASHBOARD                     │
│ [KPI1] [KPI2] [KPI3] [KPI4]          │
│                                      │
│ 📈 ANALISI GRAFICA                   │
│ [Chart1] [Chart2]                    │
│ [Chart3] [Chart4]                    │
│                                      │
│ 📋 DATI DETTAGLIATI                  │
│ [Filtri Colonna] [Sorting] [Export]  │
│ [Tabella Interattiva]                │
│                                      │
│ 🔍 ANOMALIE                          │
│ Valori outlier evidenziati           │
│                                      │
│ 📊 STATISTICHE                       │
│ [Tab Statistiche Descrittive]        │
└──────────────────────────────────────┘
```

**Funzionalità Chiave**:
- Tutti i filtri e controlli
- Esportazione multi-formato
- Salvataggio viste personalizzate
- Annotazioni su grafici
- Comparazione dataset

#### Profilo 3: Expert (Data Scientist)
**Caratteristiche**: Ricerca insights avanzati, algoritmi, predizioni

**Interfaccia Esperta** (Sezione Collapsibile "Modalità Avanzata"):
```
┌────────────────────────────────────────┐
│ [🔧 Modalità Avanzata]                 │
├────────────────────────────────────────┤
│                                        │
│ 📐 ANALISI STATISTICA AVANZATA         │
│ ┌──────────────────────────────────┐  │
│ │ Test Statistici                  │  │
│ │ [t-test] [Chi-square] [ANOVA]   │  │
│ │                                  │  │
│ │ Correlazione & Causalità         │  │
│ │ [Pearson] [Spearman] [Kendall]  │  │
│ │                                  │  │
│ │ Clustering & Segmentazione       │  │
│ │ [K-Means] [Hierarchical] [DBSCAN]│ │
│ └──────────────────────────────────┘  │
│                                        │
│ 🤖 MACHINE LEARNING                    │
│ ┌──────────────────────────────────┐  │
│ │ Modelli Predittivi               │  │
│ │ [Regressione] [Classificazione]  │  │
│ │ [Feature Importance] [SHAP]      │  │
│ └──────────────────────────────────┘  │
│                                        │
│ 💾 EXPORT TECNICO                      │
│ [SQL Query] [Python Code] [API]        │
│                                        │
│ 🔗 INTEGRAZIONI                        │
│ [Connetti Database] [API Setup]        │
│                                        │
└────────────────────────────────────────┘
```

**Funzionalità Chiave**:
- Test statistici e p-value
- Feature engineering
- Model evaluation metrics
- Codice Python/SQL generato
- Accesso a algoritmi avanzati

### Context-Sensitive Help
```
Ogni elemento ha:
1. Tooltip on-hover (200ms delay)
2. "?" icon link a documentazione
3. Modalità "Tutorial" per nuovi utenti
4. Video embedding per funzioni complesse
```

---

## 🛠️ IMPLEMENTAZIONE TECNICA

### Architettura Tecnica

```
app.py (Main)
├── 1. Layout Engine
│   ├── responsive_layout.py
│   └── layout_randomizer.py
├── 2. Components
│   ├── kpi_cards.py
│   ├── charts_intelligent.py
│   ├── tables_interactive.py
│   └── filter_system.py
├── 3. Data Processing
│   ├── data_cleaner.py
│   ├── data_validator.py
│   └── outlier_detector.py
├── 4. ML & Analytics
│   ├── ml_analyzer.py (esistente)
│   └── correlation_engine.py
└── 5. Utilities
    ├── accessibility.py
    ├── export_handler.py
    └── theme_manager.py
```

### Stack Tecnologico
```
Frontend:
  - Streamlit 1.32+ (base)
  - Plotly 5.0+ (grafici interattivi)
  - Streamlit-Elements (layout avanzato)
  - Streamlit-Dataframe (tabelle avanzate)
  - Streamlit-Aggrid (grid avanzata)

Backend:
  - Pandas 2.0+ (data manipulation)
  - NumPy 1.24+ (calcoli numerici)
  - Scikit-learn 1.3+ (ML)
  - SciPy 1.11+ (statistiche)
  - SQLAlchemy 2.0+ (database)

DevOps:
  - Docker (containerizzazione)
  - GitHub Actions (CI/CD)
  - Streamlit Cloud (hosting)
```

### Moduli Principali da Creare/Modificare

#### 1. `responsive_layout.py`
```python
class ResponsiveLayoutEngine:
    """Gestisce layout responsivo della dashboard"""
    
    def get_viewport_config(self) -> dict:
        """Rileva dimensioni viewport e restituisce config"""
        pass
    
    def calculate_chart_grid(self, num_charts: int) -> list:
        """Calcola numero colonne per layout grafico"""
        pass
    
    def calculate_kpi_columns(self, num_kpis: int) -> int:
        """Calcola numero colonne per KPI"""
        pass
```

#### 2. `layout_randomizer.py`
```python
class DashboardLayoutRandomizer:
    """Randomizza layout mantenendo qualità"""
    
    def select_visible_kpis(self, all_metrics: list) -> list:
        """Seleziona KPI da mostrare"""
        pass
    
    def select_chart_types(self, num_charts: int) -> list:
        """Seleziona tipi di grafici da mostrare"""
        pass
    
    def randomize_arrangement(self) -> dict:
        """Randomizza disposizione elementi"""
        pass
```

#### 3. `kpi_cards.py`
```python
def render_kpi_card(metric: dict, col):
    """Renderizza singolo KPI con design definito"""
    pass

def render_kpi_grid(metrics: list, columns: int):
    """Renderizza griglia di KPI con wrapping automatico"""
    pass
```

#### 4. `charts_intelligent.py`
```python
class IntelligentChartSelector:
    """Seleziona grafici intelligenti basati su dati"""
    
    def recommend_chart_type(self, series: pd.Series) -> str:
        """Raccomanda tipo di grafico per serie"""
        pass
    
    def validate_chart_data(self, data: pd.DataFrame) -> bool:
        """Valida se dati adatti a grafico"""
        pass
```

#### 5. `tables_interactive.py`
```python
class InteractiveTable:
    """Tabella con filtri intelligenti, sorting, ecc"""
    
    def render_table(self, df: pd.DataFrame):
        """Renderizza tabella con UI completo"""
        pass
    
    def apply_filters(self, df: pd.DataFrame, filters: dict) -> pd.DataFrame:
        """Applica filtri intelligenti per tipo"""
        pass
    
    def detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rileva e evidenzia outlier"""
        pass
```

#### 6. `filter_system.py`
```python
class FilterSystem:
    """Sistema filtri globale intelligente"""
    
    def render_filter_bar(self) -> dict:
        """Renderizza control bar filtri"""
        pass
    
    def get_filter_value(self, filter_key: str) -> any:
        """Recupera valore filtro da session state"""
        pass
    
    def apply_all_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applica tutti i filtri attivi"""
        pass
```

#### 7. `accessibility.py`
```python
class AccessibilityManager:
    """Gestisce WCAG compliance"""
    
    def add_aria_labels(self, element, label: str):
        """Aggiunge aria-label a elemento"""
        pass
    
    def validate_contrast_ratio(self, fg: str, bg: str) -> float:
        """Valida rapporto contrasto colore"""
        pass
    
    def add_keyboard_nav(self):
        """Abilita navigazione tastiera"""
        pass
```

### Flusso di Esecuzione

```
1. User carica file
   ↓
2. Data cleaner / validator
   ↓
3. ML Analyzer (generate insights)
   ↓
4. Layout Randomizer (scegli cosa mostrare)
   ↓
5. Render Section 1: Header
   ↓
6. Render Section 2: Filter Bar
   ↓
7. Render Section 3: KPI Cards (dinamico)
   ↓
8. Render Section 4: Charts (dinamico)
   ↓
9. Render Section 5: Tables (con filtri)
   ↓
10. Rendering completo - utente interagisce
    ↓
11. Filters/Sorts/Clicks → rerun con state
```

### CSS Framework
```html
<style>
/* Variables */
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

/* Base Styles */
body {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--color-text-primary);
    background-color: var(--color-bg-secondary);
    line-height: 1.6;
}

/* Utilities */
.text-center { text-align: center; }
.text-muted { color: var(--color-text-secondary); }
.text-mono { font-family: 'IBM Plex Mono', monospace; }

/* Components */
.card {
    background: var(--color-bg-primary);
    border-radius: var(--radius-md);
    padding: var(--spacing-lg);
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.btn {
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-sm);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn:focus {
    outline: 3px solid var(--color-primary);
    outline-offset: 2px;
}

/* Grid Responsive */
.grid {
    display: grid;
    gap: var(--spacing-lg);
    grid-auto-flow: dense;
}

@media (max-width: 768px) {
    .grid { grid-template-columns: 1fr; }
}

@media (min-width: 769px) and (max-width: 1365px) {
    .grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1366px) {
    .grid { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1920px) {
    .grid { grid-template-columns: repeat(4, 1fr); }
}
</style>
```

---

## 📊 METRICHE DI SUCCESSO

Misurare il successo del redesign:

| Metrica | Target | Come Misurare |
|---------|--------|---------------|
| **Tempo caricamento pagina** | < 2s | Google Lighthouse |
| **Bounce rate** | < 10% | Google Analytics |
| **Session duration** | > 3 min | GA |
| **Accessibility score** | ≥ 95 WCAG AA | axe DevTools |
| **Mobile usability** | 100% | Mobile Lighthouse |
| **User satisfaction** | ≥ 4.5/5 | Post-session survey |
| **Feature discovery** | > 80% utenti trovano filtri | Event tracking |
| **Repeat visits** | > 60% | GA |

---

## 🚀 ROADMAP IMPLEMENTAZIONE

### Fase 1: Setup Base (1 settimana)
- [ ] Creare moduli di base
- [ ] Implementare responsive layout engine
- [ ] Setup CSS framework

### Fase 2: Core Features (2 settimane)
- [ ] Implementare KPI cards dinamiche
- [ ] Sistema filtri globale
- [ ] Tabelle interactive

### Fase 3: Grafici Intelligenti (2 settimane)
- [ ] Chart selector intelligente
- [ ] Layout randomizer
- [ ] Rendering dinamico grafici

### Fase 4: Accessibilità & Polish (1 settimana)
- [ ] WCAG compliance
- [ ] Testing su vari device
- [ ] Performance optimization

### Fase 5: Testing & Deploy (1 settimana)
- [ ] Testing completo
- [ ] Deploy staging
- [ ] Deploy production

---

## 📝 CONCLUSIONI

Questo documento specifica una dashboard v4.0 che:

✅ **Risolve confusione**: Layout chiaro, hierarchia visiva definita  
✅ **Adatta a spazio**: Sistema responsivo su tutti i breakpoint  
✅ **Professionalmente design**: Palette colori, tipografia, spacing coherente  
✅ **Dinamica**: Layout varia ad ogni caricamento, mantenendo qualità  
✅ **Interattiva**: Filtri, sort, drill-down, export dati  
✅ **Accessibile**: WCAG AA compliant, usabile da chiunque  
✅ **Multi-livello**: UI adatta a principianti, intermediate, expert  

**La dashboard diventa uno strumento di scoperta, non solo visualizzazione.**

---

**Documento preparato per lo sviluppo di AI Dashboard Generator v4.0**
