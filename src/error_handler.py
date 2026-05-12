"""
Error Handler - Rilevamento e correzione automatica degli errori
Gestisce validazione file, pulizia dati e error messaging user-friendly
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Optional, List, Dict
from pathlib import Path
import traceback
from datetime import datetime

logging.basicConfig(level=logging.WARNING)


class DashboardErrorHandler:
    """Rileva e corregge automaticamente errori nei file e nei dati"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.errors_found = []
        self.corrections_applied = []
        self.warnings = []

    def validate_and_repair_file(
        self, file_path: str
    ) -> Tuple[bool, Optional[pd.DataFrame], List[str]]:
        """
        Valida file e applica correzioni automatiche

        Args:
            file_path: Path al file da validare

        Returns:
            Tuple: (is_valid: bool, dataframe: pd.DataFrame, corrections: List[str])
        """
        self.errors_found = []
        self.corrections_applied = []
        self.warnings = []

        try:
            # Step 1: Carica file con gestione errori
            df = self._load_file_safely(file_path)
            if df is None:
                return False, None, self.corrections_applied

            # Step 2: Validazione dati vuoti
            if not self._validate_not_empty(df):
                return False, df, self.corrections_applied

            # Step 3: Rileva problemi comuni
            issues = self._detect_common_issues(df)

            # Step 4: Applica correzioni
            for issue_type, details in issues:
                fixed_df, correction_msg = self._fix_issue(df, issue_type, details)
                if fixed_df is not None:
                    df = fixed_df
                    self.corrections_applied.append(correction_msg)

            # Step 5: Validazione finale
            if not self._final_validation(df):
                return False, df, self.corrections_applied

            return True, df, self.corrections_applied

        except Exception as e:
            self.logger.error(f"Critical error in file validation: {str(e)}")
            self.corrections_applied.append(f"❌ Errore critico: {str(e)}")
            return False, None, self.corrections_applied

    def _load_file_safely(self, file_path: str) -> Optional[pd.DataFrame]:
        """Carica file con gestione errori e fallback encoding"""

        try:
            ext = Path(file_path).suffix.lower()

            if ext == ".csv":
                try:
                    return pd.read_csv(file_path, encoding="utf-8")
                except UnicodeDecodeError:
                    self.corrections_applied.append(
                        "⚠️ UTF-8 encoding fallito, provo alternate..."
                    )
                    # Prova encodings alternativi
                    for encoding in ["latin-1", "iso-8859-1", "cp1252", "utf-16"]:
                        try:
                            df = pd.read_csv(file_path, encoding=encoding)
                            self.corrections_applied.append(
                                f"✅ File caricato con encoding {encoding}"
                            )
                            return df
                        except:
                            continue

                    self.corrections_applied.append(
                        "❌ Impossibile determinare encoding del file"
                    )
                    return None

            elif ext in [".xlsx", ".xls"]:
                return pd.read_excel(file_path)

            elif ext == ".json":
                return pd.read_json(file_path)

            else:
                self.corrections_applied.append(f"❌ Formato file {ext} non supportato")
                return None

        except Exception as e:
            self.corrections_applied.append(f"❌ Errore caricamento file: {str(e)}")
            return None

    def _validate_not_empty(self, df: pd.DataFrame) -> bool:
        """Verifica che il dataframe non sia vuoto"""
        if len(df) == 0:
            self.corrections_applied.append("❌ Il file è vuoto (0 righe)")
            return False

        if len(df.columns) == 0:
            self.corrections_applied.append("❌ Il file non ha colonne")
            return False

        return True

    def _detect_common_issues(self, df: pd.DataFrame) -> List[Tuple[str, any]]:
        """Rileva i problemi comuni nei dati"""

        issues = []

        # 1. Colonne duplicate
        if df.columns.duplicated().any():
            duplicates = df.columns[df.columns.duplicated()].tolist()
            issues.append(("duplicate_columns", duplicates))

        # 2. Righe duplicate
        duplicate_rows = df.duplicated().sum()
        if duplicate_rows > 0:
            issues.append(("duplicate_rows", duplicate_rows))

        # 3. Valori mancanti
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            issues.append(("missing_values", missing_cols))

        # 4. Colonne completamente vuote
        empty_cols = [col for col in df.columns if df[col].isnull().all()]
        if empty_cols:
            issues.append(("empty_columns", empty_cols))

        # 5. Anomalie nei tipi di dati
        for col in df.columns:
            if self._detect_type_mismatch(df, col):
                issues.append(("type_mismatch", col))

        # 6. Outliers estremi (solo per colonne numeriche)
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            outliers = self._detect_outliers(df[col])
            if outliers["count"] > 0 and outliers["count"] < len(df) * 0.1:  # Max 10%
                issues.append(("outliers", (col, outliers)))

        # 7. Spazi bianchi in stringhe
        for col in df.select_dtypes(include=["object"]).columns:
            if self._has_leading_trailing_spaces(df[col]):
                issues.append(("whitespace", col))

        return issues

    def _fix_issue(
        self, df: pd.DataFrame, issue_type: str, details: any
    ) -> Tuple[Optional[pd.DataFrame], str]:
        """Applica correzioni automatiche ai problemi rilevati"""

        if issue_type == "duplicate_columns":
            # Rimuovi colonne duplicate (mantiene la prima)
            df = df.loc[:, ~df.columns.duplicated(keep="first")]
            return df, f"✅ Rimosse {len(details)} colonne duplicate"

        elif issue_type == "duplicate_rows":
            original_len = len(df)
            df = df.drop_duplicates()
            removed = original_len - len(df)
            return df, f"✅ Rimosse {removed} righe duplicate"

        elif issue_type == "missing_values":
            # Imputazione intelligente basata su tipo dati
            for col in details:
                if df[col].dtype in ["int64", "float64"]:
                    # Numeriche: usa mediana
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                elif df[col].dtype == "object":
                    # Categoriche: usa moda (valore più frequente)
                    mode_val = (
                        df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                    )
                    df[col].fillna(mode_val, inplace=True)
                else:
                    # Altre: usa "Unknown"
                    df[col].fillna("Unknown", inplace=True)

            return df, f"✅ Imputati valori mancanti in {len(details)} colonne"

        elif issue_type == "empty_columns":
            # Rimuovi colonne completamente vuote
            df = df.drop(columns=details)
            return df, f"✅ Rimosse {len(details)} colonne vuote"

        elif issue_type == "type_mismatch":
            col = details
            col_copy = df[col].copy()

            # Prova conversione a numerico
            try:
                df[col] = pd.to_numeric(col_copy, errors="coerce")
                # Riempie NaN risultanti dalla conversione
                if df[col].isnull().any():
                    df[col].fillna(df[col].mean(), inplace=True)
                return df, f"✅ Colonna '{col}' convertita a numerico"
            except:
                pass

            # Prova conversione a data
            try:
                df[col] = pd.to_datetime(col_copy, errors="coerce")
                return df, f"✅ Colonna '{col}' convertita a data"
            except:
                pass

            # Se nulla funziona, mantieni come è
            return df, f"⚠️ Colonna '{col}' ha tipo misto, mantenuta come object"

        elif issue_type == "outliers":
            col, outlier_data = details
            lower_bound = outlier_data["lower_bound"]
            upper_bound = outlier_data["upper_bound"]

            # Capping: sostituisci outliers con limite
            original_count = len(df[(df[col] < lower_bound) | (df[col] > upper_bound)])
            df[col] = df[col].clip(lower_bound, upper_bound)

            return df, f"✅ {original_count} outlier in '{col}' corretti (capping)"

        elif issue_type == "whitespace":
            col = details
            if df[col].dtype == "object":
                # Rimuovi spazi bianchi all'inizio e fine
                df[col] = df[col].str.strip()
                return df, f"✅ Rimossi spazi bianchi da '{col}'"

        return None, "❌ Impossibile applicare correzione"

    def _detect_type_mismatch(self, df: pd.DataFrame, col: str) -> bool:
        """Rileva se colonna ha tipo dati potenzialmente sbagliato"""

        try:
            col_data = df[col].dropna()

            if len(col_data) == 0:
                return False

            if col_data.dtype == "object":
                sample = col_data.head(20)

                # Prova numerico
                try:
                    pd.to_numeric(sample)
                    return True
                except:
                    pass

                # Prova data
                try:
                    pd.to_datetime(sample)
                    return True
                except:
                    pass

            return False
        except:
            return False

    def _detect_outliers(self, series: pd.Series) -> Dict:
        """Rileva outliers usando IQR method"""

        if series.dtype not in ["int64", "float64"]:
            return {"count": 0}

        try:
            series_clean = series.dropna()

            if len(series_clean) < 4:
                return {"count": 0}

            Q1 = series_clean.quantile(0.25)
            Q3 = series_clean.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers_mask = (series_clean < lower_bound) | (series_clean > upper_bound)

            return {
                "count": outliers_mask.sum(),
                "q1": float(Q1),
                "q3": float(Q3),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
            }
        except:
            return {"count": 0}

    def _has_leading_trailing_spaces(self, series: pd.Series) -> bool:
        """Verifica se colonna ha spazi bianchi all'inizio/fine"""

        if series.dtype != "object":
            return False

        try:
            string_series = series.astype(str)
            has_spaces = (string_series != string_series.str.strip()).sum() > 0
            return has_spaces
        except:
            return False

    def _final_validation(self, df: pd.DataFrame) -> bool:
        """Validazione finale prima di accettare i dati"""

        # Controlla che almeno una colonna sia utile
        if len(df.columns) == 0:
            self.corrections_applied.append(
                "❌ Nessuna colonna disponibile dopo correzioni"
            )
            return False

        # Controlla che almeno una riga sia presente
        if len(df) == 0:
            self.corrections_applied.append(
                "❌ Nessuna riga disponibile dopo correzioni"
            )
            return False

        return True

    def get_error_summary(self) -> Dict:
        """Restituisce un sommario degli errori e correzioni"""
        return {
            "errors_found": len(self.errors_found),
            "corrections_applied": len(self.corrections_applied),
            "warnings": len(self.warnings),
            "details": {
                "corrections": self.corrections_applied,
                "warnings": self.warnings,
            },
            "timestamp": datetime.now().isoformat(),
        }


