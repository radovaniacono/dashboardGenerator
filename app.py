import plotly.graph_objects as go
import plotly.express as px
import json
import pandas as pd
import numpy as np
from datetime import datetime
import random

class DashboardGenerator:
    def __init__(self, df, ml_analyzer, insights):
        self.df = df
        self.ml_analyzer = ml_analyzer
        self.insights = insights
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Colori pastello
        self.colors = ['#A8E6CF', '#FFD3B6', '#FFAAA5', '#C7CEEA', '#B5EAD7', '#FFDAC1']
    
    def create_dashboard_html(self):
        """Crea dashboard HTML semplice ma funzionante"""
        
        # Genera grafici
        charts_html = ""
        
        # Istogramma (se ci sono dati numerici)
        if self.numeric_cols:
            fig1 = px.histogram(self.df, x=self.numeric_cols[0], 
                                title=f"Distribuzione {self.numeric_cols[0]}",
                                color_discrete_sequence=[self.colors[0]],
                                template="plotly_white")
            charts_html += f"""
            <div class="chart-card">
                <div id="chart1" style="width:100%; height:350px;"></div>
            </div>
            <script>
                var fig1 = {json.dumps(fig1.to_dict())};
                Plotly.newPlot('chart1', fig1.data, fig1.layout);
            </script>
            """
        
        # Bar chart (se ci sono dati categorici)
        if self.categorical_cols:
            counts = self.df[self.categorical_cols[0]].value_counts().head(8)
            fig2 = px.bar(x=counts.index, y=counts.values,
                          title=f"Top {self.categorical_cols[0]}",
                          color_discrete_sequence=[self.colors[1]],
                          template="plotly_white")
            charts_html += f"""
            <div class="chart-card">
                <div id="chart2" style="width:100%; height:350px;"></div>
            </div>
            <script>
                var fig2 = {json.dumps(fig2.to_dict())};
                Plotly.newPlot('chart2', fig2.data, fig2.layout);
            </script>
            """
        
        # Scatter plot (se ci sono almeno 2 metriche numeriche)
        if len(self.numeric_cols) >= 2:
            fig3 = px.scatter(self.df, x=self.numeric_cols[0], y=self.numeric_cols[1],
                              title=f"{self.numeric_cols[0]} vs {self.numeric_cols[1]}",
                              color_discrete_sequence=[self.colors[2]],
                              template="plotly_white")
            charts_html += f"""
            <div class="chart-card">
                <div id="chart3" style="width:100%; height:350px;"></div>
            </div>
            <script>
                var fig3 = {json.dumps(fig3.to_dict())};
                Plotly.newPlot('chart3', fig3.data, fig3.layout);
            </script>
            """
        
        # Box plot
        if self.numeric_cols:
            fig4 = px.box(self.df, y=self.numeric_cols[0],
                          title=f"Box plot {self.numeric_cols[0]}",
                          color_discrete_sequence=[self.colors[3]],
                          template="plotly_white")
            charts_html += f"""
            <div class="chart-card">
                <div id="chart4" style="width:100%; height:350px;"></div>
            </div>
            <script>
                var fig4 = {json.dumps(fig4.to_dict())};
                Plotly.newPlot('chart4', fig4.data, fig4.layout);
            </script>
            """
        
        # HTML completo
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-3.0.1.min.js"></script>
            <meta charset="UTF-8">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    background: #F9FBF4;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    padding: 20px;
                }}
                .dashboard {{
                    max-width: 1400px;
                    margin: 0 auto;
                }}
                .header {{
                    text-align: center;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 15px;
                    color: white;
                    margin-bottom: 20px;
                }}
                .charts-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                }}
                .chart-card {{
                    background: white;
                    border-radius: 15px;
                    padding: 15px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                }}
                @media (max-width: 768px) {{
                    .charts-grid {{ grid-template-columns: 1fr; }}
                }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1>📊 Pastel Dashboard</h1>
                    <p>Dashboard generata automaticamente</p>
                </div>
                <div class="charts-grid">
                    {charts_html}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
