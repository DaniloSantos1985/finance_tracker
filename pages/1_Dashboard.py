import streamlit as st
import pandas as pd
from utils.data_loader import load_transactions
from utils.finance import calc_monthly_metrics, category_breakdown
from utils.charts import plot_monthly_cashflow, plot_category_pie

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────
# Define o título da aba do navegador e o layout como 'wide'
# para aproveitar toda a largura da tela disponível
st.set_page_config(
    page_title='Dashboard',
    layout='wide'    
)

# Título principal exibido no topo da página
st.title('📊 Dashboard')

# ─── CARREGAMENTO DOS DADOS ──────────────────────────────────────────────────
# Carrega o DataFrame de transações a partir da fonte de dados configurada
# (arquivo CSV, banco de dados, etc.) via função utilitária
df = load_transactions()

# Interrompe a execução se não houver dados disponíveis,
# exibindo uma mensagem informativa ao usuário
if df.empty:
    st.info('Nenhuma transação encontrada. Faça o upload ou crie dados de exemplo em Configurações.')
    st.stop()

# ─── KPIs — INDICADORES-CHAVE DE DESEMPENHO ──────────────────────────────────
# Agrupa as transações pelo campo 'Tipo' (Receita/Despesa) e soma os valores,
# produzindo um Series com os totais por tipo
totais = df.groupby('Tipo')['Quantia'].sum()

# Extrai os totais individualmente; retorna 0 caso o tipo não exista no DataFrame
total_income  = totais.get('Receita', 0)
total_expense = totais.get('Despesa', 0)

# Calcula o saldo líquido (receitas menos despesas)
net = total_income - total_expense

# Cria três colunas de igual largura para exibir os KPIs lado a lado
col1, col2, col3 = st.columns(3)

# ── Receita total ─────────────────────────────────────────────────────────────
# Formata o valor no padrão monetário brasileiro (ponto como separador de milhar,
# vírgula como separador decimal) usando encadeamento de replace:
#   1) ',' → 'x'  (guarda a vírgula original temporariamente)
#   2) '.' → ','  (converte o ponto decimal em vírgula)
#   3) 'x' → '.'  (restaura a vírgula original como ponto de milhar)
col1.metric(
    '**Receita total**',
    f'R$ {total_income:,.2f}'
    .replace(',','x')
    .replace('.',',')
    .replace('x','.')
)

# ── Total de despesas ─────────────────────────────────────────────────────────
# Mesma lógica de formatação monetária aplicada ao total de despesas
col2.metric(
    '**Total de despesa**',
    f'R$ {total_expense:,.2f}'
    .replace(',','x')
    .replace('.',',')
    .replace('x','.')
)

# ── Fluxo de caixa líquido ────────────────────────────────────────────────────
# Exibe o saldo líquido; pode ser positivo (superávit) ou negativo (déficit)
col3.metric(
    '**Fluxo de caixa líquido**',
    f'R$ {net:,.2f}'
    .replace(',','x')
    .replace('.',',')
    .replace('x','.')
)

# Linha divisória visual entre os KPIs e os gráficos
st.divider()

# ─── SEÇÃO DE GRÁFICOS ────────────────────────────────────────────────────────
# Layout assimétrico: gráfico de linha ocupa 2/3 da largura (peso 2),
# gráfico de pizza ocupa 1/3 (peso 1)
col1, col2 = st.columns([2, 1])

# ── Gráfico de fluxo de caixa mensal (linha/barras) ──────────────────────────
with col1:
    # Calcula as métricas mensais agregadas (receita, despesa, saldo por mês)
    monthly = calc_monthly_metrics(df)

    # Só renderiza o gráfico se houver dados mensais disponíveis
    if not monthly.empty:
        st.plotly_chart(
            plot_monthly_cashflow(monthly),  # retorna figura Plotly
            width='stretch'                  # ocupa toda a largura da coluna
        )

# ── Gráfico de pizza por categoria ───────────────────────────────────────────
with col2:
    # Calcula o total gasto por categoria para alimentar o gráfico de pizza
    cat = category_breakdown(df)
    st.plotly_chart(
        plot_category_pie(cat),  # retorna figura Plotly
        width='stretch'
    )

# Linha divisória visual entre os gráficos e a tabela
st.divider()

# ─── EXIBIÇÃO DO DATAFRAME ───────────────────────────────────────────────────
# Envolve a tabela em um expander para economizar espaço na tela;
# o usuário expande manualmente quando quiser visualizar as transações
with st.expander('Visualização de transações filtradas'):

    st.dataframe(
        # Ordena por data decrescente (mais recentes no topo)
        # e limita a exibição às 50 transações mais recentes
        df.sort_values('Data', ascending=False).head(50),

        width='stretch',   # tabela ocupa toda a largura do expander

        # column_config personaliza a aparência e o comportamento de cada coluna
        column_config={

            # Coluna 'Data': tipo DateColumn com formato brasileiro DD/MM/AAAA
            'Data': st.column_config.DateColumn(
                'Data da transação',
                format='DD/MM/YYYY'
            ),

            # Coluna 'Quantia': tipo NumberColumn formatado como moeda (R$)
            # 'help' exibe um tooltip ao passar o mouse no cabeçalho
            'Quantia': st.column_config.NumberColumn(
                'Valor (R$)',
                format='R$ %.2f',
                help='Valor monetário movimentado'
            ),

            # Coluna 'Categoria': tipo TextColumn com tooltip explicativo
            'Categoria': st.column_config.TextColumn(
                'Categoria',
                help='Classificação da despesa ou receita'
            ),

            # Coluna 'Tipo': tipo TextColumn indicando se é receita ou despesa
            'Tipo': st.column_config.TextColumn(
                'Tipo',
                help='Indica se é despesa ou receita'
            )
        }
    )