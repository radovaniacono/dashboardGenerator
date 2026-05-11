import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
import re

warnings.filterwarnings("ignore")


class MLAnalyzer:
    def __init__(self, df):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

        # Rilevazione avanzata dei tipi di dati
        self.monetary_cols = self._detect_monetary_columns()
        self.percentage_cols = self._detect_percentage_columns()
        self.boolean_cols = self._detect_boolean_columns()
        self.geographic_cols = self._detect_geographic_columns()
        self.temporal_cols = self._detect_temporal_columns()

    def _detect_monetary_columns(self):
        """Rileva colonne monetarie per specifiche formattazioni"""
        monetary = []
        for col in self.numeric_cols:
            col_lower = col.lower()
            if any(
                term in col_lower
                for term in [
                    "price",
                    "cost",
                    "revenue",
                    "sales",
                    "amount",
                    "price",
                    "prezzo",
                    "costo",
                    "ricavo",
                    "vendita",
                    "importo",
                    "valore",
                ]
            ):
                monetary.append(col)
        return monetary

    def _detect_percentage_columns(self):
        """Rileva colonne percentuali"""
        percentage = []
        for col in self.numeric_cols:
            col_lower = col.lower()
            if any(
                term in col_lower
                for term in ["percent", "rate", "ratio", "%", "percentuale", "tasso"]
            ):
                percentage.append(col)
            # Controlla se i valori sono fra 0-100
            elif self.df[col].max() <= 100 and self.df[col].min() >= 0:
                percentage.append(col)
        return percentage

    def _detect_boolean_columns(self):
        """Rileva colonne booleane nascoste"""
        boolean = []
        for col in self.categorical_cols:
            unique_vals = self.df[col].dropna().unique()
            if len(unique_vals) <= 2:
                boolean.append(col)
        return boolean

    def _detect_geographic_columns(self):
        """Rileva colonne geografiche (lat, lon, paesi, città, etc.)"""
        geographic = []
        geo_keywords = {
            "coordinate": ["lat", "lon", "latitude", "longitude"],
            "location": [
                "country",
                "city",
                "region",
                "province",
                "stato",
                "provincia",
                "città",
                "paese",
            ],
            "postal": ["zip", "postal", "cap", "codice_postale"],
        }

        for col in self.df.columns:
            col_lower = col.lower()
            for geo_type, keywords in geo_keywords.items():
                if any(k in col_lower for k in keywords):
                    if geo_type == "coordinate" and pd.api.types.is_numeric_dtype(
                        self.df[col]
                    ):
                        geographic.append({"col": col, "type": geo_type})
                    elif geo_type != "coordinate":
                        geographic.append({"col": col, "type": geo_type})
        return geographic

    def _detect_temporal_columns(self):
        """Rileva colonne temporali nascoste in formato stringa"""
        temporal = []
        date_patterns = [
            r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
            r"\d{2}/\d{2}/\d{4}",  # DD/MM/YYYY
            r"\d{4}/\d{2}/\d{2}",  # YYYY/MM/DD
        ]

        for col in self.categorical_cols:
            if any(term in col.lower() for term in ["date", "time", "data", "ora"]):
                temporal.append(col)
        return temporal

    def analyze_data_profile(self):
        """Analisi approfondita del profilo dati con ML"""
        profile = {
            "shape": self.df.shape,
            "missing_values": self.df.isnull().sum().to_dict(),
            "missing_percentage": (
                self.df.isnull().sum() / len(self.df) * 100
            ).to_dict(),
            "data_types": self.df.dtypes.astype(str).to_dict(),
            "unique_counts": self.df.nunique().to_dict(),
            "cardinality": self._calculate_cardinality(),
            "numeric_stats": {},
            "correlations": {},
            "outliers": {},
            "clusters": None,
            "key_metrics": self._identify_key_metrics(),
            "data_quality_issues": self._detect_data_quality_issues(),
        }

        # Statistiche per colonne numeriche
        for col in self.numeric_cols:
            profile["numeric_stats"][col] = {
                "mean": (
                    float(self.df[col].mean())
                    if not pd.isna(self.df[col].mean())
                    else 0
                ),
                "median": (
                    float(self.df[col].median())
                    if not pd.isna(self.df[col].median())
                    else 0
                ),
                "std": (
                    float(self.df[col].std()) if not pd.isna(self.df[col].std()) else 0
                ),
                "q25": (
                    float(self.df[col].quantile(0.25))
                    if not pd.isna(self.df[col].quantile(0.25))
                    else 0
                ),
                "q75": (
                    float(self.df[col].quantile(0.75))
                    if not pd.isna(self.df[col].quantile(0.75))
                    else 0
                ),
                "min": (
                    float(self.df[col].min()) if not pd.isna(self.df[col].min()) else 0
                ),
                "max": (
                    float(self.df[col].max()) if not pd.isna(self.df[col].max()) else 0
                ),
                "range": (
                    float(self.df[col].max() - self.df[col].min())
                    if not pd.isna(self.df[col].min())
                    else 0
                ),
                "skewness": (
                    float(self.df[col].skew())
                    if not pd.isna(self.df[col].skew())
                    else 0
                ),
                "kurtosis": (
                    float(self.df[col].kurtosis())
                    if not pd.isna(self.df[col].kurtosis())
                    else 0
                ),
                "cv": (
                    float(self.df[col].std() / self.df[col].mean())
                    if self.df[col].mean() != 0
                    else 0
                ),  # Coefficiente di variazione
                "is_monetary": col in self.monetary_cols,
                "is_percentage": col in self.percentage_cols,
            }

            # Rilevazione outlier con Isolation Forest
            if len(self.numeric_cols) > 0 and len(self.df) > 10:
                try:
                    iso_forest = IsolationForest(contamination=0.1, random_state=42)
                    outliers_pred = iso_forest.fit_predict(
                        self.df[self.numeric_cols].fillna(0)
                    )
                    profile["outliers"][col] = int((outliers_pred == -1).sum())
                except:
                    profile["outliers"][col] = 0

        # Matrice di correlazione
        if len(self.numeric_cols) > 1:
            try:
                corr_matrix = self.df[self.numeric_cols].corr()
                profile["correlations"] = corr_matrix.to_dict()

                # Identifica correlazioni forti
                strong_correlations = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i + 1, len(corr_matrix.columns)):
                        corr_val = corr_matrix.iloc[i, j]
                        if abs(corr_val) > 0.7:
                            strong_correlations.append(
                                {
                                    "var1": corr_matrix.columns[i],
                                    "var2": corr_matrix.columns[j],
                                    "correlation": float(corr_val),
                                }
                            )
                profile["strong_correlations"] = strong_correlations
            except:
                profile["strong_correlations"] = []

        # Clustering automatico
        if len(self.numeric_cols) >= 2 and len(self.df) > 20:
            profile["clusters"] = self.auto_clustering()

        return profile

    def _calculate_cardinality(self):
        """Calcola la cardinalità delle colonne"""
        cardinality = {}
        for col in self.df.columns:
            unique_count = self.df[col].nunique()
            cardinality[col] = {
                "unique_values": unique_count,
                "cardinality_ratio": unique_count / len(self.df),
                "is_high_cardinality": unique_count > len(self.df) * 0.5,
                "is_low_cardinality": unique_count <= 10,
            }
        return cardinality

    def _identify_key_metrics(self):
        """Identifica le metriche chiave del dataset"""
        key_metrics = []

        # Metriche monetarie
        if self.monetary_cols:
            key_metrics.extend(
                [{"col": col, "type": "monetary"} for col in self.monetary_cols[:3]]
            )

        # Metriche di volume/conteggio
        for col in self.numeric_cols:
            if (
                "count" in col.lower()
                or "total" in col.lower()
                or "numero" in col.lower()
                or "n_" in col.lower()
            ):
                key_metrics.append({"col": col, "type": "count"})

        # Percentuali/tassi
        if self.percentage_cols:
            key_metrics.extend(
                [{"col": col, "type": "percentage"} for col in self.percentage_cols[:2]]
            )

        return key_metrics

    def _detect_data_quality_issues(self):
        """Rileva problemi di qualità dei dati"""
        issues = []

        # Colonne completamente vuote
        for col in self.df.columns:
            missing_pct = self.df[col].isnull().sum() / len(self.df) * 100
            if missing_pct > 50:
                issues.append(
                    {
                        "type": "missing_data",
                        "column": col,
                        "severity": "high",
                        "message": f"{col}: {missing_pct:.1f}% dati mancanti",
                    }
                )
            elif missing_pct > 20:
                issues.append(
                    {
                        "type": "missing_data",
                        "column": col,
                        "severity": "medium",
                        "message": f"{col}: {missing_pct:.1f}% dati mancanti",
                    }
                )

        # Duplicati
        dup_count = self.df.duplicated().sum()
        if dup_count > 0:
            issues.append(
                {
                    "type": "duplicates",
                    "severity": "medium",
                    "message": f"{dup_count} righe duplicate ({dup_count/len(self.df)*100:.1f}%)",
                }
            )

        return issues

    def auto_clustering(self):
        """Clustering automatico per scoprire segmenti"""
        try:
            # Prepara i dati
            data = self.df[self.numeric_cols].fillna(
                self.df[self.numeric_cols].median()
            )
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(data)

            # Trova numero ottimale di cluster
            best_k = 2
            best_score = -1

            for k in range(2, min(10, len(self.df) // 10 + 2)):
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(data_scaled)
                if len(set(labels)) > 1:
                    try:
                        score = silhouette_score(data_scaled, labels)
                        if score > best_score:
                            best_score = score
                            best_k = k
                    except:
                        pass

            # Clustering finale
            kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(data_scaled)

            # Analizza i cluster
            cluster_analysis = []
            for i in range(best_k):
                cluster_data = self.df[clusters == i]
                cluster_profile = {
                    "cluster_id": int(i),
                    "size": len(cluster_data),
                    "percentage": float(len(cluster_data) / len(self.df) * 100),
                    "avg_values": {
                        k: float(v)
                        for k, v in cluster_data[self.numeric_cols]
                        .mean()
                        .to_dict()
                        .items()
                    },
                }
                cluster_analysis.append(cluster_profile)

            self.df["auto_cluster"] = clusters

            return {
                "n_clusters": best_k,
                "silhouette_score": float(best_score),
                "clusters": cluster_analysis,
            }
        except:
            return None

    def generate_ml_insights(self):
        """Genera insight basati su ML"""
        profile = self.analyze_data_profile()

        insights = {
            "data_quality": self.assess_data_quality(profile),
            "key_drivers": self.find_key_drivers(),
            "anomalies": self.detect_anomalies(),
            "recommendations": self.generate_recommendations(profile),
        }

        return insights

    def assess_data_quality(self, profile):
        """Valuta la qualità dei dati"""
        total_cells = profile["shape"][0] * profile["shape"][1]
        missing_cells = sum(profile["missing_values"].values())
        missing_percentage = (
            (missing_cells / total_cells) * 100 if total_cells > 0 else 0
        )

        quality_score = 100 - min(missing_percentage, 100)

        return {
            "score": quality_score,
            "missing_percentage": missing_percentage,
            "has_outliers": any(v > 0 for v in profile["outliers"].values()),
            "completeness": "Buona" if missing_percentage < 10 else "Da migliorare",
        }

    def find_key_drivers(self):
        """Trova i driver principali usando Random Forest"""
        if len(self.numeric_cols) < 2 or len(self.df) < 50:
            return []

        # Trova la colonna target (potrebbe essere l'ultima numerica o specifica)
        target_col = self.numeric_cols[-1]
        feature_cols = [c for c in self.numeric_cols if c != target_col]

        if not feature_cols:
            return []

        try:
            X = self.df[feature_cols].fillna(self.df[feature_cols].median())
            y = self.df[target_col].fillna(self.df[target_col].median())

            rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            rf.fit(X, y)

            importance = []
            for i, col in enumerate(feature_cols):
                importance.append(
                    {"feature": col, "importance": float(rf.feature_importances_[i])}
                )

            importance.sort(key=lambda x: x["importance"], reverse=True)
            return importance[:5]
        except:
            return []

    def detect_anomalies(self):
        """Rileva anomalie nei dati"""
        if len(self.numeric_cols) < 1:
            return []

        try:
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomalies = iso_forest.fit_predict(self.df[self.numeric_cols].fillna(0))
            anomaly_indices = np.where(anomalies == -1)[0]

            anomalies_list = []
            for idx in anomaly_indices[:10]:
                row_data = self.df.iloc[idx].to_dict()
                anomalies_list.append(
                    {
                        "row_index": int(idx),
                        "values": {
                            k: str(v)[:50] for k, v in list(row_data.items())[:5]
                        },
                    }
                )

            return anomalies_list
        except:
            return []

    def generate_recommendations(self, profile):
        """Genera raccomandazioni automatiche per Tableau"""
        recommendations = []

        # Basato su correlazioni
        if profile.get("strong_correlations"):
            recommendations.append(
                {
                    "type": "correlation",
                    "text": f"Forti correlazioni trovate: {profile['strong_correlations'][0]['var1']} ↔ {profile['strong_correlations'][0]['var2']} (r={profile['strong_correlations'][0]['correlation']:.2f})",
                    "action": "Crea scatter plot e analisi di regressione in Tableau",
                }
            )

        # Basato su clustering
        if profile.get("clusters"):
            recommendations.append(
                {
                    "type": "clustering",
                    "text": f"Identificati {profile['clusters']['n_clusters']} segmenti di clienti/dati naturali",
                    "action": "Crea un cluster analysis dashboard in Tableau con colori per segmento",
                }
            )

        # Basato su qualità dati
        if profile.get("data_quality", {}).get("missing_percentage", 0) > 15:
            recommendations.append(
                {
                    "type": "data_quality",
                    "text": f"Alta percentuale di dati mancanti ({profile['data_quality']['missing_percentage']:.1f}%)",
                    "action": "Usa Tableau Prep per pulire i dati prima della visualizzazione",
                }
            )

        # Suggerimenti generali
        if len(self.numeric_cols) > 5:
            recommendations.append(
                {
                    "type": "dimension",
                    "text": f"Dataset con {len(self.numeric_cols)} metriche numeriche",
                    "action": "Considera di usare misure multiple e assi combinati in Tableau",
                }
            )

        if self.datetime_cols:
            recommendations.append(
                {
                    "type": "temporal",
                    "text": f"Dati temporali rilevati in {self.datetime_cols[0]}",
                    "action": "Usa gerarchie di date per drill-down (anno/mese/giorno)",
                }
            )

        return recommendations
