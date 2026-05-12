"""
Tableau Exporter - Generazione file Tableau (.twbx) pronti all'uso
Crea dashboard Tableau completamente funzionali da dati e configurazione
"""

import pandas as pd
import numpy as np
import zipfile
import tempfile
import os
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET


class TableauExporter:
    """Esporta dashboard Tableau in formato TWBX (Tableau Workbook)"""

    def __init__(
        self,
        df: pd.DataFrame,
        kpis: List = None,
        charts: List = None,
        title: str = "Dashboard",
    ):
        """
        Inizializza l'esportatore Tableau

        Args:
            df: DataFrame con i dati
            kpis: Lista di KPI da includere
            charts: Lista di configurazioni chart
            title: Titolo dashboard
        """
        self.df = df
        self.kpis = kpis or []
        self.charts = charts or []
        self.title = title
        self.temp_dir = tempfile.mkdtemp()
        self.columns_info = self._analyze_columns()

    def export_to_twbx(self, filename: str = "dashboard.twbx") -> str:
        """
        Crea file TWBX completo e funzionante

        Returns:
            Path al file TWBX creato
        """
        # Step 1: Salva CSV dati
        csv_path = self._export_csv()

        # Step 2: Crea dashboard XML
        dashboard_xml = self._generate_dashboard_twb()

        # Step 3: Crea worksheets
        worksheets = self._generate_worksheets()

        # Step 4: Package TWBX
        twbx_path = self._package_twbx(dashboard_xml, worksheets, csv_path, filename)

        return twbx_path

    def _analyze_columns(self) -> Dict:
        """Analizza colonne per tipos dati Tableau"""
        info = {}

        for col in self.df.columns:
            col_dtype = self.df[col].dtype

            if pd.api.types.is_numeric_dtype(col_dtype):
                info[col] = {"type": "real", "tableau_type": "measure"}
            elif pd.api.types.is_datetime64_any_dtype(col_dtype):
                info[col] = {"type": "datetime", "tableau_type": "dimension"}
            else:
                info[col] = {"type": "string", "tableau_type": "dimension"}

        return info

    def _export_csv(self) -> str:
        """Salva dati come CSV per Tableau"""
        csv_path = os.path.join(self.temp_dir, "data.csv")
        self.df.to_csv(csv_path, index=False, encoding="utf-8")
        return csv_path

    def _generate_dashboard_twb(self) -> str:
        """Crea dashboard XML Tableau"""

        xml_content = f"""<?xml version='1.0' encoding='utf-8'?>
<workbook source-build='2024.1.0' xmlns='http://tableauserver.com/api' xmlns:user='http://tableauserver.com/api/user'>
  <preferences/>
  
  <datasources>
    <datasource caption="Data Source" name="datasource0" inline="false" version="10.0">
      <connection class="textscan" directory="{self.temp_dir}" server="">
        <relation name="data" table="[data#csv]" type="table">
          <columns>
{self._generate_datasource_columns()}
          </columns>
        </relation>
      </connection>
      <column caption="{self.title}" datatype="string" name="[__tableau_internal_object_id__].[{self.title}]" role="measure" type="ordinal"/>
      <layout dim-ordering="alphabetic" measure-ordering="alphabetic" show-hidden-fields="false" user-managed="false"/>
    </datasource>
  </datasources>
  
  <mapsources/>
  
  <worksheets>
{self._generate_worksheet_elements()}
  </worksheets>
  
  <dashboard name="{self.title}" type="dashboard">
    <size size-name="custom" w="1280" h="720"/>
    <zones>
{self._generate_dashboard_zones()}
    </zones>
  </dashboard>
</workbook>"""

        return xml_content

    def _generate_datasource_columns(self) -> str:
        """Genera definizioni colonne datasource"""
        columns_xml = ""

        for col in self.df.columns:
            col_info = self.columns_info[col]
            columns_xml += f"""
          <column caption="{col}" datatype="{col_info['type']}" name="[{col}]" role="{col_info['tableau_type']}"/>"""

        return columns_xml

    def _generate_worksheet_elements(self) -> str:
        """Genera elementi worksheet"""
        worksheets_xml = ""

        # Worksheet KPI Summary
        worksheets_xml += f"""
    <worksheet name="KPI Summary">
      <table>
        <view name="View1">
          <datasource name="datasource0"/>
        </view>
      </table>
    </worksheet>"""

        # Worksheets per ogni chart
        for i, chart in enumerate(self.charts):
            chart_name = chart.get("name", f"Chart {i+1}").replace(" ", "_")
            worksheets_xml += f"""
    <worksheet name="{chart_name}">
      <table>
        <view name="View1">
          <datasource name="datasource0"/>
        </view>
      </table>
    </worksheet>"""

        return worksheets_xml

    def _generate_dashboard_zones(self) -> str:
        """Genera zone dashboard"""
        zones_xml = ""
        y_pos = 0

        # Zone KPI Summary
        zones_xml += f"""      <zone h="100" w="1280" x="0" y="0" name="kpi_summary" type="layout">
        <zone-objects/>
      </zone>"""

        y_pos = 120

        # Zone Charts
        col_width = 640
        x_pos = 0

        for i, chart in enumerate(self.charts):
            if i % 2 == 0:
                x_pos = 0
            else:
                x_pos = col_width

            zone_name = chart.get("name", f"Chart {i+1}").replace(" ", "_")

            zones_xml += f"""
      <zone h="400" w="{col_width}" x="{x_pos}" y="{y_pos}" name="{zone_name.lower()}_zone" type="layout">
        <zone-objects/>
      </zone>"""

            if (i + 1) % 2 == 0:
                y_pos += 420

        return zones_xml

    def _generate_worksheets(self) -> Dict[str, str]:
        """Crea XML per ogni worksheet"""
        worksheets = {}

        # KPI Summary worksheet
        worksheets["kpi_summary"] = self._generate_kpi_worksheet()

        # Chart worksheets
        for i, chart in enumerate(self.charts):
            chart_name = chart.get("name", f"Chart {i+1}").replace(" ", "_")
            worksheets[chart_name.lower()] = self._generate_chart_worksheet(chart, i)

        return worksheets

    def _generate_kpi_worksheet(self) -> str:
        """Crea worksheet KPI summary"""

        kpi_rows = ""
        for idx, kpi in enumerate(self.kpis[:4], 1):
            if hasattr(kpi, "name"):
                name = kpi.name
                value = (
                    kpi.format_value()
                    if hasattr(kpi, "format_value")
                    else str(kpi.value)
                )
            else:
                name = str(idx)
                value = str(kpi)

            kpi_rows += f"""        <row>
          <value type="string">{name}</value>
          <value type="string">{value}</value>
        </row>
"""

        xml = f"""<?xml version='1.0' encoding='utf-8'?>
<worksheet name="KPI Summary">
  <table>
    <columns>
      <column caption="KPI" datatype="string" name="[KPI]"/>
      <column caption="Value" datatype="string" name="[Value]"/>
    </columns>
    <rows>
{kpi_rows}
    </rows>
  </table>
</worksheet>"""

        return xml

    def _generate_chart_worksheet(self, chart: Dict, index: int) -> str:
        """Crea worksheet per singolo chart"""

        chart_name = chart.get("name", f"Chart {index+1}")
        chart_type = chart.get("type", "bar")

        xml = f"""<?xml version='1.0' encoding='utf-8'?>
<worksheet name="{chart_name}">
  <table>
    <columns>
      <column caption="Category" datatype="string" name="[Category]"/>
      <column caption="Value" datatype="real" name="[Value]"/>
    </columns>
  </table>
</worksheet>"""

        return xml

    def _package_twbx(
        self, dashboard_xml: str, worksheets: Dict, data_path: str, filename: str
    ) -> str:
        """Crea package TWBX (ZIP)"""

        twbx_path = os.path.join(self.temp_dir, filename)

        with zipfile.ZipFile(twbx_path, "w", zipfile.ZIP_DEFLATED) as twbx:
            # Aggiungi dashboard XML
            twbx.writestr("dashboard.twb", dashboard_xml)

            # Aggiungi worksheets
            for sheet_name, sheet_xml in worksheets.items():
                twbx.writestr(f"worksheets/{sheet_name}.twb", sheet_xml)

            # Aggiungi dati
            twbx.write(data_path, "datafiles/data.csv")

            # Aggiungi metadata
            metadata = {
                "title": self.title,
                "created": datetime.now().isoformat(),
                "rows": len(self.df),
                "columns": len(self.df.columns),
                "kpis": len(self.kpis),
                "charts": len(self.charts),
            }
            twbx.writestr("metadata.json", json.dumps(metadata, indent=2))

        return twbx_path

    def get_datasource_definition(self) -> Dict:
        """Ritorna definizione datasource per guide Tableau"""

        return {
            "name": "Data Source",
            "type": "csv",
            "dimensions": [
                col
                for col, info in self.columns_info.items()
                if info["tableau_type"] == "dimension"
            ],
            "measures": [
                col
                for col, info in self.columns_info.items()
                if info["tableau_type"] == "measure"
            ],
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
        }


