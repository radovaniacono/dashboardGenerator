import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import pandas as pd
import numpy as np
from datetime import datetime
import random
from itertools import cycle

class DashboardGenerator:
    def __init__(self, df, ml_analyzer, insights):
        self.df = df
        self.ml_analyzer = ml_analyzer
        self.insights = insights
        self.numeric_cols = ml_analyzer.numeric_cols if ml_analyzer else []
        self.categorical_cols = ml_analyzer.categorical_cols if ml_analyzer else []
        
        # Inizializza seed per randomizzazione riproducibile (basato sul file)
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
            },
            {
                'name': 'Pastel Dream',
                'primary': '#a8e6cf',
                'secondary': '#ffd3b6',
                'tertiary': '#ffaaa5',
                'background': '#fdfbf7',
                'card_bg': '#ffffff',
                'text': '#5a4a4a',
                'grid': '#f0e5de'
            },
            {
                'name': 'Bold Contrast',
                'primary': '#e63946',
                'secondary': '#f4a261',
                'tertiary': '#e9c46a',
                'background': '#2b2d42',
                'card_bg': '#3d405b',
                'text': '#edf2f4',
                'grid': '#5c677d'
            }
        ]
        return random.choice(themes)
    
    def select_random_charts(self):
        """Seleziona casualmente quali tipi di grafici generare"""
        available_charts = []
        
        # Lista di tutti i possibili grafici
        all_charts = ['histogram', 'boxplot', 'barchart', 'scatter', 'timeseries', 
                     'heatmap', 'violin', 'density', 'pie', 'radar', 'treemap', 
                     'sunburst', 'parallel', '3d_scatter', 'bubble']
        
        # Seleziona 4-7 grafici casuali
        num_charts = random.randint(4, 7)
        selected = random.sample(all_charts, min(num_charts, len(all_charts)))
        
        # Assicura che alcuni grafici siano compatibili con i dati
        compatible_charts = []
        
        if self.numeric_cols:
            chart_options = ['histogram', 'boxplot', 'violin', 'density']
            if random.choice([True, False]):
                compatible_charts.append(random.choice(chart_options))
        
        if self.categorical_cols and self.numeric_cols:
            chart_options = ['barchart', 'pie', 'treemap']
            if random.choice([True, False]):
                compatible_charts.append(random.choice(chart_options))
        
        if len(self.numeric_cols) >= 2:
            chart_options = ['scatter', 'bubble', 'radar']
            if random.choice([True, False]):
                compatible_charts.append(random.choice(chart_options))
        
        if self.ml_analyzer and self.ml_analyzer.datetime_cols and self.numeric_cols:
            if random.choice([True, False]) and 'timeseries' in selected:
                compatible_charts.append('timeseries')
        
        if len(self.numeric_cols) > 1:
            if random.choice([True, False]) and 'heatmap' in selected:
                compatible_charts.append('heatmap')
        
        # Unisci e rimuovi duplicati
        final_charts = list(set(selected + compatible_charts))
        
        # Limita a max 7 grafici
        return final_charts[:7]
    
    def create_random_chart(self, chart_type, index):
        """Crea un grafico del tipo specificato con variazioni casuali"""
        chart_functions = {
            'histogram': self.create_histogram_variant,
            'boxplot': self.create_boxplot_variant,
            'barchart': self.create_barchart_variant,
            'scatter': self.create_scatter_variant,
            'timeseries': self.create_timeseries_variant,
            'heatmap': self.create_heatmap_variant,
            'violin': self.create_violin_plot,
            'density': self.create_density_plot,
            'pie': self.create_pie_chart,
            'radar': self.create_radar_chart,
            'treemap': self.create_treemap,
            'bubble': self.create_bubble_chart,
            'parallel': self.create_parallel_coordinates,
            '3d_scatter': self.create_3d_scatter
        }
        
        if chart_type in chart_functions:
            try:
                return chart_functions[chart_type](index)
            except:
                return None
        return None
    
    def create_histogram_variant(self, index):
        """Istogramma con variazioni casuali"""
        col = random.choice(self.numeric_cols)
        data = self.df[col].dropna()
        
        # Variazioni casuali
        color = random.choice([self.theme['primary'], self.theme['secondary'], self.theme['tertiary']])
        nbins = random.randint(10, 40)
        orientation = random.choice(['v', 'h'])
        
        fig = go.Figure()
        
        if orientation == 'v':
            fig.add_trace(go.Histogram(
                x=data,
                nbinsx=nbins,
                marker_color=color,
                marker_line_color='white',
                marker_line_width=1,
                opacity=random.uniform(0.6, 0.9)
            ))
            x_title, y_title = col, "Frequenza"
        else:
            fig.add_trace(go.Histogram(
                y=data,
                nbinsy=nbins,
                marker_color=color,
                marker_line_color='white',
                marker_line_width=1,
                opacity=random.uniform(0.6, 0.9),
                orientation='h'
            ))
            x_title, y_title = "Frequenza", col
        
        fig.update_layout(
            title=f"Distribuzione {col}",
            xaxis_title=x_title,
            yaxis_title=y_title,
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_boxplot_variant(self, index):
        """Box plot con variazioni"""
        col = random.choice(self.numeric_cols)
        
        # Variazioni casuali
        show_mean = random.choice([True, False])
        color = random.choice([self.theme['primary'], self.theme['secondary']])
        
        fig = go.Figure()
        
        trace_kwargs = {
            'y': self.df[col].dropna(),
            'name': col,
            'marker_color': color,
            'line_color': color
        }
        
        if show_mean:
            trace_kwargs['boxmean'] = 'sd'
        
        fig.add_trace(go.Box(**trace_kwargs))
        
        fig.update_layout(
            title=f"Distribuzione {col}",
            yaxis_title=col,
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_barchart_variant(self, index):
        """Bar chart con variazioni"""
        col = random.choice(self.categorical_cols)
        value_counts = self.df[col].value_counts().head(random.randint(5, 15))
        
        # Variazioni casuali
        orientation = random.choice(['v', 'h'])
        colorscale = random.choice(['Viridis', 'Plasma', 'Cividis', self.theme['primary']])
        
        fig = go.Figure()
        
        if orientation == 'v':
            fig.add_trace(go.Bar(
                x=value_counts.index,
                y=value_counts.values,
                marker_color=value_counts.values,
                marker_colorscale=colorscale if colorscale in ['Viridis', 'Plasma', 'Cividis'] else None,
                marker_color_continuous_scale=colorscale if colorscale in ['Viridis', 'Plasma', 'Cividis'] else None,
                marker_color=self.theme['primary'] if colorscale not in ['Viridis', 'Plasma', 'Cividis'] else None,
                text=value_counts.values,
                textposition='outside'
            ))
        else:
            fig.add_trace(go.Bar(
                y=value_counts.index,
                x=value_counts.values,
                orientation='h',
                marker_color=value_counts.values,
                marker_colorscale=colorscale if colorscale in ['Viridis', 'Plasma', 'Cividis'] else None,
                text=value_counts.values,
                textposition='outside'
            ))
        
        fig.update_layout(
            title=f"Top {len(value_counts)} {col}",
            xaxis_title="Conteggio" if orientation == 'h' else col,
            yaxis_title=col if orientation == 'h' else "Conteggio",
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=100 if orientation == 'h' else 50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_scatter_variant(self, index):
        """Scatter plot con variazioni"""
        col1, col2 = random.sample(self.numeric_cols, 2)
        data = self.df[[col1, col2]].dropna()
        
        # Variazioni casuali
        add_trendline = random.choice([True, False])
        marker_size = random.randint(5, 15)
        opacity = random.uniform(0.4, 0.8)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data[col1],
            y=data[col2],
            mode='markers',
            marker=dict(
                size=marker_size,
                color=self.theme['primary'],
                opacity=opacity,
                line=dict(width=1, color='white') if random.choice([True, False]) else None
            ),
            name='Dati'
        ))
        
        if add_trendline and len(data) > 2:
            z = np.polyfit(data[col1], data[col2], 1)
            p = np.poly1d(z)
            x_trend = np.linspace(data[col1].min(), data[col1].max(), 50)
            fig.add_trace(go.Scatter(
                x=x_trend,
                y=p(x_trend),
                mode='lines',
                line=dict(color='red', width=2, dash='dash'),
                name='Trend'
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
        
        return fig.to_dict()
    
    def create_timeseries_variant(self, index):
        """Time series con variazioni"""
        date_col = random.choice(self.ml_analyzer.datetime_cols)
        metric_col = random.choice(self.numeric_cols)
        
        data = self.df[[date_col, metric_col]].dropna()
        
        # Variazioni casuali
        fill_area = random.choice([True, False])
        marker_style = random.choice(['lines', 'lines+markers', 'markers'])
        line_width = random.randint(1, 3)
        
        fig = go.Figure()
        
        trace_kwargs = {
            'x': data[date_col],
            'y': data[metric_col],
            'mode': marker_style,
            'line': dict(color=self.theme['primary'], width=line_width),
            'name': metric_col
        }
        
        if marker_style != 'lines':
            trace_kwargs['marker'] = dict(size=random.randint(3, 6), color=self.theme['primary'])
        
        if fill_area:
            trace_kwargs['fill'] = 'tozeroy'
            trace_kwargs['fillcolor'] = f'rgba(31, 119, 180, 0.2)'
        
        fig.add_trace(go.Scatter(**trace_kwargs))
        
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
        
        return fig.to_dict()
    
    def create_heatmap_variant(self, index):
        """Heatmap con variazioni"""
        # Seleziona un sottoinsieme di colonne
        n_cols = min(len(self.numeric_cols), random.randint(3, 8))
        selected_cols = random.sample(self.numeric_cols, n_cols)
        
        corr = self.df[selected_cols].corr()
        
        # Variazioni casuali
        colorscale = random.choice(['RdBu', 'Viridis', 'Plasma', 'Cividis', 'Hot'])
        
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale=colorscale,
            zmid=0 if colorscale == 'RdBu' else None,
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
        
        return fig.to_dict()
    
    def create_violin_plot(self, index):
        """Violin plot (alternativa al boxplot)"""
        col = random.choice(self.numeric_cols)
        
        fig = go.Figure()
        fig.add_trace(go.Violin(
            y=self.df[col].dropna(),
            name=col,
            box_visible=True,
            meanline_visible=True,
            fillcolor=self.theme['primary'],
            line_color=self.theme['secondary']
        ))
        
        fig.update_layout(
            title=f"Distribuzione {col} (Violin Plot)",
            yaxis_title=col,
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_density_plot(self, index):
        """Density plot"""
        col = random.choice(self.numeric_cols)
        
        fig = go.Figure()
        fig.add_trace(go.Histogram2dContour(
            x=self.df[col],
            y=self.df[col],
            colorscale='Viridis',
            contours=dict(coloring='fill')
        ))
        
        fig.update_layout(
            title=f"Densità {col}",
            xaxis_title=col,
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_pie_chart(self, index):
        """Pie chart"""
        col = random.choice(self.categorical_cols)
        value_counts = self.df[col].value_counts().head(8)
        
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,
            values=value_counts.values,
            hole=random.choice([0, 0.3, 0.5]),
            marker_colors=[self.theme['primary'], self.theme['secondary'], self.theme['tertiary']],
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title=f"Distribuzione {col}",
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_radar_chart(self, index):
        """Radar chart"""
        # Prendi le medie delle prime 4-6 metriche
        n_metrics = min(len(self.numeric_cols), random.randint(4, 6))
        selected_metrics = random.sample(self.numeric_cols, n_metrics)
        averages = [self.df[col].mean() for col in selected_metrics]
        
        # Normalizza
        max_vals = [self.df[col].max() for col in selected_metrics]
        normalized = [avg/maxv if maxv > 0 else 0 for avg, maxv in zip(averages, max_vals)]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=normalized,
            theta=selected_metrics,
            fill='toself',
            marker=dict(color=self.theme['primary']),
            line=dict(color=self.theme['secondary'], width=2)
        ))
        
        fig.update_layout(
            title="Radar Chart - Medie Normalizzate",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=450,
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_treemap(self, index):
        """Treemap"""
        if not self.categorical_cols or not self.numeric_cols:
            return None
        
        col_cat = random.choice(self.categorical_cols)
        col_val = random.choice(self.numeric_cols)
        
        # Aggrega per categoria
        aggregated = self.df.groupby(col_cat)[col_val].sum().head(15)
        
        fig = go.Figure(go.Treemap(
            labels=aggregated.index,
            parents=[""] * len(aggregated),
            values=aggregated.values,
            marker_colors=aggregated.values,
            marker_colorscale='Viridis',
            textinfo="label+value+percent root"
        ))
        
        fig.update_layout(
            title=f"Treemap: {col_val} per {col_cat}",
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=450,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_bubble_chart(self, index):
        """Bubble chart (scatter con dimensione)"""
        if len(self.numeric_cols) < 3:
            return None
        
        x_col, y_col, size_col = random.sample(self.numeric_cols, 3)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[x_col],
            y=self.df[y_col],
            mode='markers',
            marker=dict(
                size=self.df[size_col] / self.df[size_col].max() * 50,
                color=self.theme['primary'],
                opacity=0.6,
                sizemode='area',
                sizeref=2.*max(self.df[size_col])/(50**2)
            ),
            text=self.df.index,
            hovertemplate=f'<b>{x_col}</b>: %{{x}}<br><b>{y_col}</b>: %{{y}}<br><b>{size_col}</b>: %{{marker.size}}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Bubble Chart: {x_col} vs {y_col} (dimensione={size_col})",
            xaxis_title=x_col,
            yaxis_title=y_col,
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=450,
            margin=dict(l=50, r=30, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_parallel_coordinates(self, index):
        """Coordinate parallele"""
        if len(self.numeric_cols) < 3:
            return None
        
        # Seleziona 4-6 colonne
        n_cols = min(len(self.numeric_cols), random.randint(4, 6))
        selected_cols = random.sample(self.numeric_cols, n_cols)
        
        # Normalizza i dati
        data_norm = self.df[selected_cols].copy()
        for col in selected_cols:
            min_val = data_norm[col].min()
            max_val = data_norm[col].max()
            if max_val > min_val:
                data_norm[col] = (data_norm[col] - min_val) / (max_val - min_val)
        
        fig = go.Figure(data=go.Parcoords(
            line=dict(color=self.df[selected_cols[0]].values,
                      colorscale='Viridis',
                      showscale=True),
            dimensions=[dict(label=col, values=data_norm[col].values) for col in selected_cols]
        ))
        
        fig.update_layout(
            title="Parallel Coordinates Plot",
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=500,
            margin=dict(l=80, r=80, t=50, b=50),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_3d_scatter(self, index):
        """Scatter plot 3D"""
        if len(self.numeric_cols) < 3:
            return None
        
        x_col, y_col, z_col = random.sample(self.numeric_cols, 3)
        
        fig = go.Figure(data=[go.Scatter3d(
            x=self.df[x_col],
            y=self.df[y_col],
            z=self.df[z_col],
            mode='markers',
            marker=dict(
                size=5,
                color=self.df[z_col],
                colorscale='Viridis',
                opacity=0.8
            )
        )])
        
        fig.update_layout(
            title=f"3D Scatter: {x_col}, {y_col}, {z_col}",
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col
            ),
            plot_bgcolor=self.theme['background'],
            paper_bgcolor=self.theme['card_bg'],
            height=500,
            margin=dict(l=0, r=0, t=50, b=0),
            font=dict(color=self.theme['text'])
        )
        
        return fig.to_dict()
    
    def create_dashboard_html(self):
        """Crea dashboard HTML con layout e grafici randomizzati"""
        
        # Genera KPI cards
        kpi_html = self.generate_kpi_cards()
        
        # Genera grafici randomizzati
        charts_html = ""
        
        for idx, chart_type in enumerate(self.chart_types):
            try:
                fig_dict = self.create_random_chart(chart_type, idx)
                if fig_dict:
                    fig_json = json.dumps(fig_dict, cls=PlotlyJSONEncoder)
                    charts_html += f"""
                    <div class="chart-container" style="background: {self.theme['card_bg']};">
                        <div id="chart_{idx}_{chart_type}" style="width:100%; height:450px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_{idx} = {fig_json};
                            Plotly.newPlot('chart_{idx}_{chart_type}', fig_{idx}.data, fig_{idx}.layout);
                        }})();
                    </script>
                    """
            except Exception as e:
                charts_html += f"<div class='alert alert-warning'>Errore nel grafico {chart_type}: {str(e)}</div>"
        
        # Layout responsive con griglia casuale
        layout_style = self.get_layout_style()
        
        # HTML completo
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dynamic Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
            <script src="https://cdn.plot.ly/plotly-3.0.1.min.js" charset="utf-8"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ 
                    background: {self.theme['background']}; 
                    font-family: {random.choice(['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto'])}, Arial, sans-serif;
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
                .dashboard-header p {{
                    font-size: 1.1em;
                    opacity: 0.9;
                }}
                .kpi-card {{ 
                    background: {self.theme['card_bg']}; 
                    border-radius: {random.randint(8, 15)}px; 
                    padding: 20px; 
                    margin: 10px; 
                    box-shadow: 0 {random.randint(2, 5)}px {random.randint(10, 20)}px rgba(0,0,0,0.1); 
                    text-align: center;
                    border-top: 4px solid {self.theme['primary']};
                    transition: transform 0.3s;
                }}
                .kpi-card:hover {{
                    transform: translateY(-5px);
                }}
                .kpi-value {{ 
                    font-size: 2.2em; 
                    font-weight: bold; 
                    color: {self.theme['primary']}; 
                }}
                .kpi-label {{ 
                    color: {self.theme['text']}; 
                    font-size: 0.85em; 
                    text-transform: uppercase; 
                    letter-spacing: 1px;
                    font-weight: 600;
                    opacity: 0.8;
                }}
                .chart-container {{ 
                    background: {self.theme['card_bg']}; 
                    border-radius: {random.randint(8, 15)}px; 
                    padding: 20px; 
                    margin: 20px 0; 
                    box-shadow: 0 {random.randint(2, 5)}px {random.randint(8, 15)}px rgba(0,0,0,0.1);
                    transition: all 0.3s;
                }}
                .chart-container:hover {{
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                }}
                .insight-box {{ 
                    background: {self.theme['card_bg']};
                    border-left: 4px solid {self.theme['primary']};
                    padding: 20px; 
                    margin: 20px 0; 
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }}
                .recommendation {{ 
                    background: {self.theme['background']}; 
                    border-left: 4px solid {self.theme['secondary']}; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 8px;
                }}
                .recommendation strong {{
                    color: {self.theme['primary']};
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    margin-top: 40px;
                    color: {self.theme['text']};
                    opacity: 0.7;
                    font-size: 0.9em;
                }}
                {layout_style}
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h1>🎲 Dynamic ML Dashboard</h1>
                    <p>Theme: {self.theme['name']} | Layout: {self.layout_type} | Charts: {len(self.chart_types)}</p>
                    <small>✨ Dashboard generata automaticamente - Ogni caricamento è unico!</small>
                </div>
                
                <!-- KPI Section -->
                <div class="row">
                    {kpi_html}
                </div>
                
                <!-- Charts Section -->
                {charts_html}
                
                <!-- ML Insights -->
                <div class="insight-box">
                    <h3 style="color: {self.theme['primary']}">🤖 Machine Learning Insights</h3>
                    <div class="row">
                        <div class="col-md-4">
                            <p><strong>📊 Data Quality:</strong> {self.insights['data_quality'].get('score', 0):.1f}/100</p>
                        </div>
                        <div class="col-md-4">
                            <p><strong>⚠️ Missing Data:</strong> {self.insights['data_quality'].get('missing_percentage', 0):.1f}%</p>
                        </div>
                        <div class="col-md-4">
                            <p><strong>🔍 Outliers:</strong> {len(self.insights.get('anomalies', []))} righe anomale</p>
                        </div>
                    </div>
                </div>
                
                <!-- Tableau Recommendations -->
                <div class="chart-container">
                    <h3 style="color: {self.theme['primary']}">📋 Come replicare in Tableau</h3>
        """
        
        for rec in self.insights.get('recommendations', [])[:5]:
            html_content += f"""
                    <div class="recommendation">
                        <strong>{rec.get('type', 'Info').upper()}:</strong> {rec.get('text', '')}<br>
                        <small>🎯 {rec.get('action', '')}</small>
                    </div>
            """
        
        # Suggerimenti casuali per Tableau
        tableau_tips = [
            "💡 Prova a usare 'Show Me' in Tableau per esplorare visualizzazioni alternative",
            "🎨 Personalizza i colori usando il pannello 'Marks' per abbinarli al tuo brand",
            "📊 Usa 'Dual Axis' per combinare due tipi di grafici diversi",
            "🔍 Aggiungi 'Tooltips' personalizzati per mostrare metriche aggiuntive",
            "⚡ Usa 'LOD Expressions' per calcoli a livello di dettaglio specifico",
            "📈 Aggiungi 'Forecast' per serie temporali con almeno 2 stagionalità",
            "🎯 Crea 'Parameters' per rendere la dashboard interattiva",
            "📌 Usa 'Annotations' per evidenziare outlier o trend importanti"
        ]
        
        html_content += f"""
                    <div class="insight-box" style="margin-top: 20px;">
                        <h4 style="color: {self.theme['secondary']}">✨ Tableau Tips per questa dashboard</h4>
                        <ul>
                            <li>{random.choice(tableau_tips)}</li>
                            <li>{random.choice(tableau_tips)}</li>
                            <li>{random.choice(tableau_tips)}</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p>🤖 Generato da AI Data Engineer | Theme: {self.theme['name']} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>🔄 Ogni caricamento genera una dashboard unica e diversa!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def get_layout_style(self):
        """Restituisce stili CSS basati sul layout selezionato"""
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
                width: 90%;
                margin: 20px auto;
            }
            """
        elif self.layout_type == 'magazine':
            return """
            .chart-container:nth-child(odd) {
                width: 65%;
                margin: 20px auto;
            }
            .chart-container:nth-child(even) {
                width: 85%;
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
        """Genera KPI cards con variazioni casuali"""
        kpi_html = ""
        metrics_to_show = self.numeric_cols[:min(4, len(self.numeric_cols))]
        
        for col in metrics_to_show:
            try:
                avg_val = self.df[col].mean()
                if pd.isna(avg_val):
                    continue
                
                # Aggiungi icona casuale
                icon = random.choice(['📊', '📈', '📉', '🎯', '💹', '💰', '📦', '👥'])
                
                kpi_html += f"""
                    <div class="col-md-3">
                        <div class="kpi-card">
                            <div class="kpi-label">{icon} {col.upper()}</div>
                            <div class="kpi-value">{avg_val:,.2f}</div>
                            <small>Media: {avg_val:,.2f}</small>
                        </div>
                    </div>
                """
            except:
                continue
        
        if not kpi_html:
            kpi_html = '<div class="col-12"><p class="text-center">Nessuna metrica disponibile</p></div>'
        
        return kpi_html