class ErrorMessageFormatter:
    """Formatta i messaggi d'errore in modo user-friendly"""

    ERROR_MESSAGES = {
        "file_not_found": "📁 File non trovato. Verifica il percorso e riprova.",
        "encoding_error": "🔤 Problema di codifica file. Prova a salvare come UTF-8.",
        "invalid_format": "📊 Formato non supportato. Usa CSV, Excel o JSON.",
        "empty_file": "📭 Il file è vuoto. Aggiungi dati validi.",
        "no_numeric_data": "🔢 Nessun dato numerico trovato. Aggiungi colonne numeriche.",
        "all_nan_column": "❌ Una o più colonne sono completamente vuote.",
        "memory_error": "💾 Dataset troppo grande. Carica un file più piccolo.",
        "unicode_error": "🔤 Errore di encoding del file.",
        "invalid_data": "⚠️ Dati non validi in una o più colonne.",
    }

    @staticmethod
    def format_error(error_type: str, context: Dict = None) -> str:
        """Formatta messaggio d'errore user-friendly"""

        base_message = ErrorMessageFormatter.ERROR_MESSAGES.get(
            error_type, "❌ Errore sconosciuto"
        )

        if context:
            for key, value in context.items():
                base_message = base_message.replace(f"{{{key}}}", str(value))

        return base_message

    @staticmethod
    def suggest_fix(error_type: str) -> str:
        """Suggerisce una soluzione per l'errore"""

        suggestions = {
            "encoding_error": "Salva il file in formato UTF-8 usando Excel o un editor di testo.",
            "invalid_format": "Converti il file in uno dei formati supportati: CSV, XLSX o JSON.",
            "empty_file": "Assicurati che il file contenga dati con righe e colonne.",
            "no_numeric_data": "Aggiungi almeno una colonna con valori numerici.",
        }

        return suggestions.get(error_type, "Contatta il supporto per assistenza.")
