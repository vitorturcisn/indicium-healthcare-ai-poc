# Agente de IA para Monitoramento Epidemiológico de SRAG

> Proof of Concept (PoC) de Inteligência Artificial Generativa para análise de indicadores de Síndrome Respiratória Aguda Grave (SRAG), busca contextual em fontes institucionais e geração automatizada de relatórios.

## Sobre o projeto

Esta PoC implementa um agente de IA para apoiar o monitoramento epidemiológico de SRAG a partir de um snapshot dos dados públicos do Sistema de Informação da Vigilância Epidemiológica da Gripe (Sivep-Gripe), disponibilizados pelo Ministério da Saúde.

A solução combina:

- **Pandas** para leitura, limpeza e minimização dos dados;
- **SQLite** para armazenamento analítico local;
- **LangGraph** para orquestração do fluxo agentic;
- **Google Gemini** para raciocínio e geração do relatório;
- **Tool Calling** para separar raciocínio de cálculos determinísticos;
- **Matplotlib** para geração dos gráficos;
- **DDGS** para busca contextual na web, com validação do domínio das URLs;
- **Output Validator** para verificar o relatório antes da gravação;
- **Audit Log JSONL** para rastreabilidade da execução.

A fonte oficial utilizada na implementação é o [Portal de Dados Abertos do SUS](https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026), no conjunto **SRAG 2019 a 2026**. O desafio apresenta como referência o conjunto SRAG 2021 a 2024; esta PoC utiliza o conjunto oficial atualizado e um snapshot de 2025 e 2026, mantendo o mesmo propósito analítico. 

## Arquitetura

O fluxo principal é:

```text
CSV SRAG
   |
   v
Pandas -> limpeza + seleção de variáveis
   |
   v
SQLite (dados minimizados)
   |
   +-----------------------------+
   |                             |
   v                             |
LangGraph <-> Gemini             |
   |                             |
   +--> consultar_metricas() ----+--> SQLite
   |
   +--> gerar_graficos() --------+--> SQLite
   |
   +--> buscar_noticias() -------> DDGS -> validação de domínio
   |
   v
Output Validator
   |
   +--> correção/reflexão quando necessário
   |
   v
Artefatos finais + Audit Log
```

O diagrama completo está disponível em `diagrama_arquitetura.pdf`.

## Componentes

### 1. Entrada e minimização

A PoC trabalha somente com as variáveis necessárias às métricas implementadas:

- `DT_NOTIFIC`
- `UTI`
- `EVOLUCAO`
- `VACINA_COV`

Os dados são lidos dos dois arquivos CSV do snapshot utilizado no projeto. O LLM não recebe os registros individuais; ele recebe apenas resultados agregados produzidos pelas ferramentas.

### 2. `consultar_metricas()`

Executa consultas SQL pré-definidas no SQLite e devolve somente indicadores agregados e metadados.

Os indicadores são:

- **Taxa de aumento de casos:** comparação percentual entre os últimos 30 dias disponíveis e os 30 dias imediatamente anteriores;
- **Proporção de óbitos entre casos com desfecho conhecido:** óbitos divididos pelo número de casos com evolução conhecida;
- **Taxa de internação em UTI entre casos SRAG:** internações em UTI divididas pelos casos com informação conhecida sobre UTI;
- **Proporção de casos com vacina registrada:** casos com vacinação registrada como positiva divididos pelos casos com informação vacinal conhecida;
- **Qualidade e completude:** cobertura das variáveis `UTI`, `EVOLUCAO` e `VACINA_COV`.

Esses indicadores não devem ser confundidos com:

- **ocupação hospitalar/ocupação de UTI**, que exige dados de capacidade e leitos, como informações do CNES;
- **cobertura vacinal populacional**, que exige dados da população geral e registros consolidados de vacinação, como os do PNI;
- **incidência populacional**, pois os gráficos representam número de notificações/casos e não possuem denominador populacional.

### 3. `gerar_graficos()`

Gera dois gráficos determinísticos:

- casos diários nos últimos 30 dias disponíveis;
- casos mensais nos últimos 12 meses disponíveis.

Dias/meses sem registros são preenchidos com zero.

