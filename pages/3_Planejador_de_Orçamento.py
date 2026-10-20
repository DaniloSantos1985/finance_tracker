import streamlit as st
import pandas as pd
from utils.data_loader import load_transactions
from utils.finance import category_breakdown

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────
st.set_page_config(
    page_title='Planejador de Orçamento',
    layout='wide'
)

st.title('🧾 Planejador de Orçamento')

# ─── CARREGAMENTO DOS DADOS ──────────────────────────────────────────────────
# Carrega todas as transações persistidas em disco via função utilitária
df = load_transactions()

# Extrai as categorias únicas em ordem alfabética para popular
# os inputs de orçamento e o dicionário do session_state
categories = sorted(df['Categoria'].unique().tolist())

# ─── SIDEBAR: SELEÇÃO DO MÊS ─────────────────────────────────────────────────
st.sidebar.header('Ferramenta de Planejamento Mensal')

# date_input retorna um objeto date; o valor padrão é a data de hoje
budget_month = st.sidebar.date_input(
    'Mês do orçamento (escolha qualquer data dentro do mês)',
    value=pd.to_datetime('today')
)

# Converte a data selecionada para o primeiro dia do mês correspondente:
# to_period('M') → período mensal (ex.: 2024-03)
# .start_time    → primeiro instante do período (2024-03-01 00:00:00)
# Isso normaliza qualquer dia escolhido dentro do mês para um único valor
# comparável com a coluna 'Mês' criada mais adiante
budget_month = pd.to_datetime(budget_month).to_period('M').start_time

# ─── TRADUÇÃO DE MESES PARA PORTUGUÊS ────────────────────────────────────────
# Dicionário de mapeamento numérico → nome do mês em PT-BR
# Evita dependência de locale do sistema operacional do servidor,
# que pode variar entre ambientes (Windows, Linux, cloud)
meses_pt = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março',    4: 'Abril',
    5: 'Maio',    6: 'Junho',     7: 'Julho',     8: 'Agosto',
    9: 'Setembro',10: 'Outubro',  11: 'Novembro', 12: 'Dezembro'
}

# Obtém o nome do mês e o ano a partir do Timestamp normalizado
nome_mes = meses_pt[budget_month.month]
ano      = budget_month.year

# ─── SESSION STATE: ORÇAMENTOS POR CATEGORIA ────────────────────────────────
# session_state persiste valores entre reruns do Streamlit sem recarregar a página;
# inicializa o dicionário apenas na primeira execução (guard 'not in')
# Valor padrão de R$ 500,00 por categoria — pode ser ajustado pelo usuário
if 'budgets' not in st.session_state:
    st.session_state.budgets = {c: 500.0 for c in categories}

# ─── LAYOUT: INPUTS DE ORÇAMENTO | TABELA DE COMPARAÇÃO ─────────────────────
# col1 (peso 2) → inputs numéricos por categoria
# col2 (peso 3) → tabela comparativa gasto vs orçamento + alertas
col1, col2 = st.columns([2, 3])

# ─── COLUNA 1: INPUTS DE ORÇAMENTO ───────────────────────────────────────────
with col1:
    st.subheader(f'Planejamento para {nome_mes} de {ano}')

    for c in categories:
        # number_input renderiza um campo numérico editável para cada categoria;
        # o valor atual vem do session_state (.get com fallback de R$ 200,00)
        # key único por categoria evita conflito de estado entre os widgets
        st.session_state.budgets[c] = st.number_input(
            f'Orçamento de {c}',
            value=float(st.session_state.budgets.get(c, 200.0)),
            key=f'bud_{c}'
        )

