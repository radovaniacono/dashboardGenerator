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
        self.datetime_cols = ml_analyzer.datetime_cols if ml_analyzer else []
        
        # Palette pastello
        self.pastel_colors = [
            '#A8E6CF', '#FFD3B6', '#FFAAA5', '#FF8B94',
            '#B5EAD7', '#C7CEEA', '#E2F0CB', '#FFDAC1',
            '#B0E0E6', '#F7C6C6', '#C9E4DE', '#FDD0F2'
        ]
        
        # Seleziona tema pastello casuale
        self.theme = {
            'primary': random.choice(self.pastel_colors),
            'secondary': random.choice(self.pastel_colors),
            'background': '#F9FBF4',
            'card_bg': '#FFFFFF',
            'text': '#4A5B6E',
            'accent': '#FFB7B2'
        }
        
        # Seleziona layout a griglia fissa (non scrollabile)
        self.chart_types = self.select_charts_for_grid()
    
    def select_charts_for_grid(self):
        """Seleziona 4 grafici per layout 2x2 (non scrollabile)"""
        charts = []
        
        # Grafico 1: Istogramma (se ci sono dati numerici)
        if self.numeric_cols:
            charts.append('histogram')
        
        # Grafico 2: Bar chart categorie (se ci sono dati categorici)
        if self.categorical_cols:
            charts.append('barchart')
        elif len(self.numeric_cols) >= 2:
            charts.append('scatter')
        
        # Grafico 3: Time series (se ci sono date)
        if self.datetime_cols and self.numeric_cols:
            charts.append('timeseries')
        elif len(self.numeric_cols) > 1:
            charts.append('heatmap')
        
        # Grafico 4: Box plot o scatter
        if self.numeric_cols:
            charts.append('boxplot')
        elif self.categorical_cols:
            charts.append('pie')
        
        # Assicura almeno 4 grafici
        while len(charts) < 4:
            charts.append('histogram')
        
        return charts[:4]
    
    def create_histogram(self, index):
        col = random.choice(self.numeric_cols)
        data = self.df[col].dropna()
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data,
            nbinsx=min(20, int(np.sqrt(len(data)))),
            marker_color=self.pastel_colors[index % len(self.pastel_colors)],
            marker_line_color='white',
            marker_line_width=1,
            opacity=0.85
        ))
        fig.update_layout(
            title=f"📊 {col}",
            xaxis_title=col,
            yaxis_title="Conteggio",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme['text'], size=11)
        )
        return fig
    
    def create_barchart(self, index):
        col = random.choice(self.categorical_cols)
        value_counts = self.df[col].value_counts().head(8)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=value_counts.index,
            y=value_counts.values,
            marker_color=self.pastel_colors[index % len(self.pastel_colors)],
            text=value_counts.values,
            textposition='outside'
        ))
        fig.update_layout(
            title=f"📈 Top {col}",
            xaxis_title=col,
            yaxis_title="Conteggio",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme['text'], size=11)
        )
        return fig
    
    def create_scatter(self, index):
        col1, col2 = random.sample(self.numeric_cols, 2)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[col1],
            y=self.df[col2],
            mode='markers',
            marker=dict(
                size=8,
                color=self.pastel_colors[index % len(self.pastel_colors)],
                opacity=0.7
            )
        ))
        fig.update_layout(
            title=f"🔍 {col1} vs {col2}",
            xaxis_title=col1,
            yaxis_title=col2,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme['text'], size=11)
        )
        return fig
    
    def create_timeseries(self, index):
        date_col = self.datetime_cols[0]
        metric_col = random.choice(self.numeric_cols)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[date_col],
            y=self.df[metric_col],
            mode='lines+markers',
            line=dict(color=self.pastel_colors[index % len(self.pastel_colors)], width=2),
            marker=dict(size=4, color=self.pastel_colors[index % len(self.pastel_colors)]),
            fill='tozeroy',
            fillcolor=f'rgba({int(self.pastel_colors[index % len(self.pastel_colors)][1:3], 16)}, {int(self.pastel_colors[index % len(self.pastel_colors)][3:5], 16)}, {int(self.pastel_colors[index % len(self.pastel_colors)][5:7], 16)}, 0.2)'
        ))
        fig.update_layout(
            title=f"📅 {metric_col} nel tempo",
            xaxis_title=date_col,
            yaxis_title=metric_col,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme['text'], size=11)
        )
        return fig
    
    def create_heatmap(self, index):
        n_cols = min(len(self.numeric_cols), 5)
        selected_cols = random.sample(self.numeric_cols, n_cols)
        corr = self.df[selected_cols].corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='Pastel',
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 9}
        ))
        fig.update_layout(
            title="🔗 Correlazioni",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=80, r=20, t=50, b=50),
            font=dict(color=self.theme['text'], size=10)
        )
        return fig
    
    def create_boxplot(self, index):
        col = random.choice(self.numeric_cols)
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=self.df[col].dropna(),
            name=col,
            marker_color=self.pastel_colors[index % len(self.pastel_colors)],
            line_color=self.pastel_colors[index % len(self.pastel_colors)],
            boxmean='sd'
        ))
        fig.update_layout(
            title=f"📦 Distribuzione {col}",
            yaxis_title=col,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme['text'], size=11)
        )
        return fig
    
    def create_pie(self, index):
        col = random.choice(self.categorical_cols)
        value_counts = self.df[col].value_counts().head(6)
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,
            values=value_counts.values,
            hole=0.3,
            marker_colors=self.pastel_colors[:len(value_counts)],
            textinfo='label+percent',
            textposition='auto'
        )])
        fig.update_layout(
            title=f"🥧 {col}",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(color=self.theme['text'], size=11)
        )
        return fig
    
    def create_dashboard_html(self):
        """Dashboard NON scrollabile, layout 2x2 fisso"""
        
        # KPI cards
        kpi_html = self.generate_kpi_cards()
        
        # Genera 4 grafici
        charts_html = ""
        chart_functions = {
            'histogram': self.create_histogram,
            'barchart': self.create_barchart,
            'scatter': self.create_scatter,
            'timeseries': self.create_timeseries,
            'heatmap': self.create_heatmap,
            'boxplot': self.create_boxplot,
            'pie': self.create_pie
        }
        
        for idx, chart_type in enumerate(self.chart_types[:4]):
            try:
                if chart_type in chart_functions:
                    fig = chart_functions[chart_type](idx)
                    fig_json = json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder)
                    charts_html += f"""
                    <div class="chart-card">
                        <div id="chart_{idx}" style="width:100%; height:100%;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_{idx} = {fig_json};
                            Plotly.newPlot('chart_{idx}', fig_{idx}.data, fig_{idx}.layout, {{responsive: true}});
                        }})();
                    </script>
                    """
            except:
                pass
        
        # HTML completo con layout fisso 100vh
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pastel Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-3.0.1.min.js"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    background: {self.theme['background']};
                    font-family: 'Segoe UI', 'Inter', system-ui, -apple-system, sans-serif;
                    height: 100vh;
                    width: 100vw;
                    overflow: hidden;
                    padding: 16px;
                }}
                
                .dashboard {{
                    height: 100%;
                    width: 100%;
                    display: flex;
                    flex-direction: column;
                    gap: 16px;
                }}
                
                /* Header */
                .header {{
                    background: {self.theme['card_bg']};
                    border-radius: 24px;
                    padding: 16px 24px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
                }}
                .header h1 {{
                    font-size: 1.5rem;
                    color: {self.theme['text']};
                    font-weight: 600;
                }}
                .header h1 i {{
                    color: {self.theme['primary']};
                    margin-right: 10px;
                }}
                .badge {{
                    background: {self.theme['primary']}20;
                    padding: 8px 16px;
                    border-radius: 40px;
                    font-size: 0.8rem;
                    color: {self.theme['text']};
                }}
                
                /* KPI Row */
                .kpi-row {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 16px;
                    flex-shrink: 0;
                }}
                .kpi-card {{
                    background: {self.theme['card_bg']};
                    border-radius: 20px;
                    padding: 16px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                    transition: transform 0.2s;
                    border: 1px solid {self.theme['primary']}30;
                }}
                .kpi-card:hover {{
                    transform: translateY(-2px);
                }}
                .kpi-label {{
                    font-size: 0.75rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: {self.theme['text']}aa;
                    margin-bottom: 8px;
                }}
                .kpi-value {{
                    font-size: 2rem;
                    font-weight: 700;
                    color: {self.theme['text']};
                }}
                .kpi-icon {{
                    font-size: 1.8rem;
                    color: {self.theme['primary']};
                    opacity: 0.7;
                }}
                
                /* Grid grafici 2x2 - occupa tutto lo spazio rimanente */
                .charts-grid {{
                    flex: 1;
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    grid-template-rows: 1fr 1fr;
                    gap: 16px;
                    min-height: 0;
                }}
                .chart-card {{
                    background: {self.theme['card_bg']};
                    border-radius: 24px;
                    padding: 16px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    border: 1px solid rgba(0,0,0,0.03);
                }}
                
                /* Footer */
                .footer {{
                    flex-shrink: 0;
                    text-align: center;
                    padding: 8px;
                    font-size: 0.7rem;
                    color: {self.theme['text']}aa;
                }}
                
                /* Responsive */
                @media (max-width: 1024px) {{
                    .kpi-value {{ font-size: 1.5rem; }}
                    .header h1 {{ font-size: 1.2rem; }}
                }}
                @media (max-width: 768px) {{
                    .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
                    .charts-grid {{ grid-template-columns: 1fr; grid-template-rows: auto; overflow-y: auto; }}
                    body {{ overflow-y: auto; height: auto; }}
                    .dashboard {{ height: auto; }}
                }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <!-- Header -->
                <div class="header">
                    <h1><i class="fas fa-chalkboard-user"></i> Pastel Dashboard</h1>
                    <div class="badge">
                        <i class="fas fa-chart-line"></i> AI Analytics • {datetime.now().strftime('%d/%m/%Y')}
                    </div>
                </div>
                
                <!-- KPI Row -->
                <div class="kpi-row">
                    {kpi_html}
                </div>
                
                <!-- Charts Grid 2x2 (NO SCROLL) -->
                <div class="charts-grid">
                    {charts_html}
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <i class="fas fa-robot"></i> Generato con IA • Design pastello • Layout fisso senza scroll
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def generate_kpi_cards(self):
        """Genera 4 KPI cards con icone"""
        icons = ['💰', '📊', '🎯', '⚡', '📦', '👥', '💹', '📈']
        kpi_html = ""
        
        metrics = self.numeric_cols[:4] if len(self.numeric_cols) >= 4 else self.numeric_cols
        while len(metrics) < 4:
            metrics.append(self.numeric_cols[0] if self.numeric_cols else "Dati")
        
        for i, col in enumerate(metrics[:4]):
            try:
                if col in self.numeric_cols:
                    value = self.df[col].mean()
                    if pd.isna(value):
                        value = 0
                    val_display = f"{value:,.0f}" if abs(value) > 1000 else f"{value:,.2f}"
                else:
                    val_display = str(self.df[col].nunique()) if col in self.categorical_cols else "—"
                
                kpi_html += f"""
                <div class="kpi-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="kpi-label">{col.upper()}</div>
                            <div class="kpi-value">{val_display}</div>
                        </div>
                        <div class="kpi-icon">{icons[i % len(icons)]}</div>
                    </div>
                </div>
                """
            except:
                continue
        
        if not kpi_html:
            kpi_html = '<div class="kpi-card">Nessun dato</div>' * 4
        
        return kpi_html
