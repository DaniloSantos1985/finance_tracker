# ─── IMPORTAÇÕES ─────────────────────────────────────────────────────────────

import pandas as pd          # Manipulação e agregação de dados
import plotly.express as px  # Criação de gráficos interativos de alto nível


# ─── FUNÇÃO: GRÁFICO DE FLUXO DE CAIXA MENSAL ────────────────────────────────

def plot_monthly_cashflow(df_monthly):
    """
    Cria um gráfico de barras agrupadas comparando Receita e Despesa por mês.

    Parâmetros:
    df_monthly (pd.DataFrame): DataFrame contendo as colunas Mês, Receita e Despesa.

    Retorna:
    plotly.express.Figure:  Objeto da figura do gráfico de barras.
                            Retorna um dicionário vazio se a entrada estiver vazia.
    """

    # Retorna dicionário vazio se não houver dados
    # Evita erros do Plotly ao tentar renderizar um gráfico sem linhas
    if df_monthly.empty:
        return {}

    # Cria o gráfico de barras agrupadas com Plotly Express
    # x='Mês' → eixo horizontal com os meses
    # y=['Receita', 'Despesa'] → colunas numéricas a serem plotadas
    # barmode='group' → exibe as barras de receita e despesa lado a lado para cada mês
    fig = px.bar(
        df_monthly,
        x='Mês',
        y=['Receita', 'Despesa'],
        barmode='group',
        title='Receita Mensal vs Despesas'
    )

    return fig


# ─── FUNÇÃO: GRÁFICO DE PIZZA (DONUT) POR CATEGORIA ──────────────────────────

def plot_category_pie(df_cat):
    """
    Cria um gráfico de pizza em formato rosquinha (donut) mostrando os gastos por categoria.

    Parâmetros:
    df_cat (pd.DataFrame): DataFrame contendo as colunas Categoria e Quantia.

    Retorna:
    plotly.express.Figure: Objeto da figura do gráfico de pizza.
                          Retorna um dicionário vazio se a entrada estiver vazia.
    """

    # Retorna dicionário vazio se não houver dados
    if df_cat.empty:
        return {}

    # Cria o gráfico de pizza (donut) com Plotly Express
    # values='Quantia' → tamanho de cada fatia baseado no valor gasto
    # names='Categoria' → rótulo/nome de cada categoria
    # hole=0.4 → cria o furo central, transformando a pizza em gráfico de rosca (40% do raio)
    fig = px.pie(
        df_cat,
        values='Quantia',
        names='Categoria',
        title='Despesa por Categoria',
        hole=0.4
    )

    return fig