import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import pandas as pd
import numpy as np
from datetime import datetime

class DashboardGenerator:
    def __init__(self, df, ml_analyzer, insights):
        self.df = df
        self.ml_analyzer = ml_analyzer
        self.insights = insights
        self.numeric_cols = ml_analyzer.numeric_cols if ml_analyzer else []
        self.categorical_cols = ml_analyzer.categorical_cols if ml_analyzer else []
        
    def create_dashboard_html(self):
        """Crea dashboard HTML con grafici funzionanti"""
        
        # Genera KPI cards
        kpi_html = self.generate_kpi_cards()
        
        # Genera grafici uno per uno in modo sicuro
        charts_list = []
        
        # 1. Istogrammi per le metriche numeriche
        for i, col in enumerate(self.numeric_cols[:3]):
            try:
                fig = self.create_histogram_safe(col)
                if fig:
                    fig_json = json.dumps(fig, cls=PlotlyJSONEncoder)
                    charts_list.append(f"""
                    <div class="chart-container">
                        <h4>Distribuzione {col}</h4>
                        <div id="hist_{i}" style="width:100%; height:450px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_{i} = {fig_json};
                            Plotly.newPlot('hist_{i}', fig_{i}.data, fig_{i}.layout);
                        }})();
                    </script>
                    """)
            except Exception as e:
                charts_list.append(f"<div class='alert alert-warning'>Errore nel grafico per {col}: {str(e)}</div>")
        
        # 2. Box plot
        if len(self.numeric_cols) > 0:
            try:
                fig_box = self.create_boxplot_safe(self.numeric_cols[0])
                if fig_box:
                    fig_box_json = json.dumps(fig_box, cls=PlotlyJSONEncoder)
                    charts_list.append(f"""
                    <div class="chart-container">
                        <h4>Box Plot - {self.numeric_cols[0]}</h4>
                        <div id="box_plot" style="width:100%; height:450px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_box = {fig_box_json};
                            Plotly.newPlot('box_plot', fig_box.data, fig_box.layout);
                        }})();
                    </script>
                    """)
            except Exception as e:
                charts_list.append(f"<div class='alert alert-warning'>Errore nel box plot: {str(e)}</div>")
        
        # 3. Bar chart per categorie
        if len(self.categorical_cols) > 0:
            try:
                fig_bar = self.create_barchart_safe(self.categorical_cols[0])
                if fig_bar:
                    fig_bar_json = json.dumps(fig_bar, cls=PlotlyJSONEncoder)
                    charts_list.append(f"""
                    <div class="chart-container">
                        <h4>Top {self.categorical_cols[0]}</h4>
                        <div id="bar_chart" style="width:100%; height:450px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_bar = {fig_bar_json};
                            Plotly.newPlot('bar_chart', fig_bar.data, fig_bar.layout);
                        }})();
                    </script>
                    """)
            except Exception as e:
                charts_list.append(f"<div class='alert alert-warning'>Errore nel bar chart: {str(e)}</div>")
        
        # 4. Scatter plot
        if len(self.numeric_cols) >= 2:
            try:
                fig_scatter = self.create_scatter_safe(self.numeric_cols[0], self.numeric_cols[1])
                if fig_scatter:
                    fig_scatter_json = json.dumps(fig_scatter, cls=PlotlyJSONEncoder)
                    charts_list.append(f"""
                    <div class="chart-container">
                        <h4>Relazione {self.numeric_cols[0]} vs {self.numeric_cols[1]}</h4>
                        <div id="scatter_plot" style="width:100%; height:450px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_scatter = {fig_scatter_json};
                            Plotly.newPlot('scatter_plot', fig_scatter.data, fig_scatter.layout);
                        }})();
                    </script>
                    """)
            except Exception as e:
                charts_list.append(f"<div class='alert alert-warning'>Errore nello scatter plot: {str(e)}</div>")
        
        # 5. Time series
        if self.ml_analyzer and self.ml_analyzer.datetime_cols and len(self.numeric_cols) > 0:
            try:
                date_col = self.ml_analyzer.datetime_cols[0]
                fig_line = self.create_timeseries_safe(date_col, self.numeric_cols[0])
                if fig_line:
                    fig_line_json = json.dumps(fig_line, cls=PlotlyJSONEncoder)
                    charts_list.append(f"""
                    <div class="chart-container">
                        <h4>Trend {self.numeric_cols[0]} nel tempo</h4>
                        <div id="line_chart" style="width:100%; height:450px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_line = {fig_line_json};
                            Plotly.newPlot('line_chart', fig_line.data, fig_line.layout);
                        }})();
                    </script>
                    """)
            except Exception as e:
                charts_list.append(f"<div class='alert alert-warning'>Errore nel time series: {str(e)}</div>")
        
        # 6. Heatmap correlazioni
        if len(self.numeric_cols) > 1:
            try:
                fig_heat = self.create_heatmap_safe()
                if fig_heat:
                    fig_heat_json = json.dumps(fig_heat, cls=PlotlyJSONEncoder)
                    charts_list.append(f"""
                    <div class="chart-container">
                        <h4>Matrice di Correlazione</h4>
                        <div id="heatmap" style="width:100%; height:550px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_heat = {fig_heat_json};
                            Plotly.newPlot('heatmap', fig_heat.data, fig_heat.layout);
                        }})();
                    </script>
                    """)
            except Exception as e:
                charts_list.append(f"<div class='alert alert-warning'>Errore nella heatmap: {str(e)}</div>")
        
        # Combina tutto
        charts_html = "".join(charts_list)
        
        # HTML completo
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tableau Style Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-3.0.1.min.js" charset="utf-8"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ 
                    background: #f5f5f5; 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                    margin: 0; 
                    padding: 20px; 
                }}
                .dashboard-container {{ 
                    max-width: 1400px; 
                    margin: 0 auto; 
                }}
                .kpi-card {{ 
                    background: white; 
                    border-radius: 8px; 
                    padding: 20px; 
                    margin: 10px; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1); 
                    text-align: center;
                    border-top: 3px solid #1f77b4;
                }}
                .kpi-value {{ 
                    font-size: 2.2em; 
                    font-weight: 600; 
                    color: #1f77b4; 
                }}
                .kpi-label {{ 
                    color: #666; 
                    font-size: 0.85em; 
                    text-transform: uppercase; 
                    letter-spacing: 1px;
                    font-weight: 600;
                }}
                .chart-container {{ 
                    background: white; 
                    border-radius: 8px; 
                    padding: 20px; 
                    margin: 20px 0; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .chart-container h4 {{
                    color: #333;
                    margin-bottom: 15px;
                    font-size: 16px;
                    font-weight: 600;
                }}
                .insight-box {{ 
                    background: white;
                    border-left: 4px solid #1f77b4;
                    padding: 20px; 
                    margin: 20px 0; 
                    border-radius: 4px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                }}
                .recommendation {{ 
                    background: #f9f9f9; 
                    border-left: 4px solid #1f77b4; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 4px;
                }}
                .alert-warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffecb5;
                    color: #856404;
                    padding: 12px;
                    border-radius: 4px;
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="container-fluid">
                    <h1 class="text-center mb-4">📊 Tableau Style Dashboard</h1>
                    <p class="text-center text-muted mb-4">Dashboard generata automaticamente</p>
                    
                    <!-- KPI Section -->
                    <div class="row">
                        {kpi_html}
                    </div>
                    
                    <!-- Charts Section -->
                    {charts_html}
                    
                    <!-- Insights -->
                    <div class="insight-box">
                        <h4>🤖 ML Insights</h4>
                        <p><strong>Qualità dati:</strong> {self.insights['data_quality'].get('score', 0):.1f}/100</p>
                        <p><strong>Dati mancanti:</strong> {self.insights['data_quality'].get('missing_percentage', 0):.1f}%</p>
                    </div>
                    
                    <!-- Recommendations -->
                    <div class="chart-container">
                        <h4>📋 Raccomandazioni Tableau</h4>
            """
        
        for rec in self.insights.get('recommendations', [])[:5]:
            html_content += f"""
                        <div class="recommendation">
                            <strong>{rec.get('type', 'Info').upper()}:</strong> {rec.get('text', '')}<br>
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
    
    def create_histogram_safe(self, column):
        """Crea istogramma in modo sicuro"""
        try:
            data = self.df[column].dropna()
            if len(data) == 0:
                return None
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=data,
                nbinsx=min(30, int(np.sqrt(len(data)))),
                marker_color='#1f77b4',
                marker_line_color='white',
                marker_line_width=1,
                opacity=0.8
            ))
            
            fig.update_layout(
                title=None,
                xaxis_title=column,
                yaxis_title="Conteggio",
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=450,
                margin=dict(l=50, r=30, t=30, b=50),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#e6e6e6',
                    showline=True,
                    linecolor='#cccccc'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#e6e6e6',
                    showline=True,
                    linecolor='#cccccc'
                )
            )
            
            return fig.to_dict()
        except Exception as e:
            print(f"Errore in histogram: {e}")
            return None
    
    def create_boxplot_safe(self, column):
        """Crea box plot in modo sicuro"""
        try:
            data = self.df[column].dropna()
            if len(data) == 0:
                return None
            
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=data,
                name=column,
                boxmean='sd',
                marker_color='#2ca02c',
                line_color='#2ca02c'
            ))
            
            fig.update_layout(
                title=None,
                yaxis_title=column,
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=450,
                margin=dict(l=50, r=30, t=30, b=50)
            )
            
            return fig.to_dict()
        except Exception as e:
            print(f"Errore in boxplot: {e}")
            return None
    
    def create_barchart_safe(self, column):
        """Crea bar chart in modo sicuro"""
        try:
            value_counts = self.df[column].value_counts().head(10)
            if len(value_counts) == 0:
                return None
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=value_counts.values,
                y=value_counts.index,
                orientation='h',
                marker_color='#ff7f0e',
                text=value_counts.values,
                textposition='outside'
            ))
            
            fig.update_layout(
                title=None,
                xaxis_title="Conteggio",
                yaxis_title=column,
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=450,
                margin=dict(l=100, r=30, t=30, b=50),
                xaxis=dict(showgrid=True, gridcolor='#e6e6e6'),
                yaxis=dict(showgrid=False)
            )
            
            return fig.to_dict()
        except Exception as e:
            print(f"Errore in barchart: {e}")
            return None
    
    def create_scatter_safe(self, x_col, y_col):
        """Crea scatter plot in modo sicuro"""
        try:
            data = self.df[[x_col, y_col]].dropna()
            if len(data) == 0:
                return None
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                mode='markers',
                marker=dict(size=8, color='#9467bd', opacity=0.6)
            ))
            
            fig.update_layout(
                title=None,
                xaxis_title=x_col,
                yaxis_title=y_col,
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=450,
                margin=dict(l=50, r=30, t=30, b=50)
            )
            
            return fig.to_dict()
        except Exception as e:
            print(f"Errore in scatter: {e}")
            return None
    
    def create_timeseries_safe(self, date_col, metric_col):
        """Crea time series in modo sicuro"""
        try:
            data = self.df[[date_col, metric_col]].dropna()
            if len(data) == 0:
                return None
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data[date_col],
                y=data[metric_col],
                mode='lines+markers',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4, color='#1f77b4')
            ))
            
            fig.update_layout(
                title=None,
                xaxis_title=date_col,
                yaxis_title=metric_col,
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=450,
                margin=dict(l=50, r=30, t=30, b=50)
            )
            
            return fig.to_dict()
        except Exception as e:
            print(f"Errore in timeseries: {e}")
            return None
    
    def create_heatmap_safe(self):
        """Crea heatmap in modo sicuro"""
        try:
            corr = self.df[self.numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10}
            ))
            
            fig.update_layout(
                title=None,
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=500,
                margin=dict(l=80, r=30, t=30, b=80),
                xaxis=dict(tickangle=45),
                yaxis=dict(tickangle=0)
            )
            
            return fig.to_dict()
        except Exception as e:
            print(f"Errore in heatmap: {e}")
            return None
    
    def generate_kpi_cards(self):
        """Genera KPI cards"""
        kpi_html = ""
        metrics_to_show = self.numeric_cols[:4] if len(self.numeric_cols) >= 4 else self.numeric_cols
        
        for col in metrics_to_show:
            try:
                avg_val = self.df[col].mean()
                if pd.isna(avg_val):
                    continue
                
                kpi_html += f"""
                    <div class="col-md-3">
                        <div class="kpi-card">
                            <div class="kpi-label">{col.upper()}</div>
                            <div class="kpi-value">{avg_val:,.2f}</div>
                        </div>
                    </div>
                """
            except:
                continue
        
        if not kpi_html:
            kpi_html = '<div class="col-12"><p class="text-center">Nessuna metrica disponibile</p></div>'
        
        return kpi_html
