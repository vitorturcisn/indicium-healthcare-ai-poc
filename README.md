# Agente de IA para Monitoramento Epidemiológico de SRAG 🧬

> PoC de Inteligência Artificial Generativa para análise de indicadores epidemiológicos, contexto de notícias oficiais e geração automatizada de relatórios.

Este repositório contém a implementação de um agente baseado em IA Generativa, projetado para analisar um *snapshot* de dados reais de internações por Síndrome Respiratória Aguda Grave (SRAG) no Brasil (Open DATASUS).

## 🎯 Objetivo
Construir uma solução escalável e auditável que auxilie profissionais de saúde no entendimento da severidade de surtos respiratórios. O sistema combina cálculos estatísticos determinísticos com processamento de linguagem natural e busca contextual segura na web.

## 🏗️ Arquitetura da Solução
A orquestração utiliza o **LangGraph** para criar um *loop agentic* seguro. O motor de raciocínio é o `Gemini 3.6 Flash`, que decide autonomamente o acionamento de ferramentas. Para mitigar alucinações, o modelo **não executa matemática livre**, ele consome funções de backend (`Tools`) que retornam dados já calculados:

1. **`consultar_metricas`:** Executa SQL validado no banco SQLite.
2. **`gerar_graficos`:** Função Matplotlib estática para as séries temporais.
3. **`buscar_noticias`:** Integração DuckDuckGo restrita a domínios oficiais (`gov.br`, `fiocruz.br`, `who.int`).

*(O fluxo completo com loops e componentes está no arquivo `diagrama_arquitetura.pdf` na raiz deste repositório).*

## 📐 Definição das Métricas (Backend)
O agente extrai informações estritas do banco SRAG, não assumindo cenários externos sem os dados adequados:
* **Taxa de Internação em UTI:** Casos internados em UTI / Total de Casos Válidos da base. *(Nota: Não representa "Ocupação Hospitalar", pois a base SRAG não contém o número total de leitos vagos do CNES).*
* **Taxa de Mortalidade:** Óbitos confirmados / Casos com evolução fechada.
* **Proporção de Casos Vacinados:** Casos vacinados contra Covid-19 / Casos Válidos. *(Nota: Não representa a Cobertura Vacinal da População Brasileira, que exigiria integração com o PNI).*
* **Variação de Casos:** Diferença percentual dos últimos 30 dias versus o período anterior de 30 dias.

## 🛡️ Governança e Guardrails
Foram implementados rígidos controles de arquitetura e privacidade:

1. **Proteção de Dados Pessoais Sensíveis (LGPD):** Os dados passam por higienização estrita. O LLM **nunca** recebe registros individuais de pacientes, operando exclusivamente via agregações estatísticas.
2. **Prevenção de Prompt Injection:** Instruções de sistema bloqueiam que textos provenientes de raspagem web alterem a diretriz principal do modelo.
3. **Geração Sem Alucinações:** Regra explícita no agente para responder "Dado não disponível" caso uma ferramenta falhe ou o banco não possua o dado consultado. Sem inferência cega.
4. **Log de Auditoria:** Cada execução gera registros rastreáveis em `audit_log.json` contendo ID de execução, timestamp, prompt e ferramentas acionadas.

## 🚀 Como Executar

**Pré-requisitos:** Python 3.10+ e chave do Google AI Studio.

1. Clone o repositório:
    git clone https://github.com/SEU-USUARIO/indicium-healthcare-ai-poc.git
    cd indicium-healthcare-ai-poc

2. Instale as dependências (preferencialmente em ambiente virtual): 
    pip install langchain langgraph langchain-google-genai duckduckgo-search matplotlib pandas graphviz

3. Exporte sua chave de API:
    export GOOGLE_API_KEY="sua-chave-aqui"

4. Execute o orquestrador:
    python indicium_healthcare_ai_poc.py

## ⚠️ Limitações da PoC
* O sistema opera de forma assíncrona baseada no *snapshot* do CSV disponibilizado, não consumindo streamings em tempo real do Datasus.
* O sistema é uma ferramenta de apoio de business intelligence e **não** realiza diagnósticos, nem emite recomendações clínicas.
