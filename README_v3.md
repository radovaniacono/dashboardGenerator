# 🤖 AI Data Engineer Dashboard Generator v3.0

**Sistema intelligente di generazione dashboard con analisi ML avanzata**

## ✨ Caratteristiche Principali

### 1. **Rilevamento Automatico dei Dati**
- ✅ Identificazione automatica di tipi di dati (monetari, percentuali, temporali, geografici)
- ✅ Rileva colonne booleane nascoste
- ✅ Analisi della cardinalità e qualità dei dati
- ✅ Rilevamento di anomalie e duplicati

### 2. **KPI Dinamici Intelligenti**
- 💰 **KPI Monetari**: Totali, medie, trend con frecce direzionali
- 📊 **KPI di Volume**: Conteggi, totali con metriche comparative
- 📈 **KPI Percentuali**: Tassi e percentuali con max/min
- 📅 **KPI Temporali**: Range di date, durata in giorni
- ✅ **Qualità Dati**: Percentuale di completezza con status

### 3. **Selezione Grafici Intelligente**
L'algoritmo analizz automaticamente:
- Numero e tipo di colonne numeriche
- Distribuzione delle cardinalità
- Correlazioni forti tra variabili
- Presenza di dati temporali
- Outlier e anomalie

**Grafici supportati**:
- 📈 **Line**: Serie temporali
- 📊 **Bar**: Categorie
- 🔍 **Scatter**: Correlazioni
- 🫧 **Bubble**: 3 dimensioni
- 🔗 **Heatmap**: Correlazioni matrice
- 📦 **Boxplot**: Outlier detection
- 📊 **Histogram**: Distribuzioni
- 🗂️ **Treemap**: Composizioni
- 🔄 **Radar**: Metriche comparative
- 🎻 **Violin**: Densità distribuzioni
- 📊 **Area**: Volume cumulative
- 🥧 **Pie**: Proporzioni

### 4. **Analisi ML Avanzata**
- 🤖 **Correlazioni**: Identifica relazioni forti (r > 0.7)
- 🎯 **Clustering**: Scopre segmenti naturali nei dati
- 🔍 **Anomalie**: Rileva outlier con Isolation Forest
- 🌳 **Feature Importance**: Trova driver principali (Random Forest)
- 📊 **Qualità Dati**: Valuta completezza e problemi

### 5. **Filtri Interattivi**
- 🏷️ **Filtri Categoria**: Multi-select su colonne categoriche
- 📊 **Range Numerici**: Slider per metriche numeriche
- 🔄 **Reset Filtri**: Pulsante per ripristinare tutto
- 📊 **Aggiornamento Real-time**: KPI e grafici si aggiornano

### 6. **Tabelle Intelligenti**
- **Summary**: Anteprima dati + statistiche descrittive
- **Dettagli Completi**: Explorer con sorting e paginazione
- **Profilo Dati**: Cardinalità, valori mancanti, tipi di dati

### 7. **Export Multipli**
- 📄 **HTML**: Dashboard interattiva standalone
- 📊 **CSV**: Dati filtrati (per Tableau)
- 🔗 **JSON**: Formato strutturato per API

## 🚀 Come Usare

### Installazione

```bash
# 1. Clone il repository
git clone <repository-url>
cd dashboardGenerator

# 2. Installa le dipendenze
pip install -r requirements.txt

# 3. Avvia l'applicazione
streamlit run app.py
```

### Workflow

1. **Carica un file** (CSV, Excel, JSON)
2. **Attendi analisi ML** (automatica e veloce)
3. **Abilita le opzioni** che desideri:
   - 📊 Analisi ML
   - 💰 KPI
   - 📈 Dashboard
   - 📋 Tabelle
4. **Applica filtri** se necessario
5. **Scarica i risultati** in formato desiderato

## 📊 Esempio Dataset