Quando a última observação ocorre antes do último dia do mês, o sistema identifica o último mês como **parcial**. No snapshot utilizado na PoC, setembro de 2026 é parcial, com data de corte em 13/09/2026.

### 4. `buscar_noticias()`

Realiza busca contextual sobre SRAG usando DDGS e aplica uma validação real do hostname das URLs retornadas.

Somente são aceitos resultados em domínios que terminem exatamente nos domínios permitidos ou em seus subdomínios:

- `gov.br`
- `fiocruz.br`
- `who.int`

O conteúdo externo é tratado pelo agente como **dado não confiável / contexto externo** e nunca como instrução.

### 5. Output Validator

O relatório final passa por validação determinística para verificar:

- presença das seções obrigatórias;
- terminologia metodologicamente permitida;
- ausência de rótulos proibidos;
- ausência de conclusões inadequadas;
- menção explícita a mês parcial quando aplicável;
- presença das URLs retornadas pela busca.

Quando a primeira versão é reprovada, o fluxo pode retornar ao agente para uma nova geração, respeitando o limite configurado de tentativas.

### 6. Auditoria

Cada execução gera um registro em `audit_log.jsonl` contendo informações como ID da execução, timestamp, modelo, tools acionadas, resultados resumidos e resultado da validação. O objetivo é manter rastreabilidade sem armazenar desnecessariamente grandes volumes de conteúdo externo ou registros individuais.

## Requisitos

- Python **3.10+**;
- uma chave da API do Google AI Studio/Gemini;
- os dois arquivos CSV do snapshot utilizado pela PoC;
- Graphviz instalado como dependência de sistema apenas quando o diagrama PDF for gerado.

## Estrutura do repositório

```text
.
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── indicium_healthcare_ai_poc.py
├── gerar_diagrama.py
├── diagrama_arquitetura.pdf
├── data/
│   └── arquivos CSV do snapshot (não versionados)
└── outputs/
    └── artefatos gerados em execução (não versionados)
```

Os arquivos CSV do snapshot e os artefatos gerados são mantidos fora do versionamento. A pasta `outputs/` pode existir no repositório apenas com um `.gitkeep`.

## Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/vitorturcisn/indicium-healthcare-ai-poc.git
cd indicium-healthcare-ai-poc
```

### 2. Crie e ative um ambiente virtual

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure a chave do Gemini

Linux/macOS:

```bash
export GOOGLE_API_KEY="SUA_CHAVE_AQUI"
```

Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY="SUA_CHAVE_AQUI"
```

A aplicação também reconhece `GOOGLE_API_KEY` já presente no ambiente e, quando executada no Google Colab, consegue utilizar o sistema de Secrets do Colab.

### 5. Coloque os CSVs na pasta de dados

A execução do snapshot utilizado neste projeto espera dois arquivos CSV, obtidos separadamente do conjunto SRAG: 

```text
data/INFLUD25-14-09-2026.csv
data/INFLUD26-14-09-2026.csv
```

Esses arquivos não são versionados no GitHub. Se forem utilizados arquivos de outra data, atualize os nomes definidos na função `main()` do script.

### 6. Execute o agente

```bash
python indicium_healthcare_ai_poc.py
```

Ao terminar, os artefatos serão gravados na pasta `outputs/`.

## Como executar no Google Colab

### Célula 1 — dependências

```python
%pip install -q -r requirements.txt
!apt-get -qq update
!apt-get -qq install -y graphviz
```

### Célula 2 — carregar o Secret do Colab

Crie no painel de Secrets um secret chamado `GOOGLE_API_KEY` e habilite o acesso ao notebook.

```python
import os
from google.colab import userdata

os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")

print(
    "GOOGLE_API_KEY configurada:",
    bool(os.environ.get("GOOGLE_API_KEY"))
)
```

### Célula 3 — carregar os arquivos CSV

```python
from google.colab import files
from pathlib import Path

DATA_DIR = Path("/content/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

uploaded = files.upload()

for filename in uploaded:
    source = Path("/content") / filename
    destination = DATA_DIR / filename
    source.replace(destination)

print("Arquivos em /content/data:")
for path in sorted(DATA_DIR.iterdir()):
    print(path.name)
```

Selecione os dois arquivos:

