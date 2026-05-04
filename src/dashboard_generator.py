import plotly.graph_objects as go
import plotly.express as px
import json
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
        
        # Histograms per le prime 3 metriche numeriche
        for i, col in enumerate(self.numeric_cols[:3]):
            fig = px.histogram(self.df, x=col, title=f"Distribuzione {col}", 
                               template="plotly_white", marginal="box")
            charts_html += f"""
            <div class="chart-container">
                <div id="hist_{i}"></div>
            </div>
            <script>
                var hist_{i} = {json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)};
                Plotly.newPlot('hist_{i}', hist_{i}.data, hist_{i}.layout);
            </script>
            """
        
        # Matrice di correlazione se ci sono abbastanza colonne
        if len(self.numeric_cols) > 1:
            corr = self.df[self.numeric_cols].corr()
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto",
                                 title="Matrice di Correlazione",
                                 color_continuous_scale="RdBu")
            charts_html += f"""
            <div class="chart-container">
                <div id="corr_matrix"></div>
            </div>
            <script>
                var corr_matrix = {json.dumps(fig_corr.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)};
                Plotly.newPlot('corr_matrix', corr_matrix.data, corr_matrix.layout);
            </script>
            """
        
        # Grafico a barre per la prima categoria
        if self.categorical_cols:
            top_cat = self.df[self.categorical_cols[0]].value_counts().head(10)
            fig_bar = px.bar(x=top_cat.index, y=top_cat.values,
                            title=f"Top 10 {self.categorical_cols[0]}",
                            template="plotly_white")
            charts_html += f"""
            <div class="chart-container">
                <div id="bar_chart"></div>
            </div>
            <script>
                var bar_chart = {json.dumps(fig_bar.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)};
                Plotly.newPlot('bar_chart', bar_chart.data, bar_chart.layout);
            </script>
            """
        
        # Scatter plot se ci sono almeno 2 metriche
        if len(self.numeric_cols) >= 2:
            fig_scatter = px.scatter(self.df, x=self.numeric_cols[0], y=self.numeric_cols[1],
                                     title=f"Relazione {self.numeric_cols[0]} vs {self.numeric_cols[1]}",
                                     template="plotly_white", trendline="ols")
            charts_html += f"""
            <div class="chart-container">
                <div id="scatter_plot"></div>
            </div>
            <script>
                var scatter_plot = {json.dumps(fig_scatter.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)};
                Plotly.newPlot('scatter_plot', scatter_plot.data, scatter_plot.layout);
            </script>
            """
        
        # Genera HTML completo
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ML Dashboard - {datetime.now().strftime('%Y-%m-%d')}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
                .dashboard-container {{ padding: 20px; }}
                .kpi-card {{ background: white; border-radius: 15px; padding: 20px; margin: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); transition: transform 0.3s; }}
                .kpi-card:hover {{ transform: translateY(-5px); }}
                .kpi-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
                .kpi-label {{ color: #666; font-size: 0.9em; text-transform: uppercase; }}
                .chart-container {{ background: white; border-radius: 15px; padding: 20px; margin: 20px 0; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }}
                .insight-box {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 15px; padding: 20px; margin: 20px 0; }}
                h1, h2 {{ color: white; margin-bottom: 20px; }}
                .recommendation {{ background: #f8f9fa; border-left: 4px solid #667eea; padding: 15px; margin: 10px 0; border-radius: 10px; }}
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
                        <p>Data Quality Score: {self.insights['data_quality'].get('score', 0):.1f}/100</p>
                        <p>Missing Data: {self.insights['data_quality'].get('missing_percentage', 0):.1f}%</p>
                        <p>Outliers Detected: {len(self.insights.get('anomalies', []))} righe anomale</p>
                    </div>
                    
                    <!-- Charts Section -->
                    {charts_html}
                    
                    <!-- Recommendations -->
                    <div class="chart-container">
                        <h4>📋 Raccomandazioni per Tableau</h4>
                        <div id="recommendations">
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
                
                kpi_html += f"""
                    <div class="col-md-3">
                        <div class="kpi-card">
                            <div class="kpi-label">{col.upper()}</div>
                            <div class="kpi-value">{avg_val:,.2f}</div>
                            <small>Media: {avg_val:,.2f} | Max: {self.df[col].max():,.2f}</small>
                        </div>
                    </div>
                """
            except:
                continue
        
        if not kpi_html:
            kpi_html = '<div class="col-12"><p class="text-white">Nessuna metrica numerica disponibile</p></div>'
        
        return kpi_html
