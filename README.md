# Agente de IA para Monitoramento Epidemiológico (SRAG) 🧬

**Prova de Conceito (PoC) desenvolvida para a Indicium HealthCare Inc.**

Este repositório contém a implementação de um sistema multi-agente baseado em Inteligência Artificial Generativa, projetado para analisar dados reais de internações por Síndrome Respiratória Aguda Grave (SRAG) no Brasil (Open DATASUS) e gerar relatórios automatizados.

## 🎯 Objetivo
Construir uma solução escalável que auxilie profissionais de saúde no entendimento, em tempo real, da severidade e avanço de surtos respiratórios. O sistema combina análise estruturada de dados (SQL) com processamento de linguagem natural e busca contextual na web.

## 🏗️ Arquitetura da Solução (LangGraph)
A orquestração do agente foi desenvolvida utilizando a biblioteca **LangGraph**, garantindo um fluxo cíclico, controlável e auditável. O "cérebro" do orquestrador é alimentado pelo LLM `Gemini 3.6 Flash`, que decide de forma autônoma quando acionar as seguintes ferramentas (`Tools`):

1. **SQL Tool (`consultar_metricas`):** Converte a intenção do agente em consultas precisas em um banco SQLite local, garantindo que o LLM não "alucine" cálculos matemáticos.
2. **Chart Tool (`gerar_graficos`):** Função estática em Matplotlib acionada para gerar a série temporal dos últimos 30 dias e 12 meses.
3. **Search Tool (`buscar_noticias`):** Integração com DuckDuckGo (DDGS) para capturar o contexto atual das redes hospitalares e embasar a análise qualitativa do relatório.

*(O Diagrama Arquitetural do fluxo lógico pode ser visualizado no arquivo `diagrama_arquitetura.png` na raiz deste repositório).*

## 🛡️ Governança e Tratamento de Dados Sensíveis
Como a base do DATASUS contém dados médicos reais de mais de 165 mil pacientes por ano, implementou-se uma rotina de Engenharia de Dados estrita (Clean Data):

* **Anonimização Estrita:** Remoção de dados diretos de identificação e limitação às 10 colunas essenciais para a PoC.
* **Limpeza de Ruído Clínico:** Pacientes com código `9` (Ignorado) nas colunas vitais (`UTI`, `EVOLUCAO`, `VACINA_COV`) ou casos de óbitos por outras causas foram removidos da base. O banco final resultou em uma redução de mais de 100 mil registros inválidos, entregando uma base clinicamente pura para o Agente.
* **Isolamento de Credenciais:** As chaves de API (Google AI) são lidas exclusivamente via variáveis de ambiente, prevenindo vazamentos de segurança.

## 🚀 Como Executar

**Pré-requisitos:** Python 3.10+ e uma chave de API do Google AI Studio.

1. Clone o repositório:
```bash
git clone [https://github.com/SEU-USUARIO/indicium-healthcare-ai-poc.git](https://github.com/SEU-USUARIO/indicium-healthcare-ai-poc.git)
cd indicium-healthcare-ai-poc
```

2. Instale as dependências: 
```bash
pip install langchain langgraph langchain-google-genai duckduckgo-search matplotlib pandas duckdb
```

3. Defina sua chave de API no terminal:
```bash
export GOOGLE_API_KEY="sua-chave-aqui"
```

4. Execute o orquestrador:
```bash
python indicium_healthcare_ai_poc.py
```

## 📊 Entregáveis Gerados
Ao executar a solução, o Agente salva localmente os gráficos de série temporal e redige o relatório executivo (disponível para consulta em `relatorio_final.md`) contendo as seguintes métricas analisadas:
* Taxa de Ocupação de UTI
* Taxa de Mortalidade
* Cobertura Vacinal
* Aumento/Queda de Casos (vs período anterior)
* Análise de Contexto Integrada
