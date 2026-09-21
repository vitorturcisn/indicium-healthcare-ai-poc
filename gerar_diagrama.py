# -*- coding: utf-8 -*-
"""Gera o diagrama de arquitetura da PoC SRAG.

Funciona no Windows e no Google Colab.
Os arquivos são salvos na pasta ``outputs/`` do repositório e o PDF também
é copiado para a raiz do projeto.
"""

from pathlib import Path
import shutil

import graphviz


def get_project_dir() -> Path:
    """Retorna a pasta do projeto com base na localização do script."""
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()


def build_diagram() -> graphviz.Digraph:
    """Constrói o diagrama alinhado à arquitetura da versão 1.2.2."""
    dot = graphviz.Digraph(
        comment="Arquitetura da PoC SRAG",
        format="pdf",
        engine="dot",
    )

    dot.attr(
        rankdir="TB",
        bgcolor="white",
        pad="0.3",
        nodesep="0.55",
        ranksep="0.75",
        fontname="Helvetica",
        splines="ortho",
    )

    dot.attr(
        "node",
        fontname="Helvetica",
        fontsize="10",
        margin="0.15,0.10",
    )

    dot.attr(
        "edge",
        fontname="Helvetica",
        fontsize="8",
    )

    # Dados e preparação
    with dot.subgraph(name="cluster_data") as data:
        data.attr(
            label="Dados e preparação",
            color="#B7B7B7",
            style="rounded",
            fontname="Helvetica-Bold",
        )

        data.node(
            "CSV",
            "Arquivos CSV SRAG\nINFLUD25 + INFLUD26",
            shape="note",
            style="filled",
            fillcolor="#D9EAF7",
        )

        data.node(
            "PROC",
            "Pandas\nLeitura, limpeza e minimização",
            shape="box",
            style="filled",
            fillcolor="#D9EAD3",
        )

        data.node(
            "DB",
            "SQLite\nsrag_dados.db\nDados minimizados",
            shape="cylinder",
            style="filled",
            fillcolor="#EAD1DC",
        )

        data.edge("CSV", "PROC")
        data.edge("PROC", "DB")

    # Entrada e guardrail
    dot.node(
        "USER",
        "Solicitação do usuário",
        shape="ellipse",
        style="filled",
        fillcolor="#D9EAD3",
    )

    dot.node(
        "INPUT",
        "Input Guardrail\nProteção contra PII\nValidação da solicitação",
        shape="note",
        style="filled",
        fillcolor="#FCE5CD",
    )

    dot.edge("USER", "INPUT")
    dot.edge("INPUT", "TOOLS")

    # Orquestração determinística
    dot.node(
        "TOOLS",
        "LangGraph\nOrquestração da execução",
        shape="box",
        style="filled",
        fillcolor="#FFF2CC",
        fontname="Helvetica-Bold",
    )

    dot.node(
        "T1",
        "consultar_metricas()\nCálculos determinísticos\nSQL agregado/restrito",
        shape="box",
        style="filled",
        fillcolor="#FCE5CD",
    )

    dot.node(
        "T2",
        "gerar_graficos()\nMatplotlib\n30 dias + 12 meses",
        shape="box",
        style="filled",
        fillcolor="#FCE5CD",
    )

    dot.node(
        "T3",
        "buscar_noticias()\nBusca web + allowlist\nFontes institucionais",
        shape="box",
        style="filled",
        fillcolor="#FCE5CD",
    )

    dot.edge("TOOLS", "T1")
    dot.edge("TOOLS", "T2")
    dot.edge("TOOLS", "T3")

    dot.edge("T1", "DB", label="consulta")
    dot.edge("DB", "T1", label="agregados")
    dot.edge("T2", "DB", label="consulta")
    dot.edge("DB", "T2", label="séries")

    # Busca web
    dot.node(
        "WEB",
        "DuckDuckGo\nBusca contextual",
        shape="ellipse",
        style="filled",
        fillcolor="#EAD1DC",
    )

    dot.node(
        "SOURCES",
        "Allowlist de domínios\n"
        "gov.br\n"
        "fiocruz.br\n"
        "who.int",
        shape="box",
        style="filled",
        fillcolor="#D9EAF7",
    )

    dot.edge("T3", "WEB")
    dot.edge("WEB", "SOURCES", label="resultados")
    dot.edge("SOURCES", "T3", label="URLs validadas")

    dot.edge("T1", "TOOLS", label="métricas")
    dot.edge("T2", "TOOLS", label="gráficos")
    dot.edge("T3", "TOOLS", label="contexto")

    # LLM
    dot.node(
        "LLM",
        "Google Gemini 3.7 Flash\n"
        "Análise e geração textual\n"
        "System Prompt + resultados das tools",
        shape="box",
        style="filled",
        fillcolor="#C9DAF8",
        fontname="Helvetica-Bold",
    )

    dot.edge("TOOLS", "LLM", label="resultados determinísticos")

    # Normalização + validação
    dot.node(
        "NORM",
        "Normalização determinística\n"
        "Ex.: observação de mês parcial",
        shape="box",
        style="filled",
        fillcolor="#FFF2CC",
    )

    dot.node(
        "VAL",
        "Output Validator\n"
        "Checa estrutura, terminologia\n"
        "e coerência metodológica",
        shape="octagon",
        style="filled",
        fillcolor="#F4CCCC",
        fontname="Helvetica-Bold",
    )

    dot.edge("LLM", "NORM")
    dot.edge("NORM", "VAL")

    # Integrações futuras
    dot.node(
        "CNES",
        "Integração futura: CNES\n"
        "Capacidade / leitos de UTI",
        shape="box",
        style="dashed,filled",
        fillcolor="#F3F3F3",
    )

    dot.node(
        "PNI",
        "Integração futura: PNI\n"
        "Cobertura vacinal populacional",
        shape="box",
        style="dashed,filled",
        fillcolor="#F3F3F3",
    )

    dot.edge("CNES", "T1", style="dashed", label="futuro")
    dot.edge("PNI", "T1", style="dashed", label="futuro")

    # Saídas
    dot.node(
        "OUT",
        "Artefatos aprovados",
        shape="box",
        style="filled",
        fillcolor="#D9EAD3",
        fontname="Helvetica-Bold",
    )

    dot.node(
        "REPORT",
        "relatorio_final.md\nRelatório epidemiológico",
        shape="note",
        style="filled",
        fillcolor="#D9EAD3",
    )

    dot.node(
        "G30",
        "grafico_30_dias.png\nCasos diários",
        shape="note",
        style="filled",
        fillcolor="#D9EAD3",
    )

    dot.node(
        "G12",
        "grafico_12_meses.png\nCasos mensais",
        shape="note",
        style="filled",
        fillcolor="#D9EAD3",
    )

    dot.node(
        "QUALITY",
        "qualidade_dados.json\nQualidade/completude",
        shape="note",
        style="filled",
        fillcolor="#D9D2E9",
    )

    dot.node(
        "AUDIT",
        "audit_log.jsonl\nAuditoria da execução",
        shape="note",
        style="filled",
        fillcolor="#D9D2E9",
    )

    dot.edge("VAL", "OUT", label="aprovado")
    dot.edge("OUT", "REPORT")
    dot.edge("OUT", "G30")
    dot.edge("OUT", "G12")
    dot.edge("OUT", "QUALITY")
    dot.edge("OUT", "AUDIT")

    # Governança
    dot.node(
        "SAFE",
        "Governança e guardrails\n"
        "• Minimização de dados\n"
        "• Proteção contra PII\n"
        "• Prompt Injection protection\n"
        "• Allowlist de fontes\n"
        "• Validação determinística\n"
        "• Auditoria sem registros individuais",
        shape="box",
        style="filled",
        fillcolor="#E6E6E6",
        fontname="Helvetica-Bold",
    )

    dot.edge("SAFE", "INPUT", style="dashed")
    dot.edge("SAFE", "T3", style="dashed")
    dot.edge("SAFE", "VAL", style="dashed")
    dot.edge("SAFE", "AUDIT", style="dashed")

    return dot


def main() -> None:
    project_dir = get_project_dir()
    output_dir = project_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    dot = build_diagram()

    pdf_output = dot.render(
        filename=str(output_dir / "diagrama_arquitetura"),
        format="pdf",
        cleanup=True,
    )

    png_output = dot.render(
        filename=str(output_dir / "diagrama_arquitetura_png"),
        format="png",
        cleanup=True,
    )

    # Cópia do PDF na raiz para facilitar a publicação no GitHub.
    root_pdf = project_dir / "diagrama_arquitetura.pdf"
    shutil.copy2(pdf_output, root_pdf)

    print("=" * 70)
    print("DIAGRAMA GERADO COM SUCESSO")
    print("=" * 70)
    print(f"Projeto:   {project_dir}")
    print(f"PDF:       {pdf_output}")
    print(f"PNG:       {png_output}")
    print(f"PDF raiz:  {root_pdf}")
    print("=" * 70)


if __name__ == "__main__":
    main()