### Vendite
```
data_vendita,prodotto,quantita,prezzo,categoria,regione
2024-01-01,Prodotto A,10,99.99,Categoria 1,Nord
2024-01-02,Prodotto B,5,149.99,Categoria 2,Sud
...
```

**Output atteso**:
- 💰 KPI: Ricavo totale, average order value, top categoria
- 📈 Grafici: Vendite nel tempo, per categoria, per regione
- 📊 Insights: Correlazioni prezzo-quantità, segmenti clienti

## 🔬 Algoritmi e Metodologie

### Rilevamento Tipi Dati
- Basato su keyword matching (price, cost, revenue, ecc.)
- Analisi dei range (0-100 per percentuali)
- Cardinalità per categorie

### Selezione Grafici
- **Histogram**: Sempre (base per distribuzione)
- **Bar**: Se categorie con cardinalità bassa
- **Line**: Se dati temporali presenti
- **Scatter**: Se 2+ metriche numeriche
- **Heatmap**: Se correlazioni forti o 3+ metriche
- **Boxplot**: Se outlier rilevati
- **Treemap**: Se composizioni categoria-valore
- **Bubble**: Se 3+ metriche con alta variabilità

### Calcolo KPI
- **Monetari**: Somma e media con trend direzionale
- **Count**: Totale con media comparativa
- **Percentuali**: Media e max
- **Temporali**: Range in giorni
- **Qualità**: Percentuale non-null

## 📈 Interpretazione Insights

### Qualità Dati
- 🟢 **≥90%**: Buona - procedere con fiducia
- 🟡 **70-90%**: Soddisfacente - controllare colonne critiche
- 🔴 **<70%**: Problematica - pulire prima di analizzare

### Correlazioni
- **r > 0.7**: Forte relazione lineare
- **r 0.5-0.7**: Correlazione moderata
- **r < 0.5**: Correlazione debole

### Outlier
- Identificati con Isolation Forest
- Visibili in boxplot e violin plot
- Verificare se sono errori o dati legittimi

## 🛠️ Personalizzazione

### Modificare tema colori
Edita `self.pastel_colors` in `dashboard_generator.py`:
```python
self.pastel_colors = [
    "#A8E6CF",  # Verde salvia
    "#FFD3B6",  # Arancione
    ...
]
```

### Aggiungere nuovi grafici
1. Implementa metodo `create_xxx_chart()` in `DashboardGenerator`
2. Aggiungi a `chart_functions` dictionary
3. Aggiorna logica selezione in `select_charts_advanced()`

### Modificare KPI
Personalizza `generate_dynamic_kpis()` in `DashboardGenerator`

## 📚 Requisiti

```
pandas>=1.3.0
numpy>=1.20.0
streamlit>=1.0.0
plotly>=5.0.0
scikit-learn>=1.0.0
openpyxl>=3.0.0
```

## 🐛 Troubleshooting

### "Arrow serialization error"
**Soluzione**: Aggiorna `clean_dataframe()` per convertire colonne problematiche

### "Dashboard non si carica"
**Soluzione**: Verificare che il file HTML è valido (controlla Console browser)

### "Memoria insufficiente"
**Soluzione**: 
- Filtra il dataset prima di uploadare
- Usa CSV invece di Excel per dataset grandi
- Aumenta `st.cache_data` timeout

### "Grafici non si visualizzano"
**Soluzione**: 
- Verifica che le colonne hanno dati numerici validi
- Controlla che Plotly JavaScript CDN è raggiungibile

## 🤝 Contribuire

Benvenuti suggerimenti e pull requests!

Aree di miglioramento:
- [ ] Supporto per database diretti
- [ ] Export in Power BI
- [ ] Theme personalizzati
- [ ] Lingua multilingue

## 📄 Licenza

MIT License - Vedi LICENSE file

## 👨‍💻 Autore

**AI Data Engineer Dashboard Generator**
- Versione 3.0
- Ultimo aggiornamento: Maggio 2024

---

**Buon uso! 🚀**
