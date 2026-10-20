# ─── IMPORTAÇÕES ─────────────────────────────────────────────────────────────

import streamlit as st                          # Framework para criação da interface web
from utils.data_loader import load_transactions # Função para carregar as transações do CSV

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────

# Define título da aba do navegador e layout em tela cheia
st.set_page_config(
    page_title='Rastreador de Finanças Pessoais',
    layout='wide'
)

# ─── CABEÇALHO DA PÁGINA ─────────────────────────────────────────────────────

# Título principal exibido no topo da página
st.title('💰 Rastreador de Finanças Pessoais e Planejador de Orçamento')

# Texto introdutório com as funcionalidades do app
# Renderizado em Markdown — suporta títulos, listas e negrito
st.markdown("""
Este projeto ajuda você a acompanhar transações, definir orçamentos e visualizar suas finanças pessoais.

Use a barra lateral para navegar: Painel, Transações, Planejador de Orçamento, Configurações.
""")

# ─── CARREGAMENTO DOS DADOS ──────────────────────────────────────────────────

# st.spinner → exibe um ícone de carregamento enquanto os dados são lidos do CSV
# load_transactions() usa @st.cache_data — após a primeira execução
# os dados ficam em cache e não são recarregados desnecessariamente
with st.spinner('Carregando as transações...'):
    df = load_transactions()

    # Exibe mensagem de sucesso com o total de transações carregadas
    st.success(f'Carregado {len(df)} transações')

# ─── LINKS RÁPIDOS ───────────────────────────────────────────────────────────

# Linha divisória horizontal
st.write('---')

st.markdown('### Links Rápidos')

# st.page_link → cria links clicáveis para as páginas do app
# label → texto exibido no link com emoji para identificação visual
st.page_link('pages/1_Dashboard.py',                   label='📊 Abrir Dashboard')
st.page_link('pages/2_Transações.py',                  label='📋 Transações')
st.page_link('pages/3_Planejador_de_Orçamento.py',     label='🧾 Planejador de Orçamento')
st.page_link('pages/4_Ferramentas.py',                 label='⚙️ Ferramentas')