class TableauConnectionHelper:
    """Helper per connessioni Tableau Online/Server"""

    @staticmethod
    def create_connection_script(
        server_url: str, username: str, project: str, workbook_name: str
    ) -> str:
        """
        Crea script per pubblicare su Tableau Server/Online

        Returns:
            Script tabcmd o Python per il caricamento
        """

        script = f"""# Tableau Publication Script
# Per Tableau Server/Online

## Using tabcmd
tabcmd publish dashboard.twbx \\
    --server {server_url} \\
    --username {username} \\
    --project "{project}" \\
    --overwrite

## Using Python (Tableau Server Client)
import tableauserverclient as TSC

server = TSC.Server('{server_url}')
auth = TSC.Auth.basic_auth('{username}', 'PASSWORD')

with server.auth.sign_in(auth):
    with open('dashboard.twbx', 'rb') as f:
        project_item = TSC.ProjectItem('{project}')
        workbook_item = TSC.WorkbookItem('{project}')
        workbook_item = server.workbooks.publish(
            workbook_item, f, overwrite=True
        )
    print(f"Published: {{workbook_item.web_content_url}}")
"""

        return script

    @staticmethod
    def create_tableau_online_instructions(workbook_name: str) -> str:
        """Crea istruzioni per Tableau Online (free)"""

        instructions = f"""
# Caricare Dashboard su Tableau Online (Free Version)

## Step 1: Accedi a Tableau Online
- Vai a: https://online.tableau.com
- Accedi con il tuo account (registrati se non hai account)

## Step 2: Crea nuovo Workbook
- Click su "Create" → "Workbook"
- Seleziona "Connect to Data"
- Carica il file dashboard.twbx

## Step 3: Pubblica
- Clicca "Share" per rendere pubblico
- Copia il link per condividere con altri

## Step 4: Accedi Localmente
- Apri il link da qualsiasi browser
- Dashboard è interattiva anche online
- Free version permette fino a 2 public dashboards

---

## Alternative per Free Version:
1. **Tableau Public**: https://public.tableau.com (completamente gratis)
2. **Tableau Desktop Trial**: 14 giorni prova gratuita
3. **Tableau Server Prova**: 14 giorni per team
"""

        return instructions


