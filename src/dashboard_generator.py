import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import pandas as pd
import numpy as np
from datetime import datetime
import random
from typing import List, Dict, Tuple


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
            "#A8E6CF",
            "#FFD3B6",
            "#FFAAA5",
            "#FF8B94",
            "#B5EAD7",
            "#C7CEEA",
            "#E2F0CB",
            "#FFDAC1",
            "#B0E0E6",
            "#F7C6C6",
            "#C9E4DE",
            "#FDD0F2",
            "#D4F1F9",
            "#FFE5B4",
            "#D0F0FD",
            "#E8D0F0",
        ]

        # Tema pastello
        self.theme = {
            "primary": "#A8E6CF",
            "secondary": "#FFD3B6",
            "tertiary": "#C7CEEA",
            "background": "#F9FBF4",
            "card_bg": "#FFFFFF",
            "text": "#4A5B6E",
            "text_light": "#8A9BB0",
            "accent": "#FFB7B2",
            "border": "#E8ECF0",
        }

        # Emoji/Icone per i grafici
        self.chart_icons = {
            "line": "📈",
            "bar": "📊",
            "scatter": "🔍",
            "bubble": "🫧",
            "heatmap": "🔗",
            "histogram": "📈",
            "boxplot": "📦",
            "treemap": "🗂️",
            "radar": "🔄",
            "violin": "🎻",
            "area": "📊",
            "pie": "🥧",
            "map": "🗺️",
        }

        # Seleziona fino a 8 grafici in base ai dati
        self.chart_types = self.select_charts_advanced()

        # Genera KPI dinamici e filtri intelligenti
        self.kpis = self.generate_dynamic_kpis()
        self.suggested_filters = self.suggest_intelligent_filters()
        self.has_geographic_data = self.detect_geographic_data()
        self.layout_type = self.randomize_layout_structure()

    def select_charts_advanced(self):
        """Seleziona automaticamente fino a 8 grafici in base ai dati disponibili"""
        charts = []

        # 1. Time series (se ci sono dati temporali)
        if self.datetime_cols and self.numeric_cols:
            charts.append("line")

        # 2. Bar chart per categorie (se ci sono dati categorici)
        if self.categorical_cols:
            charts.append("bar")

        # 3. Scatter plot (se ci sono almeno 2 metriche numeriche)
        if len(self.numeric_cols) >= 2:
            charts.append("scatter")

        # 4. Bubble chart (se ci sono almeno 3 metriche numeriche)
        if len(self.numeric_cols) >= 3:
            charts.append("bubble")

        # 5. Heatmap correlazioni (se ci sono almeno 3 metriche numeriche)
        if len(self.numeric_cols) >= 3:
            charts.append("heatmap")

        # 6. Istogramma distribuzione
        if self.numeric_cols:
            charts.append("histogram")

        # 7. Box plot per outlier
        if self.numeric_cols:
            charts.append("boxplot")

        # 8. Treemap composizione
        if self.categorical_cols and self.numeric_cols:
            charts.append("treemap")

        # 9. Radar chart (se abbastanza metriche)
        if len(self.numeric_cols) >= 4:
            charts.append("radar")

        # 10. Violin plot (alternativa distribuzione)
        if self.numeric_cols:
            charts.append("violin")

        # 11. Area chart (se dati temporali)
        if self.datetime_cols and self.numeric_cols:
            charts.append("area")

        # 12. Pie chart (se poche categorie)
        if self.categorical_cols and self.df[self.categorical_cols[0]].nunique() <= 8:
            charts.append("pie")

        # Seleziona massimo 8 grafici, assicurando varietà
        selected_charts = []
        chart_priority = [
            "histogram",
            "bar",
            "line",
            "scatter",
            "heatmap",
            "boxplot",
            "treemap",
            "bubble",
        ]

        for chart in chart_priority:
            if chart in charts and len(selected_charts) < 8:
                selected_charts.append(chart)

        # Se ancora meno di 4, aggiungi altri disponibili
        for chart in charts:
            if chart not in selected_charts and len(selected_charts) < 8:
                selected_charts.append(chart)

        # Assicura almeno 4 grafici
        while len(selected_charts) < 4 and self.numeric_cols:
            selected_charts.append("histogram")

        return selected_charts

    def generate_dynamic_kpis(self) -> List[Dict]:
        """Genera KPI dinamici basati sui dati disponibili (0 - infiniti)"""
        kpis = []

        # KPI 1: Numero di record
        kpis.append(
            {
                "title": "Record Totali",
                "value": f"{len(self.df):,.0f}",
                "icon": "📊",
                "trend": None,
                "color": "#A8E6CF",
            }
        )

        # KPI 2-3: Metriche numeriche principali
        if self.numeric_cols:
            for i, col in enumerate(self.numeric_cols[:2]):
                avg_val = self.df[col].mean()
                kpis.append(
                    {
                        "title": f"Media {col}",
                        "value": f"{avg_val:,.2f}",
                        "icon": "📈",
                        "trend": None,
                        "color": self.pastel_colors[i % len(self.pastel_colors)],
                    }
                )

        # KPI 4: Categoria più frequente
        if self.categorical_cols:
            most_freq_col = self.categorical_cols[0]
            most_freq_val = self.df[most_freq_col].value_counts().index[0]
            kpis.append(
                {
                    "title": f"{most_freq_col} Top",
                    "value": str(most_freq_val),
                    "icon": "🏆",
                    "trend": None,
                    "color": "#FFD3B6",
                }
            )

        # KPI 5: Data range (se ci sono dati temporali)
        if self.datetime_cols:
            date_col = self.datetime_cols[0]
            date_range = f"{self.df[date_col].min()} a {self.df[date_col].max()}"
            kpis.append(
                {
                    "title": "Intervallo Tempo",
                    "value": str(date_range),
                    "icon": "📅",
                    "trend": None,
                    "color": "#C7CEEA",
                }
            )

        # KPI 6: Completezza dati
        completeness = (
            1 - (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)))
        ) * 100
        kpis.append(
            {
                "title": "Completezza",
                "value": f"{completeness:.1f}%",
                "icon": "✅",
                "trend": None,
                "color": "#B5EAD7",
            }
        )

        return kpis

    def suggest_intelligent_filters(self) -> List[Dict]:
        """Suggerisce fino a 2 filtri intelligenti basati sui dati"""
        filters = []

        # Filtro 1: Categoria con buona varietà
        if self.categorical_cols:
            for col in self.categorical_cols:
                unique_count = self.df[col].nunique()
                if 2 <= unique_count <= 15:  # Buona varietà per filtro
                    filters.append(
                        {
                            "column": col,
                            "type": "categorical",
                            "values": self.df[col].unique().tolist()[:10],
                            "icon": "🏷️",
                        }
                    )
                    break

        # Filtro 2: Range numerico (se disponibile)
        if self.numeric_cols and len(filters) < 2:
            numeric_col = self.numeric_cols[0]
            filters.append(
                {
                    "column": numeric_col,
                    "type": "numeric_range",
                    "min": float(self.df[numeric_col].min()),
                    "max": float(self.df[numeric_col].max()),
                    "icon": "📊",
                }
            )

        # Filtro 3: Temporale (se disponibile)
        if self.datetime_cols and len(filters) < 2:
            date_col = self.datetime_cols[0]
            filters.append(
                {
                    "column": date_col,
                    "type": "date_range",
                    "min": str(self.df[date_col].min()),
                    "max": str(self.df[date_col].max()),
                    "icon": "📅",
                }
            )

        return filters[:2]  # Max 2 filtri

    def detect_geographic_data(self) -> bool:
        """Rileva se il dataset contiene coordinate geografiche"""
        geo_keywords = [
            "lat",
            "lon",
            "latitude",
            "longitude",
            "country",
            "city",
            "region",
            "province",
        ]

        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in geo_keywords):
                # Verifica se è effettivamente numerico (per lat/lon)
                if "lat" in col_lower or "lon" in col_lower:
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        return True
                else:
                    return True

        return False

    def randomize_layout_structure(self) -> str:
        """Randomizza il tipo di layout della dashboard"""
        layout_types = [
            "grid_2col",  # 2 colonne standard
            "grid_3col",  # 3 colonne compatte
            "asymmetric",  # Layout asimmetrico (1-2-1)
            "featured",  # Un grafico grande in primo piano
            "timeline",  # Timeline con grafici in cascata
        ]
        return random.choice(layout_types)

    def get_chart_icon(self, chart_type: str) -> str:
        """Ritorna l'icona/emoji per un tipo di grafico"""
        return self.chart_icons.get(chart_type, "📊")
        """Grafico a linee per serie temporali"""
        date_col = self.datetime_cols[0]
        metric_col = random.choice(self.numeric_cols)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.df[date_col],
                y=self.df[metric_col],
                mode="lines+markers",
                line=dict(
                    color=self.pastel_colors[index % len(self.pastel_colors)], width=2
                ),
                marker=dict(
                    size=6, color=self.pastel_colors[index % len(self.pastel_colors)]
                ),
                fill="tozeroy",
                fillcolor=f"rgba({int(self.pastel_colors[index % len(self.pastel_colors)][1:3], 16)}, {int(self.pastel_colors[index % len(self.pastel_colors)][3:5], 16)}, {int(self.pastel_colors[index % len(self.pastel_colors)][5:7], 16)}, 0.2)",
            )
        )

        fig.update_layout(
            title=f"📈 {metric_col} nel tempo",
            xaxis_title=date_col,
            yaxis_title=metric_col,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme["text"], size=11),
            hovermode="x unified",
        )
        return fig

    def create_bar_chart(self, index):
        """Grafico a barre per categorie"""
        col = random.choice(self.categorical_cols)
        value_counts = self.df[col].value_counts().head(8)

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=value_counts.index,
                y=value_counts.values,
                marker_color=self.pastel_colors[index % len(self.pastel_colors)],
                text=value_counts.values,
                textposition="outside",
                marker_line_color="white",
                marker_line_width=1,
            )
        )

        fig.update_layout(
            title=f"📊 Top {col}",
            xaxis_title=col,
            yaxis_title="Conteggio",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme["text"], size=11),
            xaxis_tickangle=-45 if len(value_counts) > 5 else 0,
        )
        return fig

    def create_scatter_chart(self, index):
        """Scatter plot per correlazione tra due metriche"""
        col1, col2 = random.sample(self.numeric_cols, 2)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.df[col1],
                y=self.df[col2],
                mode="markers",
                marker=dict(
                    size=10,
                    color=self.pastel_colors[index % len(self.pastel_colors)],
                    opacity=0.6,
                    line=dict(width=1, color="white"),
                ),
                hovertemplate=f"{col1}: %{{x}}<br>{col2}: %{{y}}<extra></extra>",
            )
        )

        fig.update_layout(
            title=f"🔍 {col1} vs {col2}",
            xaxis_title=col1,
            yaxis_title=col2,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme["text"], size=11),
        )
        return fig

    def create_bubble_chart(self, index):
        """Bubble chart con 3 metriche"""
        col1, col2, col3 = random.sample(self.numeric_cols, 3)

        # Normalizza la dimensione delle bolle
        size_norm = (self.df[col3] - self.df[col3].min()) / (
            self.df[col3].max() - self.df[col3].min()
        ) * 50 + 10

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.df[col1],
                y=self.df[col2],
                mode="markers",
                marker=dict(
                    size=size_norm,
                    color=self.pastel_colors[index % len(self.pastel_colors)],
                    opacity=0.6,
                    sizemode="area",
                    sizeref=2.0 * max(size_norm) / (40**2),
                    line=dict(width=1, color="white"),
                ),
                text=self.df.index,
                hovertemplate=f"{col1}: %{{x}}<br>{col2}: %{{y}}<br>{col3}: %{{marker.size}}<extra></extra>",
            )
        )

        fig.update_layout(
            title=f"🫧 {col1} vs {col2} (dimensione={col3})",
            xaxis_title=col1,
            yaxis_title=col2,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme["text"], size=11),
        )
        return fig

    def create_heatmap_chart(self, index):
        """Heatmap delle correlazioni"""
        n_cols = min(len(self.numeric_cols), 6)
        selected_cols = random.sample(self.numeric_cols, n_cols)
        corr = self.df[selected_cols].corr()

        fig = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale="pinkyl",
                zmid=0,
                text=corr.values.round(2),
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False,
            )
        )

        fig.update_layout(
            title=f"🔗 Matrice di Correlazione",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=370,
            margin=dict(l=80, r=20, t=50, b=50),
            font=dict(color=self.theme["text"], size=10),
            xaxis=dict(tickangle=45),
            yaxis=dict(tickangle=0),
        )
        return fig

    def create_histogram_chart(self, index):
        """Istogramma distribuzione"""
        col = random.choice(self.numeric_cols)
        data = self.df[col].dropna()

        fig = go.Figure()
        fig.add_trace(
            go.Histogram(
                x=data,
                nbinsx=min(25, int(np.sqrt(len(data)))),
                marker_color=self.pastel_colors[index % len(self.pastel_colors)],
                marker_line_color="white",
                marker_line_width=1,
                opacity=0.85,
            )
        )

        fig.update_layout(
            title=f"📊 Distribuzione {col}",
            xaxis_title=col,
            yaxis_title="Frequenza",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme["text"], size=11),
        )
        return fig

    def create_boxplot_chart(self, index):
        """Box plot per outlier"""
        col = random.choice(self.numeric_cols)

        fig = go.Figure()
        fig.add_trace(
            go.Box(
                y=self.df[col].dropna(),
                name=col,
                marker_color=self.pastel_colors[index % len(self.pastel_colors)],
                line_color=self.pastel_colors[index % len(self.pastel_colors)],
                boxmean="sd",
                fillcolor=f"rgba({int(self.pastel_colors[index % len(self.pastel_colors)][1:3], 16)}, {int(self.pastel_colors[index % len(self.pastel_colors)][3:5], 16)}, {int(self.pastel_colors[index % len(self.pastel_colors)][5:7], 16)}, 0.3)",
            )
        )

        fig.update_layout(
            title=f"📦 Distribuzione {col}",
            yaxis_title=col,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme["text"], size=11),
        )
        return fig

    def create_treemap_chart(self, index):
        """Treemap composizione"""
        cat_col = random.choice(self.categorical_cols)
        num_col = random.choice(self.numeric_cols)

        aggregated = self.df.groupby(cat_col)[num_col].sum().head(12)

        fig = go.Figure(
            go.Treemap(
                labels=aggregated.index,
                parents=[""] * len(aggregated),
                values=aggregated.values,
                marker_colors=aggregated.values,
                marker_colorscale="Pastel",
                textinfo="label+value",
                hovertemplate="%{label}: %{value:,.0f}<extra></extra>",
            )
        )

        fig.update_layout(
            title=f"🗂️ {num_col} per {cat_col}",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(color=self.theme["text"], size=10),
        )
        return fig

    def create_radar_chart(self, index):
        """Radar chart comparativo"""
        # Prendi le medie delle prime 5 metriche
        metrics = self.numeric_cols[:5]
        averages = [self.df[col].mean() for col in metrics]

        # Normalizza
        max_vals = [self.df[col].max() for col in metrics]
        normalized = [
            avg / maxv if maxv > 0 else 0 for avg, maxv in zip(averages, max_vals)
        ]

        fig = go.Figure(
            data=go.Scatterpolar(
                r=normalized,
                theta=metrics,
                fill="toself",
                marker=dict(color=self.pastel_colors[index % len(self.pastel_colors)]),
                line=dict(
                    color=self.pastel_colors[index % len(self.pastel_colors)], width=2
                ),
                name="Media Normalizzata",
            )
        )

        fig.update_layout(
            title=f"🔄 Confronto Metriche",
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(size=9)),
                angularaxis=dict(tickfont=dict(size=9)),
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=40, t=50, b=40),
            font=dict(color=self.theme["text"], size=10),
        )
        return fig

    def create_violin_chart(self, index):
        """Violin plot per densità"""
        col = random.choice(self.numeric_cols)

        fig = go.Figure()
        fig.add_trace(
            go.Violin(
                y=self.df[col].dropna(),
                name=col,
                box_visible=True,
                meanline_visible=True,
                fillcolor=self.pastel_colors[index % len(self.pastel_colors)],
                line_color=self.pastel_colors[index % len(self.pastel_colors)],
                opacity=0.7,
            )
        )

        fig.update_layout(
            title=f"🎻 Densità {col}",
            yaxis_title=col,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme["text"], size=11),
        )
        return fig

    def create_area_chart(self, index):
        """Area chart per volume cumulativo"""
        date_col = self.datetime_cols[0]
        metric_col = random.choice(self.numeric_cols)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.df[date_col],
                y=self.df[metric_col],
                mode="lines",
                line=dict(
                    color=self.pastel_colors[index % len(self.pastel_colors)], width=2
                ),
                fill="tozeroy",
                fillcolor=f"rgba({int(self.pastel_colors[index % len(self.pastel_colors)][1:3], 16)}, {int(self.pastel_colors[index % len(self.pastel_colors)][3:5], 16)}, {int(self.pastel_colors[index % len(self.pastel_colors)][5:7], 16)}, 0.4)",
            )
        )

        fig.update_layout(
            title=f"📊 Volume {metric_col} nel tempo",
            xaxis_title=date_col,
            yaxis_title=metric_col,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(color=self.theme["text"], size=11),
        )
        return fig

    def create_pie_chart(self, index):
        """Grafico a torta"""
        col = random.choice(self.categorical_cols)
        value_counts = self.df[col].value_counts().head(6)

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=value_counts.index,
                    values=value_counts.values,
                    hole=0.3,
                    marker_colors=self.pastel_colors[: len(value_counts)],
                    textinfo="label+percent",
                    textposition="auto",
                    pull=[0.05] * len(value_counts),
                )
            ]
        )

        fig.update_layout(
            title=f"🥧 Composizione {col}",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(color=self.theme["text"], size=11),
        )
        return fig

    def create_dashboard_html(self):
        """Genera dashboard HTML completa con filtri e layout professionale"""

        # Genera KPI cards (6 KPI dinamici)
        kpi_html = self.generate_kpi_cards_advanced()

        # Genera filtri HTML
        filters_html = self.generate_filters_html()

        # Genera grafici
        charts_html = ""
        chart_functions = {
            "line": self.create_line_chart,
            "bar": self.create_bar_chart,
            "scatter": self.create_scatter_chart,
            "bubble": self.create_bubble_chart,
            "heatmap": self.create_heatmap_chart,
            "histogram": self.create_histogram_chart,
            "boxplot": self.create_boxplot_chart,
            "treemap": self.create_treemap_chart,
            "radar": self.create_radar_chart,
            "violin": self.create_violin_chart,
            "area": self.create_area_chart,
            "pie": self.create_pie_chart,
        }

        for idx, chart_type in enumerate(self.chart_types):
            try:
                if chart_type in chart_functions:
                    fig = chart_functions[chart_type](idx)
                    fig_json = json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder)
                    charts_html += f"""
                    <div class="chart-card" data-chart-type="{chart_type}">
                        <div class="chart-header">
                            <span class="chart-icon">{self.get_chart_icon(chart_type)}</span>
                            <button class="chart-expand" onclick="expandChart(this)">⛶</button>
                        </div>
                        <div id="chart_{idx}" class="chart-container" style="width:100%; height:320px;"></div>
                    </div>
                    <script>
                        (function() {{
                            var fig_{idx} = {fig_json};
                            Plotly.newPlot('chart_{idx}', fig_{idx}.data, fig_{idx}.layout, {{responsive: true}});
                        }})();
                    </script>
                    """
            except Exception as e:
                charts_html += f"<div class='alert-warning'>Errore grafico {chart_type}: {str(e)}</div>"

        # Layout CSS per griglia dinamica
        grid_template = self.get_grid_template()

        # HTML completo
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Interactive Pastel Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-3.0.1.min.js"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                }}
                
                /* Layout principale */
                .app {{
                    display: flex;
                    height: 100%;
                    width: 100%;
                }}
                
                /* SIDEBAR FILTRI */
                .sidebar {{
                    width: 280px;
                    background: {self.theme['card_bg']};
                    border-right: 1px solid {self.theme['border']};
                    display: flex;
                    flex-direction: column;
                    overflow-y: auto;
                    padding: 20px;
                    gap: 24px;
                    flex-shrink: 0;
                }}
                
                .sidebar-section {{
                    border-bottom: 1px solid {self.theme['border']};
                    padding-bottom: 16px;
                }}
                
                .sidebar-title {{
                    font-size: 0.75rem;
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                    color: {self.theme['text_light']};
                    margin-bottom: 12px;
                    font-weight: 600;
                }}
                
                .filter-group {{
                    margin-bottom: 16px;
                }}
                
                .filter-label {{
                    font-size: 0.8rem;
                    color: {self.theme['text']};
                    margin-bottom: 6px;
                    display: block;
                }}
                
                select, input {{
                    width: 100%;
                    padding: 10px 12px;
                    border: 1px solid {self.theme['border']};
                    border-radius: 12px;
                    font-size: 0.85rem;
                    background: {self.theme['background']};
                    color: {self.theme['text']};
                    transition: all 0.2s;
                }}
                
                select:focus, input:focus {{
                    outline: none;
                    border-color: {self.theme['primary']};
                    box-shadow: 0 0 0 3px {self.theme['primary']}30;
                }}
                
                .checkbox-group {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-top: 8px;
                }}
                
                .checkbox-item {{
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    font-size: 0.8rem;
                    color: {self.theme['text']};
                }}
                
                .reset-btn {{
                    background: {self.theme['primary']};
                    color: {self.theme['text']};
                    border: none;
                    padding: 10px;
                    border-radius: 12px;
                    cursor: pointer;
                    font-weight: 600;
                    width: 100%;
                    transition: all 0.2s;
                }}
                
                .reset-btn:hover {{
                    opacity: 0.8;
                    transform: translateY(-1px);
                }}
                
                /* AREA PRINCIPALE */
                .main {{
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    padding: 20px;
                }}
                
                /* HEADER */
                .header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    flex-shrink: 0;
                }}
                
                .header h1 {{
                    font-size: 1.6rem;
                    color: {self.theme['text']};
                    font-weight: 600;
                }}
                
                .header h1 i {{
                    color: {self.theme['primary']};
                    margin-right: 10px;
                }}
                
                .header-actions {{
                    display: flex;
                    gap: 12px;
                }}
                
                .icon-btn {{
                    background: {self.theme['card_bg']};
                    border: 1px solid {self.theme['border']};
                    padding: 10px 16px;
                    border-radius: 40px;
                    cursor: pointer;
                    font-size: 0.85rem;
                    color: {self.theme['text']};
                    transition: all 0.2s;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}
                
                .icon-btn:hover {{
                    background: {self.theme['primary']}20;
                }}
                
                /* KPI ROW */
                .kpi-row {{
                    display: grid;
                    grid-template-columns: repeat(6, 1fr);
                    gap: 16px;
                    margin-bottom: 20px;
                    flex-shrink: 0;
                }}
                
                .kpi-card {{
                    background: {self.theme['card_bg']};
                    border-radius: 20px;
                    padding: 16px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                    border: 1px solid {self.theme['border']};
                    transition: all 0.2s;
                }}
                
                .kpi-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                }}
                
                .kpi-label {{
                    font-size: 0.7rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: {self.theme['text_light']};
                    margin-bottom: 8px;
                }}
                
                .kpi-value {{
                    font-size: 1.6rem;
                    font-weight: 700;
                    color: {self.theme['text']};
                }}
                
                .kpi-trend {{
                    font-size: 0.7rem;
                    margin-top: 6px;
                    color: {self.theme['text_light']};
                }}
                
                /* GRIGLIA GRAFICI DINAMICA */
                .charts-grid {{
                    flex: 1;
                    display: grid;
                    {grid_template}
                    gap: 16px;
                    overflow-y: auto;
                    min-height: 0;
                    padding: 2px;
                }}
                
                .chart-card {{
                    background: {self.theme['card_bg']};
                    border-radius: 20px;
                    padding: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                    border: 1px solid {self.theme['border']};
                    display: flex;
                    flex-direction: column;
                    transition: all 0.2s;
                }}
                
                .chart-card:hover {{
                    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                }}
                
                .chart-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 8px;
                    padding: 0 4px;
                }}
                
                .chart-icon {{
                    font-size: 1.2rem;
                }}
                
                .chart-expand {{
                    background: none;
                    border: none;
                    cursor: pointer;
                    font-size: 0.9rem;
                    color: {self.theme['text_light']};
                    padding: 4px 8px;
                    border-radius: 8px;
                }}
                
                .chart-expand:hover {{
                    background: {self.theme['background']};
                }}
                
                .chart-container {{
                    flex: 1;
                    min-height: 0;
                }}
                
                .alert-warning {{
                    background: #FFF3E0;
                    padding: 16px;
                    border-radius: 16px;
                    color: #E67E22;
                    margin: 10px;
                }}
                
                /* Modal per espansione grafico */
                .modal {{
                    display: none;
                    position: fixed;
                    z-index: 1000;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.5);
                    justify-content: center;
                    align-items: center;
                }}
                
                .modal-content {{
                    background: {self.theme['card_bg']};
                    border-radius: 24px;
                    width: 90%;
                    height: 85%;
                    padding: 20px;
                    position: relative;
                }}
                
                .modal-close {{
                    position: absolute;
                    right: 20px;
                    top: 15px;
                    font-size: 28px;
                    cursor: pointer;
                    color: {self.theme['text_light']};
                }}
                
                .modal-close:hover {{
                    color: {self.theme['text']};
                }}
                
                /* Responsive */
                @media (max-width: 1200px) {{
                    .kpi-row {{ grid-template-columns: repeat(3, 1fr); }}
                }}
                
                @media (max-width: 768px) {{
                    .sidebar {{ width: 240px; }}
                    .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
                    .charts-grid {{ grid-template-columns: 1fr; }}
                }}
                
                @media (max-width: 640px) {{
                    .app {{ flex-direction: column; }}
                    .sidebar {{ width: 100%; max-height: 200px; flex-direction: row; flex-wrap: wrap; gap: 12px; }}
                    .sidebar-section {{ flex: 1; min-width: 140px; }}
                }}
            </style>
        </head>
        <body>
            <div class="app">
                <!-- Sidebar Filtri -->
                <div class="sidebar">
                    {filters_html}
                    <button class="reset-btn" onclick="resetAllFilters()">
                        <i class="fas fa-undo-alt"></i> Reset Filtri
                    </button>
                </div>
                
                <!-- Area Principale -->
                <div class="main">
                    <div class="header">
                        <h1><i class="fas fa-chalkboard-user"></i> Pastel Interactive Dashboard</h1>
                        <div class="header-actions">
                            <button class="icon-btn" onclick="toggleTheme()">
                                <i class="fas fa-moon"></i> Tema
                            </button>
                            <button class="icon-btn" onclick="exportData()">
                                <i class="fas fa-download"></i> CSV
                            </button>
                        </div>
                    </div>
                    
                    <!-- KPI Row -->
                    <div class="kpi-row" id="kpi-row">
                        {kpi_html}
                    </div>
                    
                    <!-- Charts Grid -->
                    <div class="charts-grid" id="charts-grid">
                        {charts_html}
                    </div>
                </div>
            </div>
            
            <!-- Modal per grafico espanso -->
            <div id="chartModal" class="modal">
                <div class="modal-content">
                    <span class="modal-close" onclick="closeModal()">&times;</span>
                    <div id="modalChart" style="width:100%; height:95%;"></div>
                </div>
            </div>
            
            <script>
                // Funzioni interattive
                function expandChart(btn) {{
                    const chartCard = btn.closest('.chart-card');
                    const chartDiv = chartCard.querySelector('.chart-container');
                    const chartId = chartDiv.id;
                    const modal = document.getElementById('chartModal');
                    const modalChart = document.getElementById('modalChart');
                    
                    // Clona il grafico nel modal
                    const originalPlot = document.getElementById(chartId);
                    if (originalPlot && originalPlot.data) {{
                        Plotly.newPlot(modalChart, originalPlot.data, originalPlot.layout, {{responsive: true}});
                    }}
                    
                    modal.style.display = 'flex';
                }}
                
                function closeModal() {{
                    document.getElementById('chartModal').style.display = 'none';
                }}
                
                function resetAllFilters() {{
                    // Reset di tutti i select e input
                    document.querySelectorAll('.sidebar select, .sidebar input').forEach(el => {{
                        if (el.tagName === 'SELECT') el.selectedIndex = 0;
                        if (el.type === 'text') el.value = '';
                        if (el.type === 'checkbox') el.checked = false;
                    }});
                    alert('Filtri resettati! Ricarica la dashboard per applicare i filtri.');
                }}
                
                function toggleTheme() {{
                    document.body.classList.toggle('dark-theme');
                }}
                
                function exportData() {{
                    window.location.href = '/export';
                }}
                
                // Chiudi modal con ESC
                document.addEventListener('keydown', function(e) {{
                    if (e.key === 'Escape') closeModal();
                }});
            </script>
        </body>
        </html>
        """

        return html_content

    def get_grid_template(self):
        """Restituisce il template CSS della griglia in base al numero di grafici"""
        n_charts = len(self.chart_types)

        if n_charts <= 2:
            return "grid-template-columns: 1fr;"
        elif n_charts <= 4:
            return "grid-template-columns: repeat(2, 1fr);"
        elif n_charts <= 6:
            return "grid-template-columns: repeat(3, 1fr);"
        else:
            return "grid-template-columns: repeat(4, 1fr);"

    def get_chart_icon(self, chart_type):
        """Restituisce l'icona per il tipo di grafico"""
        icons = {
            "line": "📈",
            "bar": "📊",
            "scatter": "🔍",
            "bubble": "🫧",
            "heatmap": "🔥",
            "histogram": "📉",
            "boxplot": "📦",
            "treemap": "🗂️",
            "radar": "🔄",
            "violin": "🎻",
            "area": "📊",
            "pie": "🥧",
        }
        return icons.get(chart_type, "📊")

    def generate_kpi_cards_advanced(self):
        """Genera 6 KPI cards dinamici"""
        kpi_html = ""

        kpis = []

        # 1. Totale (se ci sono metriche numeriche)
        if self.numeric_cols:
            col = self.numeric_cols[0]
            total = self.df[col].sum()
            kpis.append(("💰 Totale", f"{total:,.0f}", col))

        # 2. Media
        if self.numeric_cols:
            col = self.numeric_cols[0]
            media = self.df[col].mean()
            kpis.append(("📊 Media", f"{media:,.2f}", col))

        # 3. Tasso di crescita (se ci sono date)
        if self.datetime_cols and self.numeric_cols:
            try:
                col = self.numeric_cols[0]
                sorted_df = self.df.sort_values(self.datetime_cols[0])
                first_val = sorted_df[col].iloc[0] if len(sorted_df) > 0 else 0
                last_val = sorted_df[col].iloc[-1] if len(sorted_df) > 0 else 0
                if first_val != 0:
                    growth = ((last_val - first_val) / first_val) * 100
                    trend = "▲" if growth > 0 else "▼"
                    kpis.append(
                        (f"📈 Crescita", f"{trend} {abs(growth):.1f}%", "vs periodo")
                    )
            except:
                pass

        # 4. Massimo
        if self.numeric_cols:
            col = self.numeric_cols[0]
            max_val = self.df[col].max()
            kpis.append(("🏔️ Massimo", f"{max_val:,.0f}", col))

        # 5. Minimo
        if self.numeric_cols:
            col = self.numeric_cols[0]
            min_val = self.df[col].min()
            kpis.append(("⛰️ Minimo", f"{min_val:,.0f}", col))

        # 6. Conteggio univoco (categorie)
        if self.categorical_cols:
            col = self.categorical_cols[0]
            unique_count = self.df[col].nunique()
            kpis.append((f"🔢 {col[:8]}", f"{unique_count:,}", "valori unici"))

        # Assicura almeno 6 KPI
        while len(kpis) < 6:
            kpis.append(("📌 Dato", "—", ""))

        for label, value, subtitle in kpis[:6]:
            kpi_html += f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-trend">{subtitle}</div>
            </div>
            """

        return kpi_html

    def generate_filters_html(self):
        """Genera la sidebar con i filtri interattivi"""
        filters_html = """
        <div class="sidebar-section">
            <div class="sidebar-title"><i class="fas fa-filter"></i> FILTRI</div>
        """

        # Filtro temporale
        if self.datetime_cols:
            filters_html += f"""
            <div class="filter-group">
                <label class="filter-label"><i class="far fa-calendar-alt"></i> Periodo</label>
                <select id="date_filter">
                    <option value="all">Tutti i dati</option>
                    <option value="last7">Ultimi 7 giorni</option>
                    <option value="last30">Ultimi 30 giorni</option>
                    <option value="last90">Ultimi 90 giorni</option>
                </select>
            </div>
            """

        # Filtro per categoria principale
        if self.categorical_cols:
            col = self.categorical_cols[0]
            unique_vals = self.df[col].dropna().unique()[:15]
            filters_html += f"""
            <div class="filter-group">
                <label class="filter-label"><i class="fas fa-tag"></i> {col}</label>
                <select id="category_filter">
                    <option value="all">Tutti</option>
            """
            for val in unique_vals:
                filters_html += f'<option value="{val}">{val}</option>'
            filters_html += """
                </select>
            </div>
            """

        # Filtro metriche multiple
        if len(self.numeric_cols) > 1:
            filters_html += """
            <div class="filter-group">
                <label class="filter-label"><i class="fas fa-chart-line"></i> Metriche</label>
                <div class="checkbox-group" id="metrics_filter">
            """
            for col in self.numeric_cols[:5]:
                filters_html += f"""
                    <label class="checkbox-item">
                        <input type="checkbox" value="{col}" checked> {col}
                    </label>
                """
            filters_html += """
                </div>
            </div>
            """

        # Ricerca testuale
        if self.categorical_cols:
            filters_html += """
            <div class="filter-group">
                <label class="filter-label"><i class="fas fa-search"></i> Ricerca</label>
                <input type="text" id="search_filter" placeholder="Cerca...">
            </div>
            """

        filters_html += "</div>"
        return filters_html
