# ─── IMPORTAÇÕES ─────────────────────────────────────────────────────────────

import pandas as pd  # Manipulação e agregação de dados

# ─── FUNÇÃO: MÉTRICAS MENSAIS ─────────────────────────────────────────────────

def calc_monthly_metrics(df: pd.DataFrame):
    """
    Calcula as métricas mensais de Receita, Despesa e Saldo Líquido.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo as transações.

    Retorna:
    pd.DataFrame: DataFrame com colunas Mês, Receita, Despesa e Líquido.
                  Retorna DataFrame vazio se a entrada estiver vazia.
    """

    # Retorna DataFrame vazio se não houver dados
    # Evita erros ao tentar processar um DataFrame sem linhas
    if df.empty:
        return pd.DataFrame()

    # Cria uma cópia para não modificar o DataFrame original
    df2 = df.copy()

    # Garante que a coluna 'Data' está no formato datetime
    df2['Data'] = pd.to_datetime(df2['Data'])

    # Cria a coluna 'Mês' agrupando as datas por período mensal
    # to_period('M') → converte cada data para o período do mês (ex: 2026-01)
    # dt.start_time  → converte de volta para datetime no 1º dia do mês
    # Exemplo: 15/01/2026 → 01/01/2026
    df2['Mês'] = df2['Data'].dt.to_period('M').dt.start_time

    # Filtra apenas Receitas e soma o total por mês
    inc = df2[df2['Tipo'] == 'Receita'].groupby('Mês')['Quantia'].sum()

    # Filtra apenas Despesas e soma o total por mês
    exp = df2[df2['Tipo'] == 'Despesa'].groupby('Mês')['Quantia'].sum()

    # Combina Receita e Despesa em um único DataFrame
    # fillna(0) → substitui NaN por 0 nos meses sem transações de um dos tipos
    res = pd.DataFrame({
        'Receita': inc,
        'Despesa': exp
    }).fillna(0)

    # Calcula o saldo líquido mensal
    # Positivo → sobrou dinheiro | Negativo → gastou mais do que recebeu
    res['Líquido'] = res['Receita'] - res['Despesa']

    # reset_index() → transforma o índice 'Mês' de volta em coluna
    return res.reset_index()


# ─── FUNÇÃO: BREAKDOWN POR CATEGORIA ─────────────────────────────────────────

def category_breakdown(df: pd.DataFrame):
    """
    Calcula o total de despesas agrupado por categoria, do maior para o menor.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo as transações.

    Retorna:
    pd.DataFrame: DataFrame com colunas Categoria e Quantia ordenadas
                  de forma decrescente. Retorna DataFrame vazio se a
                  entrada estiver vazia.
    """

    # Retorna DataFrame vazio se não houver dados
    if df.empty:
        return pd.DataFrame()

    return (
        df[df['Tipo'] == 'Despesa']      # Filtra apenas as linhas do tipo Despesa
        .groupby('Categoria')['Quantia'] # Agrupa por categoria e seleciona a coluna Quantia
        .sum()                           # Soma o total gasto em cada categoria
        .sort_values(ascending=False)    # Ordena do maior para o menor gasto
        .reset_index()                   # Transforma o índice 'Categoria' de volta em coluna
    )