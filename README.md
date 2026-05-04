# 🤖 AI Data Engineer - Smart Dashboard Generator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What is this?

Una piattaforma che utilizza **Machine Learning** per analizzare automaticamente qualsiasi file dati e generare:

- ✅ **Dashboard interattive** con visualizzazioni dinamiche
- ✅ **PDF professionale** con passaggi dettagliati per ricreare tutto in Tableau
- ✅ **Insights automatici** usando Random Forest, Clustering, e analisi outlier

## 🚀 Features

### 🔍 Machine Learning Intelligence
- **Auto Detection**: Riconoscimento automatico del tipo di dato
- **Key Drivers**: Random Forest per identificare variabili più influenti  
- **Clustering**: KMeans per segmentazione automatica
- **Outlier Detection**: Isolation Forest per anomalie
- **Trend Analysis**: Rilevazione pattern temporali

### 📊 Dashboard Dinamica
- Generazione automatica basata sui dati
- Grafici interattivi con Plotly
- KPI e metriche intelligenti
- Heatmap correlazioni
- Visualizzazione cluster

### 📝 Guida Tableau
- Passaggi dettagliati per Tableau Prep
- Layout dashboard consigliato
- Campi calcolati suggeriti
- Checklist di validazione

## 📦 Installation

### Local Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-data-engineer-dashboard.git
cd ai-data-engineer-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
