# ─── IMPORTAÇÕES ─────────────────────────────────────────────────────────────

import streamlit as st
from utils.data_loader import load_transactions
import pandas as pd
from pathlib import Path


# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────

# Configura o título da aba do navegador e define o layout para ocupar a largura total
st.set_page_config(
    page_title='Configuraçoes',
    layout='wide'
)

# Título principal exibido no topo da página de configurações
st.title('⚙️ Configurações e Gerenciamento de Dados')


# ─── CONTROLES DO CONJUNTO DE DADOS ──────────────────────────────────────────

st.header('Controles de conjunto de dados')

# Carrega as transações atuais através da função utilitária
df = load_transactions()

# Exibe uma caixa informativa com o número total de registos (linhas) na base de dados
st.info(f'Conjunto de Dados Atuais: {len(df)} linhas')

# Botão para regenerar/sobrescrever os dados de exemplo do sistema
if st.button('Regerar dados de exemplo (sobrescrever)'):
    import subprocess, sys
    # Executa o script externo de criação de dados usando o interpretador Python atual
    subprocess.run([sys.executable, 'data/create_data_sample.py'])
    st.success('Dados de exemplo regenerados. Recarregue as páginas do aplicativo para ver as alterações.')


# ─── EXPORTAÇÃO E IMPORTAÇÃO ─────────────────────────────────────────────────

st.divider()
st.header('Export/Import')
st.write('- Utilize a página de Transações para enviar ou baixar arquivos CSV.')


# ─── PERSISTÊNCIA E VERIFICAÇÃO DE FICHEIROS ──────────────────────────────────

st.divider()
st.header('Persistência')

# Verifica através da biblioteca pathlib se o ficheiro CSV de dados existe no disco
if Path('data/sample_transactions.csv').exists():
    st.write('Localização da Base de Dados: data\\sample_transactions.csv')
else:
    st.warning('Nenhuma Base de Dados encontradas em data/')


# ─── FERRAMENTAS DA APLICAÇÃO E ESTADO DE SESSÃO ──────────────────────────────

st.divider()
st.header('Ferramentas APP')

# Inicializa a variável 'auto_refresh' no session_state caso ainda não exista
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False

# Cria uma caixa de seleção (checkbox) ligada diretamente ao estado da sessão
st.session_state.auto_refresh = st.checkbox(
    'Atualização automática ao alterar o arquivo (apenas na sessão atual)',
    value=st.session_state.auto_refresh
)

st.success('Ferramentas salva na sessão de estado (session state)')