import graphviz
from pathlib import Path

OUTPUT_DIR = Path("/content/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

dot = graphviz.Digraph(
    comment="Arquitetura do Agente SRAG",
    format="pdf"
)

dot.attr(
    rankdir="TB",
    size="11,14",
    fontname="Helvetica",
    nodesep="0.6",
    ranksep="0.8",
    bgcolor="white"
)

dot.attr(
    "node",
    fontname="Helvetica",
    fontsize="11",
    margin="0.15,0.10"
)

dot.attr(
    "edge",
    fontname="Helvetica",
    fontsize="9"
)

# ============================================================
# ENTRADA E PROCESSAMENTO
# ============================================================

dot.node(
    "CSV",
    "Arquivos CSV SRAG\nINFLUD25 + INFLUD26",
    shape="folder",
    style="filled",
    fillcolor="#D9EAF7"
)

dot.node(
    "PROC",
    "Pandas\nLeitura, limpeza e minimização",
    shape="box",
    style="filled",
    fillcolor="#D9EAD3"
)

dot.node(
    "DB",
    "SQLite\nsrag_dados.db\n(Dados minimizados)",
    shape="cylinder",
    style="filled",
    fillcolor="#EAD1DC"
)

dot.edge("CSV", "PROC")
dot.edge("PROC", "DB")

# ============================================================
# AGENTE
# ============================================================

dot.node(
    "USER",
    "Solicitação\npara o agente",
    shape="ellipse",
    style="filled",
    fillcolor="#D9EAD3"
)

dot.node(
    "INPUT",
    "Input Guardrail\n(Bloqueio de PII)",
    shape="note",
    style="filled",
    fillcolor="#FCE5CD"
)

dot.node(
    "LG",
    "LangGraph\nOrquestrador Agentic",
    shape="box",
    style="filled",
    fillcolor="#FFF2CC",
    fontname="Helvetica-Bold"
)

dot.node(
    "LLM",
    "Google Gemini\nGemini 3.6 Flash\n(System Prompt + Contexto)",
    shape="box",
    style="filled",
    fillcolor="#C9DAF8"
)

dot.edge("USER", "INPUT")
dot.edge("INPUT", "LG")
dot.edge("LG", "LLM", label=" Pensa / Decide")
dot.edge("LLM", "LG")

# ============================================================
# TOOLS
# ============================================================

dot.node(
    "T1",
    "Tool: consultar_metricas()\n"
    "Cálculos determinísticos\n"
    "SQL restrito",
    shape="component",
    style="filled",
    fillcolor="#FCE5CD"
)

dot.node(
    "T2",
    "Tool: gerar_graficos()\n"
    "Matplotlib\n"
    "30 dias / 12 meses",
    shape="component",
    style="filled",
    fillcolor="#FCE5CD"
)

dot.node(
    "T3",
    "Tool: buscar_noticias()\n"
    "Busca web + validação\n"
    "de domínio institucional",
    shape="component",
    style="filled",
    fillcolor="#FCE5CD"
)

dot.edge("LG", "T1")
dot.edge("LG", "T2")
dot.edge("LG", "T3")

dot.edge(
    "T1",
    "DB",
    label=" Consulta agregada"
)

dot.edge(
    "T1",
    "LG",
    label=" Retorna métricas"
)

dot.edge(
    "T2",
    "LG",
    label=" Retorna gráficos"
)

dot.edge(
    "T3",
    "LG",
    label=" Retorna contexto"
)

# ============================================================
# WEB
# ============================================================

dot.node(
    "WEB",
    "DuckDuckGo\nBusca contextual",
    shape="cloud",
    style="filled",
    fillcolor="#EAD1DC"
)

dot.node(
    "SOURCES",
    "Fontes permitidas\n"
    "gov.br\n"
    "fiocruz.br\n"
    "who.int",
    shape="box",
    style="filled",
    fillcolor="#D9EAF7"
)

dot.edge("T3", "WEB")
dot.edge("WEB", "SOURCES", label=" Filtra / valida")
dot.edge("SOURCES", "T3")

# ============================================================
# INTEGRAÇÕES FUTURAS
# ============================================================

dot.node(
    "CNES",
    "Integração futura: CNES\n"
    "Capacidade / leitos de UTI",
    shape="box",
    style="dashed,filled",
    fillcolor="#F3F3F3"
)

dot.node(
    "PNI",
    "Integração futura: PNI\n"
    "Cobertura vacinal populacional",
    shape="box",
    style="dashed,filled",
    fillcolor="#F3F3F3"
)

dot.edge("CNES", "T1", style="dashed")
dot.edge("PNI", "T1", style="dashed")

# ============================================================
# VALIDAÇÃO
# ============================================================

dot.node(
    "VAL",
    "Output Validator\n"
    "Validação determinística\n"
    "metodológica",
    shape="octagon",
    style="filled",
    fillcolor="#F4CCCC",
    fontname="Helvetica-Bold"
)

dot.edge(
    "LG",
    "VAL",
    label=" Valida relatório"
)

dot.edge(
    "VAL",
    "LLM",
    style="dashed",
    label=" Corrigir / Refazer"
)

# ============================================================
# SAÍDAS
# ============================================================

dot.node(
    "OUT",
    "Artefatos Gerados",
    shape="box",
    style="filled",
    fillcolor="#D9EAD3",
    fontname="Helvetica-Bold"
)

dot.node(
    "REPORT",
    "relatorio_final.md\n"
    "Relatório epidemiológico",
    shape="note",
    style="filled",
    fillcolor="#D9EAD3"
)

dot.node(
    "G30",
    "grafico_30_dias.png\n"
    "Casos diários",
    shape="note",
    style="filled",
    fillcolor="#D9EAD3"
)

dot.node(
    "G12",
    "grafico_12_meses.png\n"
    "Casos mensais",
    shape="note",
    style="filled",
    fillcolor="#D9EAD3"
)

dot.node(
    "QUALITY",
    "qualidade_dados.json\n"
    "Qualidade dos dados",
    shape="note",
    style="filled",
    fillcolor="#D9D2E9"
)

dot.node(
    "AUDIT",
    "audit_log.jsonl\n"
    "Auditoria da execução",
    shape="note",
    style="filled",
    fillcolor="#D9D2E9"
)

dot.edge("VAL", "OUT", label=" Aprovado")

dot.edge("OUT", "REPORT")
dot.edge("OUT", "G30")
dot.edge("OUT", "G12")
dot.edge("OUT", "QUALITY")
dot.edge("OUT", "AUDIT")

# ============================================================
# GUARDRAILS
# ============================================================

dot.node(
    "SAFE",
    "Guardrails e Boas Práticas\n"
    "• Proteção contra PII\n"
    "• Dados minimizados\n"
    "• API Key via Secret / ambiente\n"
    "• Validação de domínio\n"
    "• Output Validator\n"
    "• Auditoria\n"
    "• Prompt Injection protection",
    shape="box",
    style="filled",
    fillcolor="#E6E6E6",
    fontname="Helvetica-Bold"
)

dot.edge("SAFE", "INPUT", style="dashed")
dot.edge("SAFE", "T3", style="dashed")
dot.edge("SAFE", "VAL", style="dashed")
dot.edge("SAFE", "AUDIT", style="dashed")

# ============================================================
# RENDER
# ============================================================

pdf_path = dot.render(
    str(OUTPUT_DIR / "diagrama_arquitetura"),
    cleanup=True
)

png_path = dot.render(
    str(OUTPUT_DIR / "diagrama_arquitetura_png"),
    format="png",
    cleanup=True
)

print("=" * 70)
print("DIAGRAMA GERADO COM SUCESSO")
print("=" * 70)
print(f"PDF: {pdf_path}")
print(f"PNG: {png_path}")
print("=" * 70)
