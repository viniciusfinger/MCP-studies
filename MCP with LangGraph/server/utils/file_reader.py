import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def read_csv_summary(filename: str) -> str:
    """
    Read a CSV file and return a simple summary.
    Args:
        filename: Name of the CSV file (e.g. 'sample.csv')
    Returns:
        A string describing the file's contents.
    """
    print(f"Reading CSV file: {filename}")
    
    file_path = DATA_DIR / filename
    
    # Verificar se o arquivo existe
    if not file_path.exists():
        return f"Error: The file '{filename}' does not exist in the 'data' directory."
    
    df = pd.read_csv(file_path)

    return f"CSV file '{filename}' has {len(df)} rows and {len(df.columns)} columns."


def read_parquet_summary(filename: str) -> str:
    """
    Read a Parquet file and return a simple summary.
    Args:
        filename: Name of the Parquet file (e.g. 'sample.parquet')
    Returns:
        A string describing the file's contents.
    """
    print(f"Reading Parquet file: {filename}")
    file_path = DATA_DIR / filename
    
    # Verificar se o arquivo existe
    if not file_path.exists():
        return f"Erro: Arquivo '{filename}' não encontrado na pasta data."
    
    df = pd.read_parquet(file_path)
    
    return f"Parquet file '{filename}' has {len(df)} rows and {len(df.columns)} columns."