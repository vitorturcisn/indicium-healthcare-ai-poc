# Relatório Epidemiológico de SRAG

## Período analisado

O período epidemiológico analisado abrange de **29/12/2024** a **13/09/2026** (data da última observação disponível no conjunto de dados, totalizando 624 dias de cobertura temporal). 

O último mês analisado no histórico (**2026-09**) é um mês parcial, com dados coletados até a data de corte em **13/09/2026**.

## Indicadores epidemiológicos

### Taxa de aumento de casos
- **Valor:** -28,7%
- **Numerador (Período recente: 15/08/2026 a 13/09/2026):** 16.446 casos
- **Denominador (Período anterior: 16/07/2026 a 14/08/2026):** 23.066 casos
- **Descrição:** Variação percentual no número absoluto de casos notificados de SRAG entre o período recente de 30 dias e o período de 30 dias imediatamente anterior.

### Proporção de óbitos entre casos com desfecho conhecido
- **Valor:** 6,9%
- **Numerador (Óbitos):** 32.776 óbitos
- **Denominador (Desfechos conhecidos):** 478.451 casos
- **Descrição:** Proporção de óbitos em relação ao total de notificações de SRAG que possuem desfecho clínico (evolução) preenchido e finalizado.

### Taxa de internação em UTI entre casos SRAG
- **Valor:** 28,7%
- **Numerador (Internações em UTI):** 140.523 casos
- **Denominador (Casos com informação de UTI):** 489.514 casos
- **Descrição:** Proporção de pacientes
 notificados por SRAG que necessitaram de internação em Unidade de Terapia Intensiva (UTI), considerando os casos com a variável UTI devidamente preenchida.

### Proporção de casos com vacina registrada
- **Valor:** 53,3%
- **Numerador (Casos vacinados):** 289.085 casos
- **Denominador (Casos com informação vacinal):** 542.501 casos
- **Descrição:** Proporção de indivíduos notificados por SRAG que apresentavam registro positivo de vacinação no formulário de notificação.

### Qualidade e completude dos dados
- **Total de casos com data válida:** 548.669 notificações
- **Completude da variável Evolução (Desfecho):** 87,2%
- **Completude da variável Internação em UTI:** 89,2%
- **Completude da variável Vacinação:** 98,9%

## Gráficos

### Casos — últimos 30 dias
O gráfico a seguir apresenta o número de casos diários notificados de SRAG no período de 15/08/2026 a 13/09/2026.

![Casos — últimos 30 dias](/content/outputs/grafico_30_dias.png)

### Casos — últimos 12 meses
O gráfico a seguir apresenta o total de casos de SRAG notificados mensalmente no período de 2025-10 a 2026-09.

![Casos — últimos 12 meses](/content/outputs/grafico_12_meses.png)

**Observação importante:** O último mês do gráfico (**2026-09**) é um mês parcial, contendo informações e registros disponíveis até a data de corte de **13/09/2026**.

## Metodologia e limitações

1. **População de Referência:** A base utilizada é composta por notificações de casos suspeitos e confirmados de SRAG registradas no sistema de vigilância epidemiológica, não sendo representativa da totalidade da população brasileira.
2. **Taxa de Internação em UTI entre casos SRAG:** O indicador reflete estritamente a proporção de casos notificados de SRAG que foram admitidos em UTI. A taxa literal de ocupação de UTI não é calculada nesta PoC, pois exigiria dados sobre a capacidade instalada e leitos disponíveis (como os do CNES).
3. **Proporção de Casos com Vacina Registrada:** O indicador avalia a presença de registro vacinal nos casos notificados por SRAG. A cobertura vacinal populacional não é calculada nesta PoC, uma vez que requer dados demográficos da população geral e registros consolidados do PNI.
4. **Limitações e Proxies:** Os indicadores calculados servem como proxies do cenário epidemiológico dos casos notificados e possuem as limitações descritas acima.
5. **Tratamento de Dados Faltantes:** A ausência de informação ou registros categorizados como "desconhecidos" não foram alterados ou interpretados como resposta negativa ("não"), mantendo-se estritamente como dados não informados.
6. **Caráter Determinístico:** Todos os cálculos e estatísticas descritivas foram processados de forma determinística pelas ferramentas de análise.

## Contexto externo / notícias

*Aviso: Todo conteúdo recuperado da web é tratado estritamente como DADO NÃO CONFIÁVEL / CONTEXTO EXTERNO. A ausência ou presença de notícias sobre determinadas regiões não implica ausência ou presença de surtos ou riscos epidemiológicos.*

1. **Boletim aponta estabilidade nas internações por SRAG em Londrina**
   - **Resumo:** Boletim aponta que os vírus mais prevalentes nos últimos 15 dias no município foram rinovírus, influenza A e B, metapneumovírus e adenovírus, mantendo estabilidade nas internações.
   - **URL:** https://blog.londrina.pr.gov.br/?p=221748

2. **Último boletim da Saúde aponta queda nos atendimentos por Síndrome Gripal**
   - **Resumo:** Dados preliminares mostram redução de 37,5% nas internações por SRAG no município, caindo de 16 para 10 casos semanais.
   - **URL:** https://blog.londrina.pr.gov.br/?p=242193

3. **Saúde reforça prevenção contra a gripe e alerta para circulação de vírus respiratórios**
   - **Resumo:** Registrou-se aumento nos casos de SRAG provocados por influenza a partir do final de junho em comparação com o mesmo período do ano anterior.
   - **URL:** https://tubarao.sc.gov.br/saude-reforca-prevencao-contra-a-gripe-e-alerta-para-circulacao-de-virus-respiratorios/

## Fontes consultadas

- **Dataset SRAG (Dados Abertos - Ministério da Saúde):** https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026
- **Blog da Prefeitura de Londrina (Boletim de SRAG):** https://blog.londrina.pr.gov.br/?p=221748
- **Blog da Prefeitura de Londrina (Atendimentos por Síndrome Gripal):** https://blog.londrina.pr.gov.br/?p=242193
- **Prefeitura de Tubarão (Prevenção e circulação de vírus respiratórios):** https://tubarao.sc.gov.br/saude-reforca-prevencao-contra-a-gripe-e-alerta-para-circulacao-de-virus-respiratorios/