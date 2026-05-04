import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import pandas as pd
from datetime import datetime

class DashboardGenerator:
    def __init__(self, df, ml_analyzer, insights):
        self.df = df
        self.ml_analyzer = ml_analyzer
        self.insights = insights
        self.numeric_cols = ml_analyzer.numeric_cols if ml_analyzer else []
        self.categorical_cols = ml_analyzer.categorical_cols if ml_analyzer else []
        
    def create_dashboard_html(self):
        """Crea dashboard HTML interattiva"""
        
        # Genera KPI cards
        kpi_html = self.generate_kpi_cards()
        
        # Genera grafici base
        charts_html = ""
        charts_list = []
        
        # Histograms per le prime 3 metriche numeriche
        for i, col in enumerate(self.numeric_cols[:3]):
            try:
                fig = px.histogram(self.df, x=col, title=f"Distribuzione {col}", 
                                   template="plotly_white", marginal="box")
                # Converti figura in JSON
                fig_json = json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <h4>Distribuzione: {col}</h4>
                    <div id="hist_{i}"></div>
                </div>
                <script>
                    var hist_{i} = {fig_json};
                    Plotly.newPlot('hist_{i}', hist_{i}.data, hist_{i}.layout);
                </script>
                """
            except Exception as e:
                charts_html += f"<p>Errore nel grafico per {col}: {str(e)}</p>"
        
        # Box plot per i valori anomali
        if len(self.numeric_cols) > 0:
            try:
                fig_box = px.box(self.df, y=self.numeric_cols[0], title=f"Box Plot - {self.numeric_cols[0]}",
                                template="plotly_white")
                fig_box_json = json.dumps(fig_box.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <h4>Analisi Outlier: {self.numeric_cols[0]}</h4>
                    <div id="box_plot"></div>
                </div>
                <script>
                    var box_plot = {fig_box_json};
                    Plotly.newPlot('box_plot', box_plot.data, box_plot.layout);
                </script>
                """
            except:
                pass
        
        # Matrice di correlazione se ci sono abbastanza colonne
        if len(self.numeric_cols) > 1:
            try:
                corr = self.df[self.numeric_cols].corr()
                fig_corr = px.imshow(corr, text_auto=True, aspect="auto",
                                     title="Matrice di Correlazione",
                                     color_continuous_scale="RdBu",
                                     template="plotly_white")
                fig_corr_json = json.dumps(fig_corr.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <h4>Matrice di Correlazione</h4>
                    <div id="corr_matrix"></div>
                </div>
                <script>
                    var corr_matrix = {fig_corr_json};
                    Plotly.newPlot('corr_matrix', corr_matrix.data, corr_matrix.layout);
                </script>
                """
            except:
                pass
        
        # Grafico a barre per la prima categoria
        if self.categorical_cols and len(self.categorical_cols) > 0:
            try:
                top_cat = self.df[self.categorical_cols[0]].value_counts().head(10)
                fig_bar = px.bar(x=top_cat.index, y=top_cat.values,
                                title=f"Top 10 {self.categorical_cols[0]}",
                                template="plotly_white",
                                labels={'x': self.categorical_cols[0], 'y': 'Conteggio'})
                fig_bar_json = json.dumps(fig_bar.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <h4>Categorie principali: {self.categorical_cols[0]}</h4>
                    <div id="bar_chart"></div>
                </div>
                <script>
                    var bar_chart = {fig_bar_json};
                    Plotly.newPlot('bar_chart', bar_chart.data, bar_chart.layout);
                </script>
                """
            except:
                pass
        
        # Scatter plot se ci sono almeno 2 metriche
        if len(self.numeric_cols) >= 2:
            try:
                fig_scatter = px.scatter(self.df, x=self.numeric_cols[0], y=self.numeric_cols[1],
                                        title=f"Relazione {self.numeric_cols[0]} vs {self.numeric_cols[1]}",
                                        template="plotly_white", 
                                        trendline="ols",
                                        labels={'x': self.numeric_cols[0], 'y': self.numeric_cols[1]})
                fig_scatter_json = json.dumps(fig_scatter.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <h4>Relazione tra variabili</h4>
                    <div id="scatter_plot"></div>
                </div>
                <script>
                    var scatter_plot = {fig_scatter_json};
                    Plotly.newPlot('scatter_plot', scatter_plot.data, scatter_plot.layout);
                </script>
                """
            except:
                pass
        
        # Line chart per serie temporali
        if self.ml_analyzer and self.ml_analyzer.datetime_cols and len(self.numeric_cols) > 0:
            try:
                date_col = self.ml_analyzer.datetime_cols[0]
                fig_line = px.line(self.df, x=date_col, y=self.numeric_cols[0],
                                  title=f"Trend di {self.numeric_cols[0]} nel tempo",
                                  template="plotly_white",
                                  labels={'x': 'Data', 'y': self.numeric_cols[0]})
                fig_line_json = json.dumps(fig_line.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <h4>Serie Temporale</h4>
                    <div id="line_chart"></div>
                </div>
                <script>
                    var line_chart = {fig_line_json};
                    Plotly.newPlot('line_chart', line_chart.data, line_chart.layout);
                </script>
                """
            except:
                pass
        
        # Genera HTML completo
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ML Dashboard - {datetime.now().strftime('%Y-%m-%d')}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }}
                .dashboard-container {{ max-width: 1400px; margin: 0 auto; }}
                .kpi-card {{ background: white; border-radius: 15px; padding: 20px; margin: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); transition: transform 0.3s; text-align: center; }}
                .kpi-card:hover {{ transform: translateY(-5px); }}
                .kpi-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
                .kpi-label {{ color: #666; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }}
                .chart-container {{ background: white; border-radius: 15px; padding: 20px; margin: 20px 0; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }}
                .insight-box {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 15px; padding: 20px; margin: 20px 0; }}
                h1, h2, h3, h4 {{ color: white; margin-bottom: 20px; }}
                .recommendation {{ background: #f8f9fa; border-left: 4px solid #667eea; padding: 15px; margin: 10px 0; border-radius: 10px; }}
                .metric-card {{ background: white; border-radius: 10px; padding: 15px; margin: 10px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="container-fluid">
                    <h1 class="text-center mb-4">📊 ML-Powered Smart Dashboard</h1>
                    <p class="text-center text-white mb-5">Dashboard generata automaticamente con Machine Learning</p>
                    
                    <!-- KPI Section -->
                    <div class="row">
                        {kpi_html}
                    </div>
                    
                    <!-- Insights Section -->
                    <div class="insight-box">
                        <h3>🤖 ML Insights</h3>
                        <div class="row">
                            <div class="col-md-4">
                                <p><strong>Data Quality Score:</strong> {self.insights['data_quality'].get('score', 0):.1f}/100</p>
                            </div>
                            <div class="col-md-4">
                                <p><strong>Missing Data:</strong> {self.insights['data_quality'].get('missing_percentage', 0):.1f}%</p>
                            </div>
                            <div class="col-md-4">
                                <p><strong>Outliers Detected:</strong> {len(self.insights.get('anomalies', []))} righe anomale</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Charts Section -->
                    {charts_html}
                    
                    <!-- Recommendations -->
                    <div class="chart-container">
                        <h4>📋 Raccomandazioni per Tableau</h4>
        """
        
        for rec in self.insights.get('recommendations', [])[:5]:
            html_content += f"""
                        <div class="recommendation">
                            <strong>{rec.get('type', 'general').upper()}:</strong> {rec.get('text', '')}<br>
                            <small>🎯 {rec.get('action', '')}</small>
                        </div>
            """
        
        html_content += """
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def generate_kpi_cards(self):
        """Genera KPI cards dinamiche"""
        kpi_html = ""
        
        # Seleziona metriche principali
        metrics_to_show = self.numeric_cols[:4] if len(self.numeric_cols) >= 4 else self.numeric_cols
        
        for col in metrics_to_show:
            try:
                avg_val = self.df[col].mean()
                if pd.isna(avg_val):
                    avg_val = 0
                
                # Calcola trend (crescente/decrescente)
                trend = "📈" if len(self.df) > 1 and self.df[col].iloc[-1] > self.df[col].iloc[0] else "📉"
                
                kpi_html += f"""
                    <div class="col-md-3">
                        <div class="kpi-card">
                            <div class="kpi-label">{col.upper()}</div>
                            <div class="kpi-value">{avg_val:,.2f} {trend}</div>
                            <small>Media: {avg_val:,.2f} | Max: {self.df[col].max():,.2f}</small>
                        </div>
                    </div>
                """
            except Exception as e:
                continue
        
        if not kpi_html:
            kpi_html = '<div class="col-12"><p class="text-white text-center">Nessuna metrica numerica disponibile</p></div>'
        
        return kpi_html
