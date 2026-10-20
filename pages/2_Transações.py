import streamlit as st
import pandas as pd
from utils.data_loader import load_transactions, save_transactions

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────
st.set_page_config(
    page_title='Transações',
    layout='wide'       # layout wide aproveita toda a largura da tela
)

st.title('📋 Transações')

# ─── CARREGAMENTO DOS DADOS ──────────────────────────────────────────────────
# Carrega o DataFrame persistido em disco (CSV) via função utilitária;
# é reutilizado tanto para exibição/edição quanto para o download ao final
df = load_transactions()

# ─── LAYOUT PRINCIPAL: TABELA EDITÁVEL + PAINEL DE AÇÕES ────────────────────
# Divisão assimétrica: editor de dados ocupa 3/4 da largura (peso 3),
# painel de ações ocupa 1/4 (peso 1)
col1, col2 = st.columns([3, 1])

# ─── COLUNA 1: EDITOR DE TRANSAÇÕES ─────────────────────────────────────────
with col1:
    st.subheader('Transações (editadas)')

    # st.data_editor renderiza o DataFrame como uma tabela interativa:
    # · num_rows='dynamic' → permite adicionar e remover linhas diretamente na UI
    # · width='stretch'    → a tabela ocupa toda a largura da coluna
    edited = st.data_editor(
        df,
        num_rows='dynamic',
        width='stretch',

        # column_config personaliza aparência e comportamento coluna a coluna
        column_config={

            # DateColumn exibe e valida datas; format define o padrão visual (BR)
            'Data': st.column_config.DateColumn(
                'Data da transação',
                format='DD/MM/YYYY'
            ),

            # NumberColumn garante entrada numérica e formata como moeda;
            # 'help' aparece como tooltip no cabeçalho da coluna
            'Quantia': st.column_config.NumberColumn(
                'Valor (R$)',
                format='R$ %.2f',
                help='Valor monetário movimentado'
            ),

            # TextColumn para campos de texto livre com tooltip explicativo
            'Categoria': st.column_config.TextColumn(
                'Categoria',
                help='Classificação da despesa ou receita'
            ),

            # TextColumn indicando se a linha representa receita ou despesa
            'Tipo': st.column_config.TextColumn(
                'Tipo',
                help='Indica se é despesa ou receita'
            )
        }
    )

    # Instrução visível abaixo da tabela orientando o fluxo de edição
    st.caption(
        'Edite as linhas diretamente no local. '
        'Adicione ou remova linhas. '
        'Clique em "Salvar", abaixo, para confirmar as alterações.'
    )

# ─── COLUNA 2: PAINEL DE AÇÕES ───────────────────────────────────────────────
with col2:
    st.subheader('Ações')

    # ── Upload de CSV externo ─────────────────────────────────────────────────
    # file_uploader aceita apenas arquivos .csv; retorna None enquanto vazio
    uploader = st.file_uploader(
        'Enviar arquivo CSV para substituir o conjunto de dados',
        type=['csv']
    )

    if uploader:
        try:
            # parse_dates converte automaticamente a coluna 'Data' para datetime,
            # evitando erros de tipo nas operações posteriores
            new_df = pd.read_csv(uploader, parse_dates=['Data'])
            st.success(f'Carregado {len(new_df)} linhas. Prévia abaixo.')

            # Exibe apenas as 5 primeiras linhas como pré-visualização rápida
            st.dataframe(new_df.head())

            # Botão de confirmação: só substitui o dataset após clique explícito,
            # evitando sobrescrita acidental ao fazer upload
            if st.button('Salvar o CSV carregado como dataset'):
                new_df.to_csv('data/sample_transations.csv', index=False)
                st.success(
                    'Conjunto de dados enviado, salvo. '
                    'Atualize as páginas para recarregar.'
                )

        except Exception as e:
            # Captura qualquer erro de leitura (encoding, colunas faltando, etc.)
            # e exibe mensagem amigável sem travar o app
            st.error(f'Erro para ler o CSV: {e}')

    # ── Salvar edições feitas diretamente na tabela ───────────────────────────
    # 'edited' contém o DataFrame com todas as alterações feitas pelo usuário
    # no st.data_editor acima; save_transactions persiste essas mudanças em disco
    if st.button('Salvar transações editadas'):
        save_transactions(edited)
        st.success('Alterações salvas em data/sample_transactins.csv')
        st.info(
            'Recarregue as páginas do aplicativo para visualizar as alterações'
        )

# ─── SEÇÃO DE DOWNLOAD ───────────────────────────────────────────────────────
st.divider()
st.write('Download do conjunto de dados atuais.')

# Serializa o DataFrame para CSV em memória (sem salvar em disco),
# codificado em UTF-8 para garantir compatibilidade com acentos e caracteres PT-BR
csv = df.to_csv(index=False).encode('utf-8')

# download_button envia o arquivo diretamente ao navegador do usuário;
# file_name define o nome sugerido ao salvar
st.download_button(
    'Download do CSV',
    csv,
    file_name='transactions_export.csv'
)