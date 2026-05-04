import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
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
        self.numeric_cols = ml_analyzer.numeric_cols if ml_analyzer else []
        self.categorical_cols = ml_analyzer.categorical_cols if ml_analyzer else []
        
        # Inizializza seed per randomizzazione
        random.seed(hash(str(df.shape) + str(df.columns.tolist())) % 2**32)
        
        # Seleziona tema casuale
        self.theme = self.select_random_theme()
        
        # Seleziona layout casuale
        self.layout_type = random.choice(['grid', 'waterfall', 'dashboard', 'magazine', 'minimal'])
        
        # Seleziona tipi di grafici casuali
        self.chart_types = self.select_random_charts()
        
    def select_random_theme(self):
        """Seleziona un tema casuale per la dashboard"""
        themes = [
            {
                'name': 'Tableau Classic',
                'primary': '#1f77b4',
                'secondary': '#ff7f0e',
                'tertiary': '#2ca02c',
                'background': '#ffffff',
                'card_bg': '#ffffff',
                'text': '#333333',
                'grid': '#e6e6e6'
            },
            {
                'name': 'Dark Modern',
                'primary': '#00ffff',
                'secondary': '#ff00ff',
                'tertiary': '#00ff00',
                'background': '#1e1e1e',
                'card_bg': '#2d2d2d',
                'text': '#ffffff',
                'grid': '#404040'
            },
            {
                'name': 'Corporate Blue',
                'primary': '#003f5c',
                'secondary': '#58508d',
                'tertiary': '#bc5090',
                'background': '#f0f2f6',
                'card_bg': '#ffffff',
                'text': '#2c3e50',
                'grid': '#d3d9e0'
            },
            {
                'name': 'Sunset',
                'primary': '#ff6b35',
                'secondary': '#f7c59f',
                'tertiary': '#efefd0',
                'background': '#fff5e6',
                'card_bg': '#ffffff',
                'text': '#4a4a4a',
                'grid': '#ffe0cc'
            },
            {
                'name': 'Forest',
                'primary': '#2d6a4f',
                'secondary': '#40916c',
                'tertiary': '#52b788',
                'background': '#f0f7f0',
                'card_bg': '#ffffff',
                'text': '#1b4332',
                'grid': '#d4e6d4'
            },
            {
                'name': 'Ocean',
                'primary': '#0077b6',
                'secondary': '#0096c7',
                'tertiary': '#00b4d8',
                'background': '#e0f7fa',
                'card_bg': '#ffffff',
                'text': '#023e8a',
                'grid': '#b3e5fc'
            }
        ]
        return random.choice(themes)
    
    def select_random_charts(self):
        """Seleziona casualmente quali tipi di grafici generare"""
        available_charts = []
        
        if self.numeric_cols:
            available_charts.append('histogram')
            available_charts.append('boxplot')
        
        if self.categorical_cols and self.numeric_cols:
            available_charts.append('barchart')
        
        if len(self.numeric_cols) >= 2:
            available_charts.append('scatter')
        
        if self.ml_analyzer and self.ml_analyzer.datetime_cols and self.numeric_cols:
            available_charts.append('timeseries')
        
        if len(self.numeric_cols) > 1:
            available_charts.append('heatmap')
        
        # Seleziona 3-5 grafici casuali
        num_charts = min(random.randint(3, 5), len(available_charts))
        if num_charts < 1:
            num_charts = 1
        
        return random.sample(available_charts, num_charts)
    
    def create_histogram(self, index):
        """Crea istogramma"""
        col = random.choice(self.numeric_cols)
        data = self.df[col].dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data,
            nbinsx=min(30, int(np.sqrt(len(data)))),
            marker_color=self.theme['primary'],
            marker_line_color='white',
            marker_line_width=1,
            opacity=0.8
        ))
        
        fig.update_layout(
            title=f"Distribuzione {col}",
            xaxis_title=col,
            yaxis_title="Frequenza",
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig
    
    def create_boxplot(self, index):
        """Crea box plot"""
        col = random.choice(self.numeric_cols)
        
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=self.df[col].dropna(),
            name=col,
            marker_color=self.theme['primary'],
            line_color=self.theme['primary']
        ))
        
        fig.update_layout(
            title=f"Distribuzione {col}",
            yaxis_title=col,
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig
    
    def create_barchart(self, index):
        """Crea bar chart"""
        col = random.choice(self.categorical_cols)
        value_counts = self.df[col].value_counts().head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=value_counts.index,
            y=value_counts.values,
            marker_color=self.theme['secondary'],
            text=value_counts.values,
            textposition='outside'
        ))
        
        fig.update_layout(
            title=f"Top 10 {col}",
            xaxis_title=col,
            yaxis_title="Conteggio",
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig
    
    def create_scatter(self, index):
        """Crea scatter plot"""
        col1, col2 = random.sample(self.numeric_cols, 2)
        data = self.df[[col1, col2]].dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data[col1],
            y=data[col2],
            mode='markers',
            marker=dict(
                size=8,
                color=self.theme['primary'],
                opacity=0.6
            ),
            name='Dati'
        ))
        
        fig.update_layout(
            title=f"Relazione tra {col1} e {col2}",
            xaxis_title=col1,
            yaxis_title=col2,
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig
    
    def create_timeseries(self, index):
        """Crea time series"""
        date_col = self.ml_analyzer.datetime_cols[0]
        metric_col = random.choice(self.numeric_cols)
        
        data = self.df[[date_col, metric_col]].dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data[date_col],
            y=data[metric_col],
            mode='lines+markers',
            line=dict(color=self.theme['primary'], width=2),
            marker=dict(size=4, color=self.theme['primary']),
            name=metric_col
        ))
        
        fig.update_layout(
            title=f"Trend {metric_col} nel tempo",
            xaxis_title=date_col,
            yaxis_title=metric_col,
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text']),
            hovermode='x unified'
        )
        
        return fig
    
    def create_heatmap(self, index):
        """Crea heatmap delle correlazioni"""
        # Seleziona un sottoinsieme di colonne
        n_cols = min(len(self.numeric_cols), 6)
        selected_cols = random.sample(self.numeric_cols, n_cols)
        
        corr = self.df[selected_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Matrice di Correlazione",
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=500,
            margin=dict(l=100, r=30, t=50, b=100),
            font=dict(color=self.theme['text']),
            xaxis=dict(tickangle=45),
            yaxis=dict(tickangle=0)
        )
        
        return fig
    
    def create_dashboard_html(self):
        """Crea dashboard HTML con grafici randomizzati"""
        
        # Genera KPI cards
        kpi_html = self.generate_kpi_cards()
        
        # Genera grafici randomizzati
        charts_html = ""
        
        chart_functions = {
            'histogram': self.create_histogram,
            'boxplot': self.create_boxplot,
            'barchart': self.create_barchart,
            'scatter': self.create_scatter,
            'timeseries': self.create_timeseries,
            'heatmap': self.create_heatmap
        }
        
        for idx, chart_type in enumerate(self.chart_types):
            try:
                if chart_type in chart_functions:
                    fig = chart_functions[chart_type](idx)
                    if fig:
                        fig_json = json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder)
                        charts_html += f"""
                        <div class="chart-container" style="background: {self.theme['card_bg']};">
                            <div id="chart_{idx}" style="width:100%; height:450px;"></div>
                        </div>
                        <script>
                            (function() {{
                                var fig_{idx} = {fig_json};
                                Plotly.newPlot('chart_{idx}', fig_{idx}.data, fig_{idx}.layout);
                            }})();
                        </script>
                        """
            except Exception as e:
                charts_html += f"<div class='alert alert-warning'>Errore nel grafico {chart_type}: {str(e)}</div>"
        
        # Layout CSS
        layout_css = self.get_layout_css()
        
        # HTML completo
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dynamic Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-3.0.1.min.js" charset="utf-8"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ 
                    background: {self.theme['background']}; 
                    font-family: Arial, sans-serif;
                    margin: 0; 
                    padding: 20px; 
                }}
                .dashboard-container {{ 
                    max-width: 1400px; 
                    margin: 0 auto; 
                }}
                .dashboard-header {{
                    text-align: center;
                    padding: 30px;
                    background: linear-gradient(135deg, {self.theme['primary']}, {self.theme['secondary']});
                    border-radius: 15px;
                    margin-bottom: 30px;
                    color: white;
                }}
                .dashboard-header h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }}
                .kpi-card {{ 
                    background: {self.theme['card_bg']}; 
                    border-radius: 10px; 
                    padding: 20px; 
                    margin: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                    text-align: center;
                    border-top: 3px solid {self.theme['primary']};
                }}
                .kpi-value {{ 
                    font-size: 2em; 
                    font-weight: bold; 
                    color: {self.theme['primary']}; 
                }}
                .kpi-label {{ 
                    color: {self.theme['text']}; 
                    font-size: 0.85em; 
                    text-transform: uppercase; 
                    letter-spacing: 1px;
                }}
                .chart-container {{ 
                    background: {self.theme['card_bg']}; 
                    border-radius: 10px; 
                    padding: 20px; 
                    margin: 20px 0; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .insight-box {{ 
                    background: {self.theme['card_bg']};
                    border-left: 4px solid {self.theme['primary']};
                    padding: 20px; 
                    margin: 20px 0; 
                    border-radius: 8px;
                }}
                .recommendation {{ 
                    background: {self.theme['background']}; 
                    border-left: 4px solid {self.theme['secondary']}; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 8px;
                }}
                .alert-warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffecb5;
                    color: #856404;
                    padding: 12px;
                    border-radius: 4px;
                    margin: 10px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    margin-top: 40px;
                    color: {self.theme['text']};
                    opacity: 0.7;
                }}
                {layout_css}
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h1>🎲 Dynamic ML Dashboard</h1>
                    <p>Tema: {self.theme['name']} | Layout: {self.layout_type} | {len(self.chart_types)} grafici</p>
                </div>
                
                <!-- KPI Section -->
                <div class="row">
                    {kpi_html}
                </div>
                
                <!-- Charts Section -->
                {charts_html}
                
                <!-- ML Insights -->
                <div class="insight-box">
                    <h3>🤖 Machine Learning Insights</h3>
                    <div class="row">
                        <div class="col-md-4">
                            <p><strong>Qualità Dati:</strong> {self.insights['data_quality'].get('score', 0):.1f}/100</p>
                        </div>
                        <div class="col-md-4">
                            <p><strong>Dati Mancanti:</strong> {self.insights['data_quality'].get('missing_percentage', 0):.1f}%</p>
                        </div>
                        <div class="col-md-4">
                            <p><strong>Outlier:</strong> {len(self.insights.get('anomalies', []))} righe</p>
                        </div>
                    </div>
                </div>
                
                <!-- Tableau Recommendations -->
                <div class="chart-container">
                    <h3>📋 Come replicare in Tableau</h3>
        """
        
        for rec in self.insights.get('recommendations', [])[:5]:
            html_content += f"""
                    <div class="recommendation">
                        <strong>{rec.get('type', 'Info').upper()}:</strong> {rec.get('text', '')}<br>
                        <small>🎯 {rec.get('action', '')}</small>
                    </div>
            """
        
        html_content += f"""
                </div>
                
                <div class="footer">
                    <p>🤖 Generato da AI Data Engineer | Theme: {self.theme['name']} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def get_layout_css(self):
        """Restituisce CSS per il layout selezionato"""
        if self.layout_type == 'grid':
            return """
            .chart-container {
                display: inline-block;
                width: 48%;
                margin: 1%;
                vertical-align: top;
            }
            @media (max-width: 768px) {
                .chart-container { width: 98%; }
            }
            """
        elif self.layout_type == 'waterfall':
            return """
            .chart-container {
                width: 95%;
                margin: 20px auto;
            }
            """
        else:
            return """
            .chart-container {
                width: 100%;
                margin: 20px 0;
            }
            """
    
    def generate_kpi_cards(self):
        """Genera KPI cards"""
        kpi_html = ""
        metrics_to_show = self.numeric_cols[:min(4, len(self.numeric_cols))]
        
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
                            <small>Media</small>
                        </div>
                    </div>
                """
            except:
                continue
        
        if not kpi_html:
            kpi_html = '<div class="col-12"><p class="text-center">Nessuna metrica disponibile</p></div>'
        
        return kpi_html
