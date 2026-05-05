# 🎨 Sistema di Generazione Dashboard Intelligente

## 📋 Descrizione Generale

Questo sistema genera dashboard interattive e adattive che si adattano automaticamente a qualsiasi dataset. Ogni dashboard è unica e varia strutturalmente sulla base delle caratteristiche dei dati caricati.

---

## 🎯 Caratteristiche Principali

### 1. **KPI Dinamici e Intelligenti** (0 - infiniti)
- **Numero Totale Record**: Visualizza il totale dei record del dataset
- **Metriche Numeriche**: Media calcolata automaticamente per le colonne numeriche principali
- **Categoria Top**: Mostra la categoria più frequente nel dataset
- **Intervallo Temporale**: Se presente, visualizza l'intervallo di tempo dei dati
- **Completezza Dati**: Percentuale di dati non nulli nel dataset
- **Icone Emoji**: Ogni KPI include un'icona visiva distintiva per facile identificazione

**Vantaggi:**
- Adattamento automatico in base ai dati disponibili
- Evidenzia metriche rilevanti senza sovraccaricare
- Display ordinato e leggibile

---

### 2. **Filtri Intelligenti (Max 2)**
Il sistema suggerisce fino a **2 filtri intelligenti** in base al dataset:

#### **Filtro Categorico**
- Si attiva automaticamente se il dataset contiene colonne con 2-15 valori unici
- Permette la selezione facile tra categorie
- Icona: 🏷️

#### **Filtro Numerico (Range)**
- Permette di filtrare per range di valori
- Utile per selezionare sottoinsiemi di dati numerici
- Icona: 📊

#### **Filtro Temporale**
- Si attiva se il dataset contiene colonne date/datetime
- Range picker intuitivo
- Icona: 📅

---

### 3. **Mappe Interattive (Quando Applicabili)**
Il sistema rileva automaticamente dati geografici tramite:
- Colonne con keywords: `latitude`, `longitude`, `lat`, `lon`
- Colonne geografiche: `country`, `city`, `region`, `province`

Quando rilevati, viene aggiunta una **mappa interattiva Plotly** che visualizza:
- Dati geografici georeferenziati
- Clustering automatico di punti
- Zoom e pan interattivo

Icona: 🗺️

---

### 4. **Layout Randomico e Strutturalmente Vario**

Il sistema supporta **5 tipi di layout diversi**, scelti casualmente:

#### **Grid 2 Colonne** (grid_2col)
```
┌────────────┬────────────┐
│  Grafico 1 │  Grafico 2 │
├────────────┼────────────┤
│  Grafico 3 │  Grafico 4 │
├────────────┼────────────┤
│  Grafico 5 │  Grafico 6 │
└────────────┴────────────┘
```
- **Ideale per**: Dataset con 6-8 grafici
- **Bilanciamento**: Equilibrato
- **Focus**: Multicomparativo

#### **Grid 3 Colonne** (grid_3col)
```
┌────┬────┬────┐
│ G1 │ G2 │ G3 │
├────┼────┼────┤
│ G4 │ G5 │ G6 │
└────┴────┴────┘
```
- **Ideale per**: Dataset compatti con molti grafici
- **Bilanciamento**: Compatto
- **Focus**: Visione d'insieme

#### **Layout Asimmetrico** (asymmetric)
```
┌──────────────────┐
│   Grafico Grande │
├────────┬─────────┤
│ Grafico│Grafico 3│
├────────┼─────────┤
│ Grafico│Grafico 4│
└────────┴─────────┘
```
- **Ideale per**: Evidenziare un grafico principale
- **Bilanciamento**: Gerarchico
- **Focus**: Un grafico in primo piano

#### **Featured Layout** (featured)
```
┌──────────────────────┐
│   Grafico Principale │
│    (Larghezza Piena) │
├──────┬──────┬────────┤
│ KPI  │ KPI  │ KPI    │
├──────┴──────┴────────┤
│ Grafici di supporto  │
└──────────────────────┘
```
- **Ideale per**: Dataset critici
- **Bilanciamento**: Verticale
- **Focus**: Metrica principale

#### **Timeline Layout** (timeline)
```
Timeline Verticale
○ Milestone 1 [Grafico 1]
│
○ Milestone 2 [Grafico 2]
│
○ Milestone 3 [Grafico 3]
```
- **Ideale per**: Dati temporali
- **Bilanciamento**: Sequenziale
- **Focus**: Evoluzione nel tempo

---

### 5. **Selezione Intelligente di Grafici**

Il sistema sceglie automaticamente fino a **8 grafici** in base ai dati:

| Tipo Grafico | Icona | Requisiti | Descrizione |
|---|---|---|---|
| **Linea** | 📈 | Dati temporali + numerici | Trend nel tempo |
| **Barre** | 📊 | Dati categorici | Confronti per categoria |
| **Scatter** | 🔍 | 2+ metriche numeriche | Correlazione bivariata |
| **Bubble** | 🫧 | 3+ metriche numeriche | Correlazione multidimensionale |
| **Heatmap** | 🔗 | 3+ metriche numeriche | Matrice correlazioni |
| **Istogramma** | 📈 | Dati numerici | Distribuzione singola |
| **Box Plot** | 📦 | Dati numerici | Outlier e quartili |
| **Treemap** | 🗂️ | Categorici + numerici | Composizione gerarchica |
| **Radar** | 🔄 | 4+ metriche | Confronto multidimensionale |
| **Violin** | 🎻 | Dati numerici | Densità dettagliata |
| **Area** | 📊 | Dati temporali | Accumulo nel tempo |
| **Torta** | 🥧 | Categorici (≤8 valori) | Proporzioni totali |
| **Mappa** | 🗺️ | Dati geografici | Distribuzione geografica |

---

## 🎨 Paletta Colori Pastel

La dashboard utilizza colori pastel armoniosi:

```
Azzurro Menta      #A8E6CF
Pesca Morbida      #FFD3B6
Rosa Delicata      #FFAAA5
Rosso Blando       #FF8B94
Verde Menta        #B5EAD7
Viola Morbido      #C7CEEA
Verde Pistacchio   #E2F0CB
Pesca Chiara       #FFDAC1
Azzurro Cielo      #B0E0E6
Rosa Pallida       #F7C6C6
Turchese Leggero   #C9E4DE
Magenta Leggero    #FDD0F2
Azzurro Pastello   #D4F1F9
Giallo Pastello    #FFE5B4
Azzurro Cielo II   #D0F0FD
Viola Leggero      #E8D0F0
```

---

## 🎯 Flusso di Generazione Dashboard

```
1. CARICAMENTO DATI
   ├─ Lettura file (CSV, Excel, JSON)
   ├─ Pulizia e validazione
   └─ Identificazione tipi di colonne

2. ANALISI INTELLIGENTE
   ├─ Rilevamento dati temporali
   ├─ Identificazione metriche numeriche
   ├─ Estrazione categorie
   └─ Rilevamento dati geografici

3. GENERAZIONE COMPONENTI
   ├─ KPI Dinamici (0-∞)
   ├─ Filtri Intelligenti (max 2)
   ├─ Selezione Grafici (max 8)
   └─ Rilevamento Mappa

4. RANDOMIZZAZIONE LAYOUT
   ├─ Scelta tipo layout
   ├─ Randomizzazione ordine grafici
   ├─ Assegnazione colori
   └─ Ottimizzazione responsive

5. RENDERING FINALE
   ├─ Generazione HTML
   ├─ Incorporamento Plotly.js
   ├─ Styling Pastel
   └─ Export dashboard.html
```

---

## 💡 Esempi di Utilizzo

### Dataset Vendite
**Layout**: Featured
**KPI**: 
- Totale Record: 1,250
- Media Vendite: €5,420
- Top Cliente: Acme Corp
- Intervallo: 01/01/2024 - 31/12/2024
- Completezza: 98.5%

**Filtri**: Regione, Data
**Grafici**: Linea (Trend), Barre (Top Prodotti), Scatter (Prezzo vs Quantità), Heatmap (Correlazioni)

### Dataset Geografico (Turismo)
**Layout**: Featured + Mappa
**KPI**: Record, Media Ospiti, Top Destinazione, Intervallo, Completezza
**Filtri**: Città, Range Prezzi
**Grafici**: Mappa interattiva, Barre, Pie (Composizione)

### Dataset Scientifi (Ricerca)
**Layout**: Grid 3 Colonne
**KPI**: 6+ Metriche
**Filtri**: Metodologia, Range Valori
**Grafici**: Radar, Scatter, Heatmap, Box Plot, Violin

---

## ✨ Vantaggi del Sistema

✅ **Adattabilità**: Funziona con qualsiasi dataset
✅ **Autonomia**: Selezione automatica di componenti rilevanti
✅ **Variabilità**: Layout e ordine grafici sempre diversi
✅ **Estetica**: Colori armoniosi e design pulito
✅ **Performance**: Caricamento veloce e interattività fluida
✅ **User-Friendly**: Intuitivo e facile da navigare
✅ **Responsive**: Funziona su desktop, tablet, mobile

---

## 🛠️ Tecnologie Utilizzate

- **Backend**: Python, Streamlit
- **Visualizzazione**: Plotly, Plotly.js
- **Dati**: Pandas, NumPy
- **Styling**: CSS3, Pastel Colors

---

## 📝 Versione

v2.0 - Sistema Intelligente di Generazione Dashboard (Maggio 2026)

---

*Dashboard Generator - Powered by AI Data Engineering*