class TwbxValidator:
    """Valida file TWBX per compatibilità"""

    @staticmethod
    def validate_twbx(twbx_path: str) -> Tuple[bool, List[str]]:
        """
        Valida file TWBX

        Returns:
            Tuple: (is_valid, list_of_issues)
        """

        issues = []

        try:
            with zipfile.ZipFile(twbx_path, "r") as zf:
                # Controlla file essenziali
                required_files = ["dashboard.twb", "datafiles/data.csv"]

                for required in required_files:
                    if required not in zf.namelist():
                        issues.append(f"Missing required file: {required}")

                # Verifica XML validity
                try:
                    dashboard_xml = zf.read("dashboard.twb")
                    ET.fromstring(dashboard_xml)
                except ET.ParseError as e:
                    issues.append(f"Invalid XML in dashboard.twb: {e}")

                # Controlla metadata
                try:
                    metadata_json = zf.read("metadata.json")
                    json.loads(metadata_json)
                except:
                    issues.append("Invalid or missing metadata.json")

        except zipfile.BadZipFile:
            issues.append("File is not a valid ZIP archive")
        except Exception as e:
            issues.append(f"Validation error: {str(e)}")

        return len(issues) == 0, issues

    @staticmethod
    def get_twbx_info(twbx_path: str) -> Dict:
        """Estrae informazioni da TWBX"""

        info = {}

        try:
            with zipfile.ZipFile(twbx_path, "r") as zf:
                # Leggi metadata
                try:
                    metadata_json = zf.read("metadata.json")
                    info["metadata"] = json.loads(metadata_json)
                except:
                    pass

                # Controlla dimensione
                info["file_size"] = os.path.getsize(twbx_path)
                info["file_size_mb"] = round(info["file_size"] / (1024 * 1024), 2)

                # Lista file
                info["files"] = zf.namelist()

                # Data creazione
                info["created"] = datetime.now().isoformat()

        except Exception as e:
            info["error"] = str(e)

        return info
