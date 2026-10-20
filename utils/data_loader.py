# ─── IMPORTAÇÕES ─────────────────────────────────────────────────────────────

import pandas as pd                # Manipulação e leitura de dados
import streamlit as st             # Interface web e sistema de cache
from pathlib import Path           # Manipulação de caminhos de arquivos

# ─── CAMINHOS DOS ARQUIVOS ───────────────────────────────────────────────────

# Path → cria um objeto de caminho compatível com qualquer sistema operacional
# Windows: data\sample_transactions.csv | Mac/Linux: data/sample_transactions.csv
DATA_CSV = Path('data/sample_transactions.csv')  # Arquivo CSV com as transações
DB_PATH  = Path('data/finance.db')               # Arquivo do banco de dados SQLite (reservado para uso futuro)

# ─── FUNÇÃO: CARREGAR TRANSAÇÕES ─────────────────────────────────────────────

# @st.cache_data → armazena o resultado em cache após a primeira execução
# Evita recarregar o CSV toda vez que o usuário interage com a página
# O cache é invalidado automaticamente quando o arquivo CSV é alterado
@st.cache_data
def load_transactions(csv_path: str = str(DATA_CSV)):
    """
    Carrega as transações do arquivo CSV e retorna um DataFrame do pandas.

    Parâmetros:
    csv_path (str): Caminho para o arquivo CSV. Usa DATA_CSV como padrão.

    Retorna:
    pd.DataFrame: DataFrame com as transações carregadas.
                  Retorna DataFrame vazio se o arquivo não for encontrado.
    """
    try:
        # Lê o arquivo CSV convertendo a coluna 'Data' para datetime automaticamente
        # parse_dates=['Data'] → converte a coluna diretamente na leitura
        df = pd.read_csv(csv_path, parse_dates=['Data'])

        # Remove a parte de hora da coluna 'Data' mantendo apenas a data
        # dt.date → extrai apenas a data (sem hora)
        # pd.to_datetime → reconverte para datetime (necessário para operações de data)
        df['Data'] = pd.to_datetime(df['Data'].dt.date, errors='coerce')

        return df

    except FileNotFoundError:
        # Retorna um DataFrame vazio com as colunas corretas
        # Evita que o app quebre caso o arquivo CSV não exista ainda
        return pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Tipo', 'Quantia'])


# ─── FUNÇÃO: SALVAR TRANSAÇÕES ────────────────────────────────────────────────

def save_transactions(df: pd.DataFrame, csv_path: str = str(DATA_CSV)):
    """
    Salva o DataFrame de transações no arquivo CSV.

    Parâmetros:
    df (pd.DataFrame): DataFrame com as transações a serem salvas.
    csv_path (str): Caminho para o arquivo CSV. Usa DATA_CSV como padrão.
    """
    # Salva o DataFrame como CSV
    # index=False → não inclui a coluna de índice numérico no arquivo
    df.to_csv(csv_path, index=False)