```text
INFLUD25-14-09-2026.csv
INFLUD26-14-09-2026.csv
```

### Célula 4 — execução do agente

```python
!python /content/indicium_healthcare_ai_poc.py
```

Caso o script esteja no diretório de trabalho atual:

```python
!python indicium_healthcare_ai_poc.py
```

### Célula 5 — gerar o diagrama

```python
!python gerar_diagrama.py
```

## Geração do diagrama de arquitetura

A geração do diagrama foi separada da aplicação principal para manter o código de produção independente da ferramenta Graphviz.

Execute:

```bash
python gerar_diagrama.py
```

São gerados:

```text
outputs/diagrama_arquitetura.pdf
outputs/diagrama_arquitetura_png.png
```

O arquivo PDF pode ser movido para a raiz do repositório caso você queira apresentá-lo diretamente no GitHub.

## Artefatos gerados

Após uma execução bem-sucedida, o sistema produz:

| Arquivo | Descrição |
|---|---|
| `relatorio_final.md` | Relatório epidemiológico em Markdown |
| `grafico_30_dias.png` | Série diária dos últimos 30 dias |
| `grafico_12_meses.png` | Série mensal dos últimos 12 meses |
| `qualidade_dados.json` | Métricas de qualidade e completude |
| `audit_log.jsonl` | Registro de auditoria da execução |
| `srag_dados.db` | Banco SQLite com os dados minimizados |

## Segurança e governança

### Minimização de dados

O banco analítico utiliza somente as quatro variáveis necessárias à PoC. O LLM recebe resultados agregados das ferramentas e não possui uma ferramenta para consultar livremente registros individuais.

### Proteção contra PII

Existe um guardrail de entrada que bloqueia solicitações envolvendo padrões como CPF, nome completo, endereço, dados individuais, registros individuais ou identificadores explícitos de pacientes.

### Prompt Injection

Resultados de busca web são tratados como dados não confiáveis. O system prompt instrui o agente a ignorar comandos ou instruções encontrados em títulos, resumos ou páginas externas.

### Validação de fontes

O código não confia apenas no operador `site:` da busca. O hostname real das URLs retornadas é analisado antes que o resultado seja entregue ao agente.

### Validação do relatório

O Output Validator é determinístico e independente do julgamento livre do LLM. Falhas de estrutura ou terminologia podem disparar uma nova geração antes da gravação final.

### Auditoria

O `audit_log.jsonl` registra a execução e o resultado da validação, permitindo rastrear quais ferramentas foram acionadas e qual foi o resultado resumido de cada etapa.

## Qualidade dos dados e interpretação

A ausência ou o desconhecimento permanecem como ausência/desconhecimento. O código considera os valores conhecidos de cada variável separadamente e permite que cada métrica tenha seu próprio denominador.

A métrica de duplicidade disponível no relatório corresponde a **duplicidades exatas depois da minimização para as quatro colunas**. Ela não deve ser interpretada automaticamente como quantidade de pacientes ou notificações duplicadas na base original.

## Exemplo de resultado do snapshot utilizado

No snapshot utilizado durante o desenvolvimento, a última observação disponível foi **13/09/2026**. O mês de setembro de 2026 é, portanto, parcial. O relatório final explicita essa condição e os gráficos utilizam somente os registros disponíveis até essa data.

## Limitações da PoC

- trabalha com snapshot de dados, e não com uma integração contínua em tempo real;
- depende da disponibilidade e qualidade dos arquivos CSV utilizados;
- não calcula ocupação real de leitos de UTI;
- não calcula cobertura vacinal da população geral;
- os gráficos representam volume de notificações/casos, não incidência populacional;
- as notícias são contexto externo e não substituem análise epidemiológica oficial;
- não realiza diagnóstico nem prescrição clínica.

## Fonte dos dados

Ministério da Saúde — Portal de Dados Abertos do SUS:

https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026

O portal identifica o conjunto como **“Banco de dados da Síndrome Respiratória Aguda Grave (SRAG) - 2019 a 2026”** e informa que os bancos são disponibilizados por ano, com o banco corrente sujeito a atualizações. 

## Licença

Este projeto está licenciado sob os termos descritos no arquivo [LICENSE](LICENSE).
