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
        
    def get_tableau_style(self):
        """Restituisce lo stile Tableau per i grafici"""
        return {
            'template': 'plotly_white',
            'font_family': 'Tableau, "Tableau", "Helvetica Neue", Arial, sans-serif',
            'title_font_size': 14,
            'title_font_color': '#4a4a4a',
            'axis_title_font_size': 11,
            'axis_title_color': '#666666',
            'tick_font_size': 10,
            'tick_color': '#888888',
            'grid_color': '#e6e6e6',
            'background_color': '#ffffff',
            'colors': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        }
    
    def create_tableau_histogram(self, column):
        """Crea istogramma in stile Tableau"""
        style = self.get_tableau_style()
        
        # Calcola bin size ottimale (stile Tableau)
        data = self.df[column].dropna()
        n_bins = min(20, int(np.sqrt(len(data))))
        
        fig = go.Figure()
        
        # Aggiungi istogramma
        fig.add_trace(go.Histogram(
            x=data,
            nbinsx=n_bins,
            marker_color=style['colors'][0],
            marker_line_color='white',
            marker_line_width=1,
            opacity=0.85,
            name=column
        ))
        
        # Stile Tableau
        fig.update_layout(
            title={
                'text': f'Distribuzione {column}',
                'font': {'size': style['title_font_size'], 'color': style['title_font_color']},
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title={
                'text': column,
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            yaxis_title={
                'text': 'Conteggio',
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            plot_bgcolor=style['background_color'],
            paper_bgcolor=style['background_color'],
            xaxis=dict(
                showgrid=True,
                gridcolor=style['grid_color'],
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color'],
                linewidth=1
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=style['grid_color'],
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color'],
                linewidth=1
            ),
            margin=dict(l=60, r=60, t=60, b=60),
            bargap=0.1,
            font_family=style['font_family']
        )
        
        return fig
    
    def create_tableau_bar_chart(self, column):
        """Crea bar chart in stile Tableau"""
        style = self.get_tableau_style()
        
        # Top 10 categorie
        value_counts = self.df[column].value_counts().head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=value_counts.values,
            y=value_counts.index,
            orientation='h',
            marker_color=style['colors'][1],
            marker_line_color='white',
            marker_line_width=1,
            text=value_counts.values,
            textposition='outside',
            textfont=dict(size=10, color='#333333')
        ))
        
        fig.update_layout(
            title={
                'text': f'Top 10 {column}',
                'font': {'size': style['title_font_size'], 'color': style['title_font_color']},
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title={
                'text': 'Conteggio',
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            yaxis_title={
                'text': column,
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            plot_bgcolor=style['background_color'],
            paper_bgcolor=style['background_color'],
            xaxis=dict(
                showgrid=True,
                gridcolor=style['grid_color'],
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color']
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color'],
                categoryorder='total ascending'
            ),
            margin=dict(l=120, r=60, t=60, b=60),
            font_family=style['font_family'],
            height=400
        )
        
        return fig
    
    def create_tableau_scatter(self, x_col, y_col):
        """Crea scatter plot in stile Tableau"""
        style = self.get_tableau_style()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[x_col],
            y=self.df[y_col],
            mode='markers',
            marker=dict(
                size=8,
                color=style['colors'][2],
                opacity=0.6,
                line=dict(width=1, color='white')
            ),
            name='Dati'
        ))
        
        # Aggiungi linea di tendenza
        z = np.polyfit(self.df[x_col].dropna(), self.df[y_col].dropna(), 1)
        p = np.poly1d(z)
        x_trend = np.linspace(self.df[x_col].min(), self.df[x_col].max(), 100)
        
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode='lines',
            line=dict(color='red', width=2, dash='dash'),
            name='Linea di tendenza'
        ))
        
        fig.update_layout(
            title={
                'text': f'Relazione {x_col} vs {y_col}',
                'font': {'size': style['title_font_size'], 'color': style['title_font_color']},
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title={
                'text': x_col,
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            yaxis_title={
                'text': y_col,
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            plot_bgcolor=style['background_color'],
            paper_bgcolor=style['background_color'],
            xaxis=dict(
                showgrid=True,
                gridcolor=style['grid_color'],
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color']
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=style['grid_color'],
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color']
            ),
            margin=dict(l=60, r=60, t=60, b=60),
            font_family=style['font_family']
        )
        
        return fig
    
    def create_tableau_time_series(self, date_col, metric_col):
        """Crea serie temporale in stile Tableau"""
        style = self.get_tableau_style()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[date_col],
            y=self.df[metric_col],
            mode='lines+markers',
            line=dict(color=style['colors'][0], width=2),
            marker=dict(size=4, color=style['colors'][0]),
            name=metric_col,
            fill='tozeroy',
            fillcolor=f'rgba({int(style["colors"][0][1:3], 16)}, {int(style["colors"][0][3:5], 16)}, {int(style["colors"][0][5:7], 16)}, 0.1)'
        ))
        
        fig.update_layout(
            title={
                'text': f'Trend {metric_col} nel tempo',
                'font': {'size': style['title_font_size'], 'color': style['title_font_color']},
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title={
                'text': date_col,
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            yaxis_title={
                'text': metric_col,
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            plot_bgcolor=style['background_color'],
            paper_bgcolor=style['background_color'],
            xaxis=dict(
                showgrid=True,
                gridcolor=style['grid_color'],
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color']
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=style['grid_color'],
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color']
            ),
            margin=dict(l=60, r=60, t=60, b=60),
            hovermode='x unified',
            font_family=style['font_family']
        )
        
        return fig
    
    def create_tableau_boxplot(self, column):
        """Crea box plot in stile Tableau"""
        style = self.get_tableau_style()
        
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=self.df[column].dropna(),
            name=column,
            boxmean='sd',
            marker_color=style['colors'][3],
            line=dict(color=style['colors'][3], width=1),
            fillcolor=f'rgba({int(style["colors"][3][1:3], 16)}, {int(style["colors"][3][3:5], 16)}, {int(style["colors"][3][5:7], 16)}, 0.3)'
        ))
        
        fig.update_layout(
            title={
                'text': f'Distribuzione {column} (Box Plot)',
                'font': {'size': style['title_font_size'], 'color': style['title_font_color']},
                'x': 0.5,
                'xanchor': 'center'
            },
            yaxis_title={
                'text': column,
                'font': {'size': style['axis_title_font_size'], 'color': style['axis_title_color']}
            },
            plot_bgcolor=style['background_color'],
            paper_bgcolor=style['background_color'],
            yaxis=dict(
                showgrid=True,
                gridcolor=style['grid_color'],
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color']),
                showline=True,
                linecolor=style['grid_color'],
                zeroline=True,
                zerolinecolor=style['grid_color']
            ),
            xaxis=dict(
                showticklabels=True,
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color'])
            ),
            margin=dict(l=60, r=60, t=60, b=60),
            font_family=style['font_family']
        )
        
        return fig
    
    def create_tableau_heatmap(self):
        """Crea heatmap delle correlazioni in stile Tableau"""
        style = self.get_tableau_style()
        
        corr = self.df[self.numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title={
                'text': 'Matrice di Correlazione',
                'font': {'size': style['title_font_size'], 'color': style['title_font_color']},
                'x': 0.5,
                'xanchor': 'center'
            },
            plot_bgcolor=style['background_color'],
            paper_bgcolor=style['background_color'],
            xaxis=dict(
                tickangle=45,
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color'])
            ),
            yaxis=dict(
                tickfont=dict(size=style['tick_font_size'], color=style['tick_color'])
            ),
            margin=dict(l=100, r=60, t=60, b=100),
            font_family=style['font_family'],
            width=600,
            height=500
        )
        
        return fig
    
    def create_dashboard_html(self):
        """Crea dashboard HTML con grafici stile Tableau"""
        
        # Genera KPI cards
        kpi_html = self.generate_kpi_cards()
        
        # Genera grafici
        charts_html = ""
        
        # 1. Istogrammi per le prime 3 metriche numeriche (stile Tableau)
        for i, col in enumerate(self.numeric_cols[:3]):
            try:
                fig = self.create_tableau_histogram(col)
                fig_json = json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <div id="hist_{i}" style="width:100%; height:450px;"></div>
                </div>
                <script>
                    var hist_{i} = {fig_json};
                    Plotly.newPlot('hist_{i}', hist_{i}.data, hist_{i}.layout);
                </script>
                """
            except Exception as e:
                charts_html += f"<p>Errore nel grafico per {col}: {str(e)}</p>"
        
        # 2. Box plot per la prima metrica
        if self.numeric_cols:
            try:
                fig_box = self.create_tableau_boxplot(self.numeric_cols[0])
                fig_box_json = json.dumps(fig_box.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <div id="box_plot" style="width:100%; height:450px;"></div>
                </div>
                <script>
                    var box_plot = {fig_box_json};
                    Plotly.newPlot('box_plot', box_plot.data, box_plot.layout);
                </script>
                """
            except:
                pass
        
        # 3. Bar chart per categorie (stile Tableau)
        if self.categorical_cols:
            try:
                fig_bar = self.create_tableau_bar_chart(self.categorical_cols[0])
                fig_bar_json = json.dumps(fig_bar.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <div id="bar_chart" style="width:100%; height:450px;"></div>
                </div>
                <script>
                    var bar_chart = {fig_bar_json};
                    Plotly.newPlot('bar_chart', bar_chart.data, bar_chart.layout);
                </script>
                """
            except:
                pass
        
        # 4. Scatter plot
        if len(self.numeric_cols) >= 2:
            try:
                fig_scatter = self.create_tableau_scatter(self.numeric_cols[0], self.numeric_cols[1])
                fig_scatter_json = json.dumps(fig_scatter.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <div id="scatter_plot" style="width:100%; height:450px;"></div>
                </div>
                <script>
                    var scatter_plot = {fig_scatter_json};
                    Plotly.newPlot('scatter_plot', scatter_plot.data, scatter_plot.layout);
                </script>
                """
            except:
                pass
        
        # 5. Time series
        if self.ml_analyzer and self.ml_analyzer.datetime_cols and self.numeric_cols:
            try:
                date_col = self.ml_analyzer.datetime_cols[0]
                fig_line = self.create_tableau_time_series(date_col, self.numeric_cols[0])
                fig_line_json = json.dumps(fig_line.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <div id="line_chart" style="width:100%; height:450px;"></div>
                </div>
                <script>
                    var line_chart = {fig_line_json};
                    Plotly.newPlot('line_chart', line_chart.data, line_chart.layout);
                </script>
                """
            except:
                pass
        
        # 6. Heatmap correlazioni
        if len(self.numeric_cols) > 1:
            try:
                fig_heatmap = self.create_tableau_heatmap()
                fig_heatmap_json = json.dumps(fig_heatmap.to_dict(), cls=PlotlyJSONEncoder)
                charts_html += f"""
                <div class="chart-container">
                    <div id="heatmap" style="width:100%; height:550px;"></div>
                </div>
                <script>
                    var heatmap = {fig_heatmap_json};
                    Plotly.newPlot('heatmap', heatmap.data, heatmap.layout);
                </script>
                """
            except:
                pass
        
        # HTML completo con istruzioni per Tableau
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tableau Style Dashboard - {datetime.now().strftime('%Y-%m-%d')}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ 
                    background: #f5f5f5; 
                    font-family: 'Tableau', 'Helvetica Neue', Arial, sans-serif; 
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
                    padding: 15px; 
                    margin: 20px 0; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .insight-box {{ 
                    background: white;
                    border-left: 4px solid #1f77b4;
                    padding: 20px; 
                    margin: 20px 0; 
                    border-radius: 4px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                }}
                h1, h2, h3, h4 {{ 
                    color: #333; 
                    margin-bottom: 20px;
                    font-weight: 500;
                }}
                .recommendation {{ 
                    background: #f9f9f9; 
                    border-left: 4px solid #1f77b4; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 4px;
                }}
                .tableau-note {{
                    background: #f0f7ff;
                    border: 1px solid #cce5ff;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 4px;
                    font-size: 0.9em;
                }}
                .copy-btn {{
                    background: #1f77b4;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 0.8em;
                }}
                .copy-btn:hover {{
                    background: #155a8a;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="container-fluid">
                    <h1 class="text-center mb-4">📊 Tableau Style Dashboard</h1>
                    <p class="text-center text-muted mb-5">Grafici in stile Tableau - Pronti per essere replicati</p>
                    
                    <!-- KPI Section -->
                    <div class="row">
                        {kpi_html}
                    </div>
                    
                    <!-- Istruzioni per Tableau -->
                    <div class="tableau-note">
                        <strong>📌 Come replicare questo grafico in Tableau:</strong><br>
                        1. Seleziona il tipo di grafico desiderato dalla toolbar<br>
                        2. Trascina le misure sugli assi corrispondenti<br>
                        3. Applica lo stile "Tableau Default"<br>
                        4. Personalizza colori e formati dal pannello "Marks"
                    </div>
                    
                    <!-- Charts Section -->
                    {charts_html}
                    
                    <!-- Insights e Raccomandazioni Tableau -->
                    <div class="chart-container">
                        <h4>📋 Come creare questa dashboard in Tableau</h4>
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
                    
                    <!-- Tips Tableau -->
                    <div class="chart-container">
                        <h4>💡 Tips per replicare i grafici in Tableau</h4>
                        <ul>
                            <li><strong>Istogrammi:</strong> Trascina la misura su Colonne, crea bin (Crea → Bin) e poi trascina il conteggio su Righe</li>
                            <li><strong>Box Plot:</strong> Usa "Analytics" → "Box Plot" o trascina la misura su Righe e la dimensione su Dettaglio</li>
                            <li><strong>Scatter Plot:</strong> Trascina una misura su Colonne, l'altra su Righe, aggiungi linea di tendenza da Analytics</li>
                            <li><strong>Bar Chart orizzontale:</strong> Trascina la dimensione su Righe, la misura su Colonne, poi scambia assi</li>
                            <li><strong>Time Series:</strong> Trascina la data su Colonne (scegli livello di dettaglio), la misura su Righe</li>
                        </ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def generate_kpi_cards(self):
        """Genera KPI cards in stile Tableau"""
        kpi_html = ""
        
        metrics_to_show = self.numeric_cols[:4] if len(self.numeric_cols) >= 4 else self.numeric_cols
        
        for col in metrics_to_show:
            try:
                avg_val = self.df[col].mean()
                if pd.isna(avg_val):
                    avg_val = 0
                
                min_val = self.df[col].min()
                max_val = self.df[col].max()
                
                kpi_html += f"""
                    <div class="col-md-3">
                        <div class="kpi-card">
                            <div class="kpi-label">{col.upper()}</div>
                            <div class="kpi-value">{avg_val:,.2f}</div>
                            <small>Min: {min_val:,.2f} | Max: {max_val:,.2f}</small>
                        </div>
                    </div>
                """
            except Exception as e:
                continue
        
        if not kpi_html:
            kpi_html = '<div class="col-12"><p class="text-center">Nessuna metrica numerica disponibile</p></div>'
        
        return kpi_html
