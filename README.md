# 💰 Finance Tracker — Rastreador de Finanças Pessoais

Aplicação web interativa construída com **Python + Streamlit** para acompanhar transações financeiras, definir orçamentos por categoria e visualizar o fluxo de caixa mensal.

---

## 📸 Visão Geral

| Página | Descrição |
|---|---|
| 📊 Dashboard | KPIs, gráfico de fluxo de caixa mensal e distribuição de gastos por categoria |
| 📋 Transações | Edição direta da tabela, upload e download de CSV |
| 🧾 Planejador de Orçamento | Definição de limites por categoria com alertas visuais |
| ⚙️ Configurações | Geração de dados de exemplo, verificação de arquivos e estado da sessão |

---

## 🚀 Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/finance-tracker.git
cd finance-tracker
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Gere os dados de exemplo

```bash
python data/create_data_sample.py
```

> Cria o arquivo `data/sample_transactions.csv` com 365 dias de transações simuladas.

### 5. Inicie o app

```bash
streamlit run app.py
```

Acesse em: https://rastreadordefinancas.streamlit.app/

---

## 🗂️ Estrutura do Projeto

```
finance_tracker/
│
├── app.py                      # Página inicial e navegação
│
├── pages/
│   ├── 1_Dashboard.py              # KPIs e gráficos
│   ├── 2_Transações.py             # Editor de transações e upload/download CSV
│   ├── 3_Planejador_de_Orçamento.py# Planejamento mensal por categoria
│   └── 4_Ferramentas.py            # Configurações e gerenciamento de dados
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py              # Leitura e escrita do CSV (com cache)
│   ├── finance.py                  # Cálculo de métricas mensais e breakdown
│   └── charts.py                   # Geração de gráficos com Plotly
│
├── data/
│   ├── create_data_sample.py       # Script de geração de dados simulados
│   └── sample_transactions.csv     # Base de dados local (gerada pelo script)
│
└── requirements.txt
```

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão mínima | Uso |
|---|---|---|
| [Streamlit](https://streamlit.io/) | `>= 1.28.0` | Interface web e componentes interativos |
| [Pandas](https://pandas.pydata.org/) | `>= 2.0.0` | Manipulação e agregação de dados |
| [Plotly](https://plotly.com/python/) | `>= 5.0.0` | Gráficos interativos |
| [NumPy](https://numpy.org/) | latest | Geração de dados aleatórios |
| [openpyxl](https://openpyxl.readthedocs.io/) | latest | Suporte a exportação Excel |
| [SQLAlchemy](https://www.sqlalchemy.org/) | latest | Reservado para integração futura com banco de dados |

---

## ✨ Funcionalidades

- **Dashboard** com KPIs em tempo real: receita total, despesa total e saldo líquido
- **Gráfico de barras** comparando receita e despesa mês a mês
- **Gráfico de rosca** com distribuição de gastos por categoria
- **Tabela editável** com adição, remoção e edição de linhas diretamente na UI
- **Upload de CSV** externo para substituir o conjunto de dados
- **Download** do dataset atual em CSV com um clique
- **Planejador de orçamento** mensal com alertas por categoria:
  - 🟢 Dentro do orçamento (< 80%)
  - 🟡 Próximo do limite (80% – 100%)
  - 🔴 Orçamento excedido (> 100%)
- **Persistência via session_state** para manter orçamentos entre interações
- **Geração de dados simulados** diretamente pela interface de configurações
- **Formatação monetária brasileira** (R$ com ponto como separador de milhar)

---

## 📊 Dados Simulados

O script `data/create_data_sample.py` gera automaticamente 365 dias de transações com:

- **Salário mensal** entre R$ 2.800 e R$ 3.199 (todo dia 1)
- **Despesas diárias** aleatórias entre R$ 5,00 e R$ 200,00 (distribuição de Poisson, média 0,8/dia)
- **Receita extra** de freelance entre R$ 50,00 e R$ 500,00 (probabilidade de 2% por dia)
- Categorias: Compras de mercado, Aluguel, Contas, Transporte, Entretenimento, Salário, Diversos

---

## 📋 Requisitos

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.0.0
numpy
openpyxl
sqlalchemy
```

---

## 📌 Observações

- Os dados são persistidos localmente em `data/sample_transactions.csv`
- Os orçamentos definidos no planejador são mantidos apenas na sessão atual; ao reiniciar o app são redefinidos para R$ 500,00 por categoria
- O campo `data/finance.db` está reservado para uma futura integração com SQLite

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido por **Danilo Oliveira dos Santos** — Outubro de 2026.