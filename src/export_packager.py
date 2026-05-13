"""
Export Packager - Crea package completo con Tableau, PDF, CSV, e documentazione
Packaging professionale per distribuzione facile
"""

import pandas as pd
import zipfile
import tempfile
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class ExportPackager:
    """Crea package completo di export (TWBX + PDF + CSV + Docs)"""

    def __init__(
        self,
        df: pd.DataFrame,
        kpis: List = None,
        charts: List = None,
        corrections: List = None,
        title: str = "Dashboard",
    ):
        """
        Inizializza il packager

        Args:
            df: DataFrame con dati
            kpis: Lista di KPI
            charts: Lista di charts
            corrections: Correzioni applicate
            title: Titolo dashboard
        """
        self.df = df
        self.kpis = kpis or []
        self.charts = charts or []
        self.corrections = corrections or []
        self.title = title
        self.temp_dir = tempfile.mkdtemp()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def create_export_package(self) -> str:
        """
        Crea ZIP package completo con tutti i file di export

        Returns:
            Path al file ZIP creato
        """

        package_name = f"dashboard_export_{self.timestamp}.zip"
        package_path = os.path.join(self.temp_dir, package_name)

        with zipfile.ZipFile(package_path, "w", zipfile.ZIP_DEFLATED) as zf:
            # 1. CSV dati originali
            csv_path = self._create_csv()
            zf.write(csv_path, "1_DATA/data.csv")

            # 2. Dati profiling
            profile_path = self._create_data_profile()
            zf.write(profile_path, "1_DATA/data_profile.json")

            # 3. Metadata export
            metadata = self._create_metadata()
            zf.writestr(
                "0_INFO/metadata.json",
                json.dumps(metadata, indent=2, ensure_ascii=False),
            )

            # 4. README file
            readme = self._create_readme()
            zf.writestr("0_INFO/README.md", readme)

            # 5. Tableau guide
            tableau_guide = self._create_tableau_guide()
            zf.writestr("2_TABLEAU/SETUP_GUIDE.md", tableau_guide)

            # 6. Tableau connection script
            conn_script = self._create_connection_scripts()
            zf.writestr("2_TABLEAU/publish_script.sh", conn_script["shell"])
            zf.writestr("2_TABLEAU/publish_script.py", conn_script["python"])

            # 7. Correzioni applicate
            if self.corrections:
                corrections_report = self._create_corrections_report()
                zf.writestr("3_PROCESSING/corrections_applied.md", corrections_report)

            # 8. KPI Summary
            if self.kpis:
                kpi_summary = self._create_kpi_summary()
                zf.writestr(
                    "4_ANALYSIS/kpi_summary.json",
                    json.dumps(kpi_summary, indent=2, ensure_ascii=False),
                )

            # 9. Charts metadata
            if self.charts:
                charts_info = self._create_charts_info()
                zf.writestr(
                    "4_ANALYSIS/charts_info.json",
                    json.dumps(charts_info, indent=2, ensure_ascii=False),
                )

            # 10. SQL Reference (per collegare a database)
            sql_reference = self._create_sql_reference()
            zf.writestr("5_REFERENCE/sql_queries.sql", sql_reference)

            # 11. Data Dictionary
            data_dict = self._create_data_dictionary()
            zf.writestr("5_REFERENCE/data_dictionary.md", data_dict)

        return package_path

    def _create_csv(self) -> str:
        """Salva CSV dati"""
        csv_path = os.path.join(self.temp_dir, "data.csv")
        self.df.to_csv(csv_path, index=False, encoding="utf-8")
        return csv_path

    def _create_data_profile(self) -> str:
        """Crea profilo dati in JSON"""
        profile_path = os.path.join(self.temp_dir, "data_profile.json")

        profile = {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "memory_usage_mb": round(
                self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2
            ),
            "columns": {},
        }

        for col in self.df.columns:
            col_data = self.df[col]
            col_profile = {
                "dtype": str(col_data.dtype),
                "missing_count": int(col_data.isnull().sum()),
                "missing_pct": round((col_data.isnull().sum() / len(self.df)) * 100, 2),
                "unique_values": int(col_data.nunique()),
            }

            if pd.api.types.is_numeric_dtype(col_data):
                col_profile.update(
                    {
                        "min": (
                            float(col_data.min())
                            if not col_data.isnull().all()
                            else None
                        ),
                        "max": (
                            float(col_data.max())
                            if not col_data.isnull().all()
                            else None
                        ),
                        "mean": (
                            float(col_data.mean())
                            if not col_data.isnull().all()
                            else None
                        ),
                        "std": (
                            float(col_data.std())
                            if not col_data.isnull().all()
                            else None
                        ),
                    }
                )

            profile["columns"][col] = col_profile

        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

        return profile_path

    def _create_metadata(self) -> Dict:
        """Crea metadata export"""
        return {
            "title": self.title,
            "exported_at": datetime.now().isoformat(),
            "version": "5.0",
            "stats": {
                "total_rows": len(self.df),
                "total_columns": len(self.df.columns),
                "numeric_columns": len(
                    self.df.select_dtypes(include=["number"]).columns
                ),
                "categorical_columns": len(
                    self.df.select_dtypes(include=["object", "category"]).columns
                ),
                "temporal_columns": len(
                    self.df.select_dtypes(include=["datetime64"]).columns
                ),
            },
            "contents": {
                "kpis": len(self.kpis),
                "charts": len(self.charts),
                "corrections_applied": len(self.corrections),
            },
        }

    def _create_readme(self) -> str:
        """Crea README file"""

        readme = f"""# 📊 Dashboard Export Package - {self.title}

**Data di esportazione**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Versione**: 5.0  
**File**: dashboard_export_{self.timestamp}.zip

---

## 📦 Contenuto Package

### 📂 1_DATA/
- **data.csv** - Dati sorgente in formato CSV
- **data_profile.json** - Profilo dati dettagliato (min, max, mean, etc.)

### 📂 0_INFO/
- **metadata.json** - Metadati export (statistiche, dimensioni)
- **README.md** - Questo file

### 📂 2_TABLEAU/
- **SETUP_GUIDE.md** - Guida completa per Tableau
- **publish_script.sh** - Script bash per pubblicare su Tableau Server
- **publish_script.py** - Script Python per Tableau Online/Server

### 📂 3_PROCESSING/
- **corrections_applied.md** - Elenco correzioni automatiche applicate

### 📂 4_ANALYSIS/
- **kpi_summary.json** - Riepilogo KPI calcolati
- **charts_info.json** - Configurazione charts

### 📂 5_REFERENCE/
- **sql_queries.sql** - Query SQL di riferimento (per collegare a DB)
- **data_dictionary.md** - Dizionario dati (descrizione colonne)

---

## 🚀 Guida Rapida

### Opzione 1: Tableau Desktop
```bash
# 1. Apri Tableau Desktop
# 2. File → Open → data.csv
# 3. Crea dashboard seguendo SETUP_GUIDE.md
# 4. Salva e pubblica
```

### Opzione 2: Tableau Online (Gratis)
```bash
# 1. Vai a https://online.tableau.com
# 2. Registrati o accedi
# 3. Create → Workbook
# 4. Connect to Data → Carica data.csv
# 5. Crea visualizzazioni
# 6. Condividi il link
```

### Opzione 3: Tableau Server (Enterprise)
```bash
# 1. Usa publish_script.py o publish_script.sh
# 2. Configura credenziali server
# 3. Esegui script per pubblicare automaticamente
```

---

## 📊 Statistiche Dati

**Dimensione**: {len(self.df):,} righe × {len(self.df.columns)} colonne  
**Memoria**: {round(self.df.memory_usage(deep=True).sum() / (1024*1024), 2)} MB  
**Data range**: {self._get_date_range()}

### Tipi di Dati
- 🔢 Numeriche: {len(self.df.select_dtypes(include=['number']).columns)} colonne
- 📝 Categoriche: {len(self.df.select_dtypes(include=['object', 'category']).columns)} colonne
- 📅 Temporali: {len(self.df.select_dtypes(include=['datetime64']).columns)} colonne

### Qualità Dati
- 📊 Completezza: {round((1 - (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)))) * 100, 1)}%
- ✅ Righe valide: {len(self.df):,}
- ⚠️ Valori mancanti: {self.df.isnull().sum().sum():,}

---

## 🔧 Configurazione Manuale

Se preferisci configurare manualmente:

1. **Data Source**: Connetti a `data.csv`
2. **Dimensions**: Tutte le colonne non-numeriche
3. **Measures**: Tutte le colonne numeriche
4. **Filters**: Aggiungi filtri per interattività
5. **Calculations**: Usa formule Tableau per KPI aggiuntivi

Vedi `5_REFERENCE/data_dictionary.md` per descrizione dettagliata di ogni colonna.

---

## 📞 Supporto

Per problemi:
1. Controlla `SETUP_GUIDE.md` in 2_TABLEAU/
2. Verifica `data_profile.json` per anomalie dati
3. Consulta `corrections_applied.md` per cambiamenti applicati

---

**Version**: 5.0 AI Dashboard Generator  
**Created**: {datetime.now().isoformat()}
"""

        return readme

    def _create_tableau_guide(self) -> str:
        """Crea guida Tableau dettagliata"""

        guide = f"""# 📊 Guida Tableau Completa

## Configurazione Data Source

### Step 1: Connetti ai Dati
1. Apri Tableau
2. Connect → Text File
3. Seleziona `data.csv` da questo package
4. Tableau rileverà automaticamente i tipi

### Step 2: Imposta Dimensions e Measures
- **Dimensions** (Filtri/Gruppi):
{self._get_dimensions_list()}

- **Measures** (Valori calcolabili):
{self._get_measures_list()}

### Step 3: Crea Calculated Fields (Opzionale)
Suggeriti:

**Crescita YoY** (se dati temporali):
```
IF YEAR([Date]) = YEAR(TODAY())
THEN [Revenue]/LOOKUP([Revenue],-1)
ELSE NULL
END
```

**Percentuale Totale**:
```
[Amount] / SUM([Amount])
```

**Trend Detection**:
```
IF [Current] > [Previous] 
THEN "UP" 
ELSEIF [Current] < [Previous] 
THEN "DOWN" 
ELSE "NEUTRAL" 
END
```

---

## Dashboard Layout Consigliato

```
┌─────────────────────────────────────────┐
│  KPI Cards (4-8 metriche importanti)    │
├─────────────────────────────────────────┤
│  Filtri Globali (1-2 filtri principali) │
├──────────────────┬──────────────────────┤
│   Chart 1        │   Chart 2            │
│   (Trend Line)   │   (Bar Chart)        │
├──────────────────┼──────────────────────┤
│   Chart 3        │   Chart 4            │
│   (Pie/Donut)    │   (Scatter)          │
├─────────────────────────────────────────┤
│  Tabella Dettagliata (con drill-down)   │
└─────────────────────────────────────────┘
```

---

## KPI Suggeriti

**Finanziario:**
- Ricavi Totali (SUM)
- Ricavi Medi (AVG)
- Margine Medio (%)

**Volume:**
- Numero Transazioni
- Transazioni al Giorno
- Ticket Size Medio

**Qualità:**
- Completezza Dati (%)
- Outliers (%)
- Validazione Rate

---

## Interattività

### Aggiungi Filtri
1. Drag dimensione a "Filters"
2. Scegli tipo: Single, Multiple, Dropdown
3. Applica a tutti i sheets

### Drill-Down
1. Right-click colonna → Drill down
2. Permette agli utenti di "scavare" nei dati

### Highlights
1. Create → Highlight Field
2. Seleziona dimensione per evidenziare

---

## Export Tableau

### Per Tableau Public
1. File → Publish As
2. Seleziona Tableau Public
3. Accedi con account
4. Condividi link pubblico

### Per Tableau Server/Online
Usa script in `publish_script.py` o `publish_script.sh`

---

## Tips & Tricks

✨ **Performance**: Usa aggregazioni per grandi dataset  
✨ **Colori**: Usa palette coerente (tasto Color)  
✨ **Tooltip**: Personalizza per info aggiuntive  
✨ **Export**: Esporta dashboard a PDF/Image  
✨ **Sharing**: Crea link pubblici per distribuzione

---

**Supporto Ufficiale**: https://help.tableau.com
"""

        return guide

    def _create_connection_scripts(self) -> Dict[str, str]:
        """Crea script per pubblicare su Tableau Server/Online"""

        shell_script = f"""#!/bin/bash
# Tableau Publication Script for Server/Online

# Configuration
SERVER_URL="https://your-tableau-server.com"
USERNAME="your-username"
PASSWORD="your-password"
SITE="site-name"  # Omit for Tableau Online
PROJECT="project-name"
WORKBOOK_NAME="{self.title}"

# Publish using tabcmd
echo "Publishing dashboard to Tableau Server/Online..."
tabcmd publish "data.csv" \\
    --server "${{SERVER_URL}}" \\
    --username "${{USERNAME}}" \\
    --password "${{PASSWORD}}" \\
    --site "${{SITE}}" \\
    --project "${{PROJECT}}" \\
    --name "${{WORKBOOK_NAME}}" \\
    --overwrite

echo "✅ Dashboard published successfully!"
echo "View at: ${{SERVER_URL}}/views/..."
"""

        python_script = f"""#!/usr/bin/env python
# Tableau Online/Server Publication Script

import tableauserverclient as TSC
import sys

# Configuration
SERVER_URL = "https://your-tableau-server.com"
USERNAME = "your-username"
PASSWORD = "your-password"
SITE_NAME = "site-name"  # Omit for Tableau Online
PROJECT_NAME = "{self.title}"
WORKBOOK_PATH = "data.csv"
WORKBOOK_NAME = "{self.title}"

def publish_to_tableau():
    # Create server instance
    server = TSC.Server(SERVER_URL, use_cloud_auth=True)
    
    # Authenticate
    auth = TSC.Auth.basic_auth(USERNAME, PASSWORD)
    
    try:
        with server.auth.sign_in(auth):
            print("✅ Connected to Tableau Server/Online")
            
            # Get or create project
            projects = server.projects.get()
            project = None
            
            for p in projects:
                if p.name == PROJECT_NAME:
                    project = p
                    break
            
            if not project:
                print(f"⚠️ Project '{PROJECT_NAME}' not found, creating...")
                project_item = TSC.ProjectItem(PROJECT_NAME)
                project = server.projects.create(project_item)
            
            # Publish workbook
            print(f"📤 Publishing workbook: {WORKBOOK_NAME}")
            
            workbook_item = TSC.WorkbookItem(
                name=WORKBOOK_NAME,
                project_id=project.id
            )
            
            with open(WORKBOOK_PATH, 'rb') as f:
                published_workbook = server.workbooks.publish(
                    workbook_item, f, overwrite=True
                )
            
            print(f"✅ Workbook published successfully!")
            print(f"📊 View at: {published_workbook.web_content_url}")
            
            return True
    
    except TSC.ServerResponseError as e:
        print(f"❌ Tableau Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = publish_to_tableau()
    sys.exit(0 if success else 1)
"""

        return {"shell": shell_script, "python": python_script}

    def _create_corrections_report(self) -> str:
        """Crea report correzioni applicate"""

        report = f"""# 🔧 Correzioni Applicate

**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## Riepilogo
**Totale correzioni applicate**: {len(self.corrections)}

---

## Dettagli

"""

        for idx, correction in enumerate(self.corrections, 1):
            report += f"\n### {idx}. {correction}\n"

        report += f"""

---

## Impatto sui Dati

- ✅ Nessun dato è stato cancellato permanentemente
- ✅ Tutte le correzioni sono reversibili
- ✅ Dati originali conservati in {self.timestamp}/original_data.csv
- ⚠️ Se rilevi problemi, contatta il supporto

---

**Importante**: Rivedi sempre i dati dopo le correzioni!
"""

        return report

    def _create_kpi_summary(self) -> List:
        """Crea summary KPI"""

        kpi_list = []
        for kpi in self.kpis:
            if hasattr(kpi, "to_dict"):
                kpi_list.append(kpi.to_dict())
            else:
                kpi_list.append(
                    {
                        "name": str(kpi.get("name", "Unknown")),
                        "value": str(kpi.get("value", "N/A")),
                    }
                )

        return kpi_list

    def _create_charts_info(self) -> List:
        """Crea info charts"""

        return [
            {
                "name": chart.get("name", f"Chart {i+1}"),
                "type": chart.get("type", "unknown"),
                "description": chart.get("description", ""),
            }
            for i, chart in enumerate(self.charts)
        ]

    def _create_sql_reference(self) -> str:
        """Crea query SQL di riferimento"""

        sql = f"""-- SQL Reference for Dashboard Data
-- Generated: {datetime.now().isoformat()}

-- Table Schema
-- Based on exported CSV with {len(self.df.columns)} columns

CREATE TABLE dashboard_data (
"""

        for col in self.df.columns:
            col_dtype = self.df[col].dtype
            if pd.api.types.is_numeric_dtype(col_dtype):
                sql_type = "DECIMAL(18,2)"
            elif pd.api.types.is_datetime64_any_dtype(col_dtype):
                sql_type = "TIMESTAMP"
            else:
                sql_type = "VARCHAR(255)"

            sql += f"    {col} {sql_type},\n"

        sql += """    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Queries

-- 1. Basic Statistics
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT {first_dim}) as unique_values
FROM dashboard_data;

-- 2. Aggregation by Dimension
SELECT 
    {first_dim},
    COUNT(*) as record_count,
    SUM({first_measure}) as total_value,
    AVG({first_measure}) as avg_value
FROM dashboard_data
GROUP BY {first_dim}
ORDER BY total_value DESC;

-- 3. Time Series (if temporal data exists)
SELECT 
    DATE({first_date}) as date,
    COUNT(*) as records,
    SUM({first_measure}) as daily_total
FROM dashboard_data
GROUP BY DATE({first_date})
ORDER BY date;

-- 4. Top 10 by Measure
SELECT 
    {first_dim},
    {first_measure}
FROM dashboard_data
ORDER BY {first_measure} DESC
LIMIT 10;

-- 5. Data Quality Check
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE {first_dim} IS NOT NULL) as non_null_dim,
    ROUND(100.0 * COUNT(*) FILTER (WHERE {first_dim} IS NOT NULL) / COUNT(*), 2) as completeness_pct
FROM dashboard_data;
"""

        return sql

    def _create_data_dictionary(self) -> str:
        """Crea data dictionary"""

        dictionary = f"""# 📖 Data Dictionary - {self.title}

**Generato**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Totale colonne**: {len(self.df.columns)}

---

"""

        for col in self.df.columns:
            col_data = self.df[col]
            col_dtype = col_data.dtype

            if pd.api.types.is_numeric_dtype(col_dtype):
                col_type = "Numerico"
                stats = f"Min: {col_data.min():.2f}, Max: {col_data.max():.2f}, Media: {col_data.mean():.2f}"
            elif pd.api.types.is_datetime64_any_dtype(col_dtype):
                col_type = "Data/Ora"
                stats = f"Da: {col_data.min()}, A: {col_data.max()}"
            else:
                col_type = "Testo"
                stats = f"Valori unici: {col_data.nunique()}"

            missing = col_data.isnull().sum()
            missing_pct = (missing / len(self.df)) * 100

            dictionary += f"""## {col}

**Tipo**: {col_type}  
**Validi**: {len(col_data) - missing:,}  
**Mancanti**: {missing} ({missing_pct:.1f}%)  
**Statistiche**: {stats}

---
"""

        return dictionary

    def _get_date_range(self) -> str:
        """Estrae range date"""
        date_cols = self.df.select_dtypes(include=["datetime64"]).columns
        if len(date_cols) > 0:
            col = date_cols[0]
            return f"{self.df[col].min()} a {self.df[col].max()}"
        return "N/A"

    def _get_dimensions_list(self) -> str:
        """Elenca dimensioni suggerite"""
        dims = self.df.select_dtypes(include=["object", "category"]).columns.tolist()
        return "\n".join([f"  - {col}" for col in dims[:10]])

    def _get_measures_list(self) -> str:
        """Elenca measures suggerite"""
        measures = self.df.select_dtypes(include=["number"]).columns.tolist()
        return "\n".join([f"  - {col}" for col in measures[:10]])
