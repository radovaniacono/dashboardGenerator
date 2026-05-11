# 🚀 Quick Start Guide - Dashboard Generator v3.0

## ⚡ 5 Minuti per Iniziare

### Step 1: Installazione (1 min)
```bash
cd /Users/radovaniacono/Documents/dashboardinterattive/dashboardGenerator

# Installa dipendenze
pip install -r requirements.txt

# Oppure manualmente:
pip install streamlit pandas numpy plotly scikit-learn openpyxl
```

### Step 2: Avvia l'App (30 sec)
```bash
streamlit run app.py
```

### Step 3: Carica un File CSV (30 sec)
Esempio minimo di CSV `vendite.csv`:
```csv
data,prodotto,quantita,prezzo,categoria
2024-01-01,A,10,99.99,Categoria1
2024-01-02,B,5,149.99,Categoria2
2024-01-03,A,15,99.99,Categoria1
2024-01-04,C,8,199.99,Categoria3
```

### Step 4: Seleziona Opzioni (1 min)
```
☑️ Analisi ML              (insights automatici)
☑️ KPI                     (metriche critiche)
☑️ Dashboard              (grafici interattivi)
☑️ Tabelle                (dati dettagliati)
```

### Step 5: Scarica Risultati (1 min)
```
📄 Dashboard.html         (standalone interattivo)
📊 data.csv              (per Tableau/Power BI)
🔗 data.json             (per API)
```

---

## 📊 Cosa Vedrai

### 1️⃣ Analisi ML
```
📊 Shape: 1000 × 15
🛡️ Completezza: 95.2%
🔢 Metriche: 8 colonne numeriche
⚠️ Problemi: Nessuno rilevato
📈 Correlazioni: 2 correlazioni forti trovate
🏷️ Tipi: Monetarie (2), Percentuali (1), Temporali (1)
```

### 2️⃣ KPI Intelligenti
```
💰 Ricavo Totale: € 45,230
   ↑ Media: €453

📊 Quantità: 100 unità
   Media: 10

🏆 Top: Categoria A
   88% del totale

📈 Trend: +12.5% vs media
✅ Qualità: 95.2% completo
📅 Periodo: 365 giorni
```

### 3️⃣ Grafici Intelligenti
```
📈 Line chart       → Vendite nel tempo
📊 Bar chart        → Per categoria
🔍 Scatter plot     → Prezzo vs quantità
🔗 Heatmap          → Correlazioni
📦 Boxplot          → Outlier
🗂️ Treemap          → Composizione
🥧 Pie              → Proporzioni
🎻 Violin           → Distribuzioni
```

### 4️⃣ Tabelle
```
Tab 1: Summary
  - 10 righe + statistiche

Tab 2: Dettagli Completi
  - Tutti i dati con sorting

Tab 3: Profilo
  - Cardinalità e missing data
```

---

## 🔧 Comandi Utili

### Ricaricare l'app
```bash
streamlit run app.py --logger.level=debug
```

### Cancellare cache
```bash
streamlit cache clear
```

### Opzioni avanzate
```bash
streamlit run app.py --theme.base "dark"
streamlit run app.py --client.toolbarMode "minimal"
```

---

## 📁 Struttura File

```
dashboardGenerator/
├── app.py                           ← Main application
├── requirements.txt                 ← Dependencies
├── src/
│   ├── ml_analyzer.py              ← ML analysis engine
│   ├── dashboard_generator.py       ← Chart & KPI generation
│   └── pdf_generator.py            ← PDF export (future)
├── README_v3.md                    ← Documentazione
├── FEATURES.md                     ← Miglioramenti
└── QUICK_START.md                  ← Questo file!
```

---

## 💾 Dataset Beispiele

### Minimo Richiesto
```csv
metriche
100
200
150
```
✅ Genera histogram + KPI

### Consigliato
```csv
data,categoria,valore,quantita,percentuale
2024-01-01,A,1000,10,80.5
2024-01-02,B,1500,15,85.3
```
✅ Genera tutti i grafici

### Ottimale (3+ colonne numeriche + temporali + categorie)
```csv
data,categoria,regione,ricavo,costo,margine,volume
2024-01-01,A,Nord,5000,3000,40%,100
2024-01-02,B,Sud,6000,3500,42%,120
```
✅ Clustering, correlazioni, trend line

---

## ❓ Domande Comuni

### Q: Qual è la dimensione massima file?
**R**: 500MB consigliato (CSV). Per file più grandi usa Excel.

### Q: Quali formati supporta?
**R**: CSV, XLSX, XLS, JSON

### Q: Come filtro i dati?
**R**: Usa le opzioni nel sidebar:
- 🏷️ Filtro categoria (multi-select)
- 📊 Range slider (numerici)
- 🔄 Reset per pulire

### Q: Posso personalizzare colori?
**R**: Edita `self.pastel_colors` in `dashboard_generator.py`

### Q: Come aggiungo un nuovo grafico?
**R**: 
1. Implementa `create_xxx_chart()` in `DashboardGenerator`
2. Aggiungi a dictionary `chart_functions`
3. Aggiorna logica in `select_charts_advanced()`

---

## 🐛 Troubleshooting Veloce

| Problema | Soluzione |
|----------|----------|
| "Port 8501 in use" | `streamlit run app.py --server.port 8502` |
| File non carica | Controlla encoding CSV (UTF-8 preferibile) |
| Grafici vuoti | Verificare che colonne sono numeriche |
| Memoria piena | Filtra dataset prima (< 100K righe) |
| Dashboard lento | Disabilita insights ML se troppo lento |

---

## 🎓 Workflow Tipico

### Scenario: Analizzare Vendite Mensili

```
1. Carica "vendite_marzo.csv"
   └─ Attendi analisi ML (2-3 sec)

2. Abilita tutte le opzioni
   └─ Vedi sezione insights

3. Applica filtri se necessario
   └─ "Categoria = Elettronica"
   └─ "Prezzo = 100-500"

4. Scrolla per vedere:
   ✅ KPI aggiornati
   ✅ Tabella dati filtrata
   ✅ 8 grafici intelligenti

5. Scarica per presentazione
   └─ Dashboard.html (per client)
   └─ data.csv (per Tableau)
```

---

## 📚 Per Saperne di Più

Consulta:
- **README_v3.md** → Documentazione completa
- **FEATURES.md** → Cosa è migliorato
- Docstring nel codice sorgente

---

## ✨ Tips & Tricks

### Tip 1: Dataset Pulito = Risultati Migliori
```
✅ Non mettere righe di intestazione extra
✅ Converti date in formato ISO (YYYY-MM-DD)
✅ Assicura nomi colonne coerenti (snake_case)
```

### Tip 2: Interpreta gli Insights
```
🟢 Correlazione > 0.7  → Dipendenza forte
🟡 Correlazione 0.5-0.7 → Relazione moderata
🔴 Missing > 50%       → Colonna problematica
```

### Tip 3: Esporta Intelligentemente
```
📄 HTML   → Per presentare ai client
📊 CSV    → Per import Tableau
🔗 JSON   → Per API e pipelines
```

---

## 🎉 Pronto!

Hai tutto quello che serve. **Carica il tuo primo file e scopri cosa rivela l'IA sui tuoi dati!**

**Domande?** Controlla la sezione Troubleshooting o leggi FEATURES.md

---

**Happy Analyzing! 🤖📊**