# ─── COLUNA 2: COMPARAÇÃO GASTO VS ORÇAMENTO ────────────────────────────────
with col2:
    st.subheader(f'Gastos por categoria versus orçamento ({nome_mes} de {ano})')

    # ── Filtro de transações pelo mês selecionado ─────────────────────────────
    df2 = df.copy()                                          # preserva o df original
    df2['Data'] = pd.to_datetime(df['Data'])                 # garante tipo datetime

    # Cria coluna auxiliar 'Mês' com o primeiro dia de cada mês,
    # no mesmo formato de budget_month, para comparação direta
    df2['Mês'] = df2['Data'].dt.to_period('M').dt.start_time

    # Filtra apenas as linhas cujo mês coincide com o selecionado na sidebar
    month_df = df2[df2['Mês'] == budget_month]

    # Agrega o total gasto por categoria no mês, apenas para despesas
    spent = (
        month_df[month_df['Tipo'] == 'Despesa']
        .groupby('Categoria')['Quantia']
        .sum()
        .reset_index()
    )

    # Converte para dicionário {categoria: total_gasto} para consulta O(1)
    spent = spent.set_index('Categoria')['Quantia'].to_dict()

    # ── Construção da tabela de visão geral ───────────────────────────────────
    overview = []

    for c, b in st.session_state.budgets.items():
        s   = round(spent.get(c, 0.0), 2)   # gasto real; 0 se não houver registro
        pct = s / b if b > 0 else 0         # porcentagem gasta; evita divisão por zero

        # Regra de status:
        # · pct < 0.80 → 'Ok'       (abaixo de 80 % do orçamento)
        # · pct < 1.00 → 'Aviso'    (entre 80 % e 100 %)
        # · pct >= 1.0 → 'Excedido' (estourou o orçamento)
        status = 'Ok' if pct < 0.8 else ('Aviso' if pct < 1.0 else 'Excedido')

        overview.append((c, b, s, pct, status))

    # Monta o DataFrame de visão geral com colunas nomeadas explicitamente
    df_over = pd.DataFrame(
        overview,
        columns=['Categoria', 'Orçamento', 'Gastos', 'Porcentagem de Gastos', 'Status']
    )

    # Exibe a tabela ordenada do maior para o menor percentual de gasto,
    # destacando as categorias mais críticas no topo
    st.dataframe(
        df_over.sort_values('Porcentagem de Gastos', ascending=False),
        width='stretch',
        column_config={

            # Colunas monetárias formatadas como R$ com 2 casas decimais
            'Orçamento': st.column_config.NumberColumn(
                'Orçamento',
                format='R$ %.2f',
                help='Limite de gasto definido para a categoria'
            ),
            'Gastos': st.column_config.NumberColumn(
                'Gastos',
                format='R$ %.2f',
                help='Total gasto na categoria no mês selecionado'
            ),

            # Porcentagem exibida com 2 casas decimais (ex.: 0.75 → "0.75")
            # Idealmente usar format='%.0%%' para exibir como "75 %"
            'Porcentagem de Gastos': st.column_config.NumberColumn(
                'Gastos (%)',
                format='%.2f',
            )
        }
    )
  
    # ─── ALTERNATIVA 1: Substituir caixas de alerta por texto com ícones ─────────

    for _, row in df_over.iterrows():
        gasto     = row['Gastos']
        orcamento = row['Orçamento']
        categoria = row['Categoria']

    # Define o ícone correspondente ao status
        if row['Status'] == 'Excedido':
            icone = "🔴"
        elif row['Status'] == 'Aviso':
            icone = "🟡"
        else:
            icone = "🟢"
    
        # Exibe em linha limpa (sem caixas grandes ocupando a tela inteira)
        st.markdown(f"{icone} **{categoria}** — Gasto: R\$ {gasto:.2f} / R\$ {orcamento:.2f} ({row['Status']})")

# ─── BOTÃO DE PERSISTÊNCIA DOS ORÇAMENTOS ────────────────────────────────────
# Os orçamentos definidos são mantidos apenas no session_state (memória da sessão);
# ao recarregar o app eles são perdidos, a menos que sejam salvos em arquivo
# nas Configurações (funcionalidade a ser implementada)
if st.button('Salvar orçamento (sessão)'):
    st.success(
        'Os orçamentos foram salvos na sessão. '
        'Se desejar torná-los permanentes, salve-os em um arquivo nas Configurações.'
    )