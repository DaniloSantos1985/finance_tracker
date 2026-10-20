# ─── IMPORTAÇÕES ─────────────────────────────────────────────────────────────

import pandas as pd                      # Manipulação de dados e exportação CSV
import numpy as np                       # Geração de números aleatórios
from datetime import datetime, timedelta # Manipulação de datas

# ─── CONFIGURAÇÃO INICIAL ────────────────────────────────────────────────────
# Define uma semente fixa para o gerador de números aleatórios
# Garante que os dados gerados sejam sempre os mesmos a cada execução
np.random.seed(42)

# Define o número de dias a gerar — 365 dias (1 ano)
n_days = 365

# Calcula a data de início — hoje menos 364 dias
# O -1 garante que o intervalo termine exatamente hoje
start = datetime.today() - timedelta(days=n_days - 1)

# Gera uma lista de 365 datas diárias usando list comprehension
# timedelta(days=i) → adiciona i dias à data de início a cada iteração
dates = [start + timedelta(days=i) for i in range(n_days)]

# ─── CATEGORIAS E TIPOS ───────────────────────────────────────────────────────

# Lista de categorias de transações disponíveis
# 'Diversos' é o último item — será excluído nas transações aleatórias
categories = ['Compras de mercado', 'Aluguel', 'Contas', 'Transporte', 'Entretenimento', 'Salário', 'Diversos']

# Tipos possíveis de transação
types = ['Despesa', 'Receita']

# ─── GERAÇÃO DAS TRANSAÇÕES ───────────────────────────────────────────────────

# Lista vazia que receberá cada transação como dicionário
# Ao final será convertida em DataFrame
rows = []

# Percorre cada data do intervalo — 365 iterações, uma por dia
for d in dates:

    # ── SALÁRIO (dia 1 de cada mês) ──────────────────────────────────────────

    # Verifica se é o primeiro dia do mês
    # d.day → extrai o número do dia da data
    if d.day == 1:
        rows.append({
            'Data':      d.date(),                           # data sem hora — ex: 2026-01-01
            'Descrição': 'Salário',                          # descrição fixa
            'Categoria': 'Salário',                          # categoria fixa
            'Tipo':      'Receita',                          # sempre Receita
            'Quantia':   3000 + np.random.randint(-200, 200) # valor entre R$ 2.800 e R$ 3.199
        })
        # Resultado: 12 salários gerados no total — 1 por mês

    # ── TRANSAÇÕES ALEATÓRIAS (despesas do dia) ───────────────────────────────

    # np.random.poisson(0.8) → gera um número aleatório de transações por dia
    # Distribuição de Poisson com média 0.8:
    # ~45% dos dias → 0 transações
    # ~36% dos dias → 1 transação
    # ~14% dos dias → 2 transações
    # ~5%  dos dias → 3 ou mais transações
    # O _ é variável descartável — só importa o número de repetições
    for _ in range(np.random.poisson(0.8)):

        # Sorteia uma categoria aleatória excluindo 'Diversos' (último item)
        # categories[:-1] → remove o último elemento da lista
        cat = np.random.choice(categories[:-1])

        # Gera um valor aleatório entre R$ 5,00 e R$ 200,00
        # round(..., 2) → arredonda para 2 casas decimais
        amt = round(np.random.uniform(5, 200), 2)

        rows.append({
            'Data':      d.date(),           # data do dia atual no loop
            'Descrição': f'Valor de {cat}',  # ex: "Aluguel purchase"
            'Categoria': cat,                # categoria sorteada
            'Tipo':      'Despesa',          # tipo de transação
            'Quantia':   amt                 # valor entre R$ 5,00 e R$ 200,00
        })

    # ── RECEITA EXTRA — FREELANCE (ocasional) ────────────────────────────────

    # np.random.rand() → gera um número decimal aleatório entre 0 e 1
    # < 0.02 → apenas 2% de chance de ocorrer a cada dia
    # Simula uma receita extra esporádica como freelance
    if np.random.rand() < 0.02:
        rows.append({
            'Data':      d.date(),                              # data do dia atual
            'Descrição': 'Freelance',                           # descrição fixa
            'Categoria': 'Diversos',                            # categoria Diversos
            'Tipo':      'Receita',                             # tipo de transação
            'Quantia':   round(np.random.uniform(50, 500), 2)  # valor entre R$ 50,00 e R$ 500,00
        })

# ─── CRIAÇÃO DO DATAFRAME ────────────────────────────────────────────────────

# Converte a lista de dicionários em DataFrame do pandas
df = pd.DataFrame(rows)

# Embaralha todas as linhas do DataFrame aleatoriamente
# frac=1 → embaralha 100% das linhas (todas)
# random_state=1 → semente fixa para reprodutibilidade
# reset_index(drop=True) → redefine o índice após o embaralhamento
# drop=True → descarta o índice antigo em vez de adicioná-lo como coluna
df = df.sample(frac=1, random_state=1).reset_index(drop=True)

# ─── EXPORTAÇÃO ──────────────────────────────────────────────────────────────

# Salva o DataFrame como arquivo CSV na pasta data/
# ⚠️ index=False não foi adicionado — o índice numérico será incluído no CSV
df.to_csv('data/sample_transactions.csv', index=False)

# Confirmação no terminal de que o arquivo foi gerado com sucesso
print('Transações de exemplo criadas: data/sample_transactions.csv')