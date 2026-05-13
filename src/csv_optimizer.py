"""
CSV Optimizer - Caricamento veloce e ottimizzato per file grandi
Implementa parallel processing, chunking, e type inference intelligente
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, List
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import os

warnings.filterwarnings("ignore")


class CSVOptimizer:
    """Ottimizza caricamento CSV per velocità massima"""

    def __init__(self, max_workers: int = 4, chunk_size: int = 50000):
        """
        Inizializza optimizer

        Args:
            max_workers: Numero di worker paralleli
            chunk_size: Dimensione chunk per parallel processing
        """
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.cache = {}

    def infer_dtype_optimized(self, series: pd.Series) -> str:
        """
        Inferisce tipo dato in modo veloce (ottimizzato)

        Args:
            series: Pandas Series

        Returns:
            str: Tipo dato rilevato
        """
        if series.empty:
            return "object"

        # Sample per performance (primi 5000 elementi)
        sample = series.head(5000).dropna()
        if len(sample) == 0:
            return "object"

        # Prova numerico
        try:
            pd.to_numeric(sample)
            return "float32"  # uint8 per numeri piccoli
        except (ValueError, TypeError):
            pass

        # Prova datetime
        try:
            pd.to_datetime(sample)
            return "datetime64[ns]"
        except (ValueError, TypeError):
            pass

        # Prova boolean
        if set(sample.unique()).issubset(
            {True, False, "True", "False", "true", "false", "1", "0", 1, 0}
        ):
            return "bool"

        # Default object
        return "object"

    def read_csv_fast(
        self, filepath: str, encoding: str = "utf-8"
    ) -> Tuple[bool, pd.DataFrame, List[str]]:
        """
        Legge CSV con ottimizzazioni di velocità

        Args:
            filepath: Path al file CSV
            encoding: Encoding del file

        Returns:
            Tuple: (success, dataframe, optimizations_applied)
        """
        optimizations = []

        try:
            # Step 1: Leggi header solamente per tipo inference
            df_head = pd.read_csv(filepath, nrows=5000, encoding=encoding)
            optimizations.append("✅ Header read (5000 righe sample)")

            # Step 2: Infer dtype ottimizzati
            dtype_dict = {}
            for col in df_head.columns:
                inferred = self.infer_dtype_optimized(df_head[col])
                dtype_dict[col] = inferred

            # Usa low_memory=False per evitare warning
            df = pd.read_csv(
                filepath,
                encoding=encoding,
                dtype=dtype_dict,
                low_memory=False,
            )
            optimizations.append(
                f"✅ Type inference applicate ({len(dtype_dict)} colonne)"
            )

            # Step 3: Ottimizzazioni di memoria
            memory_before = df.memory_usage(deep=True).sum() / 1024**2
            df = self._optimize_memory(df)
            memory_after = df.memory_usage(deep=True).sum() / 1024**2
            memory_saved = memory_before - memory_after
            if memory_saved > 0:
                optimizations.append(f"✅ Memoria salvata: {memory_saved:.1f} MB")

            return True, df, optimizations

        except Exception as e:
            return False, None, [f"❌ Errore: {str(e)}"]

    def _optimize_memory(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ottimizza memoria del dataframe

        Args:
            df: Input dataframe

        Returns:
            pd.DataFrame: Dataframe ottimizzato
        """
        df = df.copy()

        for col in df.columns:
            col_type = df[col].dtype

            # Ottimizza interi
            if col_type != "object":
                c_min = df[col].min() if len(df[col].dropna()) > 0 else 0
                c_max = df[col].max() if len(df[col].dropna()) > 0 else 0

                if str(col_type)[:3] == "int":
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif (
                        c_min > np.iinfo(np.int16).min
                        and c_max < np.iinfo(np.int16).max
                    ):
                        df[col] = df[col].astype(np.int16)
                    elif (
                        c_min > np.iinfo(np.int32).min
                        and c_max < np.iinfo(np.int32).max
                    ):
                        df[col] = df[col].astype(np.int32)
                else:
                    # Float optimization
                    if (
                        c_min > np.finfo(np.float32).min
                        and c_max < np.finfo(np.float32).max
                    ):
                        df[col] = df[col].astype(np.float32)

            # Ottimizza stringhe → categoria
            elif col_type == "object":
                num_unique_values = len(df[col].unique())
                num_total_values = len(df[col])
                if num_unique_values / num_total_values < 0.05:
                    df[col] = df[col].astype("category")

        return df

    def read_csv_chunked(
        self, filepath: str, encoding: str = "utf-8"
    ) -> Tuple[bool, pd.DataFrame, List[str]]:
        """
        Legge CSV in chunk per file molto grandi (>500MB)

        Args:
            filepath: Path al file CSV
            encoding: Encoding del file

        Returns:
            Tuple: (success, dataframe, optimizations_applied)
        """
        optimizations = []

        try:
            chunks = []
            chunk_num = 0

            for chunk in pd.read_csv(
                filepath, encoding=encoding, chunksize=self.chunk_size, low_memory=False
            ):
                chunk = self._optimize_memory(chunk)
                chunks.append(chunk)
                chunk_num += 1

            df = pd.concat(chunks, ignore_index=True)
            optimizations.append(
                f"✅ Chunked read ({chunk_num} chunk x {self.chunk_size} righe)"
            )

            return True, df, optimizations

        except Exception as e:
            return False, None, [f"❌ Errore: {str(e)}"]

    def read_csv_adaptive(
        self, filepath: str, encoding: str = "utf-8"
    ) -> Tuple[bool, pd.DataFrame, List[str]]:
        """
        Sceglie automaticamente il metodo di lettura ottimale

        Args:
            filepath: Path al file CSV
            encoding: Encoding del file

        Returns:
            Tuple: (success, dataframe, optimizations_applied)
        """
        optimizations = []

        try:
            # Verifica dimensione file
            file_size_mb = os.path.getsize(filepath) / 1024**2
            optimizations.append(f"📊 Dimensione file: {file_size_mb:.1f} MB")

            # Scegli metodo in base a dimensione
            if file_size_mb < 100:
                # File piccolo → lettura veloce normale
                success, df, opts = self.read_csv_fast(filepath, encoding)
            else:
                # File grande → chunked reading
                success, df, opts = self.read_csv_chunked(filepath, encoding)
                optimizations.extend(opts)

            if success:
                optimizations.insert(0, "✅ Lettura completata con ottimizzazioni")
                optimizations.append(
                    f"✅ Righe: {len(df):,}, Colonne: {len(df.columns)}"
                )

            return success, df, optimizations

        except Exception as e:
            return False, None, [f"❌ Errore: {str(e)}"]

    def get_cache_stats(self) -> dict:
        """
        Ritorna statistiche cache

        Returns:
            dict: Statistiche di cache
        """
        return {
            "cached_files": len(self.cache),
            "total_cached_size_mb": sum(
                df.memory_usage(deep=True).sum() / 1024**2 for df in self.cache.values()
            ),
        }

    def clear_cache(self):
        """Svuota cache"""
        self.cache.clear()


# ============================================================================
# FUNZIONE HELPER SEMPLIFICATA
# ============================================================================


def load_csv_optimized(
    filepath: str, encoding: str = "utf-8"
) -> Tuple[bool, pd.DataFrame, List[str]]:
    """
    Helper function per caricamento CSV ottimizzato

    Args:
        filepath: Path al file CSV
        encoding: Encoding

    Returns:
        Tuple: (success, df, optimizations)
    """
    optimizer = CSVOptimizer()
    return optimizer.read_csv_adaptive(filepath, encoding)
