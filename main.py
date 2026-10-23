"""
Mini-projeto: Festa em Cena
Analize dos pedidos de Halloween de 2024 e 2025.

Para rodar:
    python main.py
"""

import re
import sys
from datetime import datetime

import pandas as pd

# para os acentos aparecerem certos no terminal
sys.stdout.reconfigure(encoding="utf-8")

arquivo = "data/halloween_vendas.csv"


def limpar_categoria(valor):
    """Limpa uma categoria e devolve o texto padronizado."""
    if pd.isna(valor):
        return "sem categoria"

    texto = str(valor).strip().lower()
    texto = re.sub(r"[^a-z\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    if texto == "":
        return "sem categoria"

    return texto.capitalize()


def limpar_canal(valor):
    """Troca o nome do canal pelo nome oficial."""
    texto = str(valor).strip().lower()
    canais = {
        "mercado": "Mercado",
        "loja física": "Loja física",
        "web": "Web",
    }
    return canais.get(texto, "não identificado")


def converter_data(valor):
    """Converte a data de venda; se nao conseguir, devolve None."""
    try:
        return datetime.strptime(str(valor).strip(), "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None


def ler_arquivo():
    """Le o CSV e devolve o DataFrame."""
    try:
        return pd.read_csv(arquivo, sep=",", encoding="utf-8")
    except FileNotFoundError:
        print("Arquivo nao encontrado:", arquivo)
        return None


def mostrar_leitura(df):
    """Mostra o tamanho da base e as primeiras linhas."""
    print("\nLinhas:", len(df))
    print("Colunas:", len(df.columns))
    print("\nPrimeiras linhas:")
    print(df.head(3))


def limpar_categorias(df):
    """Padroniza as categorias e conta as vazias e as alteradas."""
    df["categoria_limpa"] = df["categoria"].apply(limpar_categoria)

    vazias = df["categoria"].isna() | (df["categoria"].astype(str).str.strip() == "")
    alteradas = (~vazias) & (df["categoria_limpa"] != df["categoria"])

    print("\n--- CATEGORIAS ---")
    print("Categorias vazias preenchidas:", vazias.sum())
    print("Categorias nao vazias alterdas:", alteradas.sum())
    print(df["categoria_limpa"].value_counts())
    return df


def limpar_canais(df):
    """Padroniza o canal de venda."""
    df["canal_limpo"] = df["canal_venda"].apply(limpar_canal)

    print("\n--- CANAIS ---")
    print(df["canal_limpo"].value_counts())
    print("Nao identificados:", (df["canal_limpo"] == "não identificado").sum())
    return df


def validar_numeros(df):
    """Marca quantidade e preco invalidos, sem corrigir os valores."""
    df["quantidade_num"] = pd.to_numeric(df["quantidade"], errors="coerce")
    df["preco_num"] = pd.to_numeric(df["preco_unitario"], errors="coerce")

    qtd_ok = (df["quantidade_num"] > 0) & (df["quantidade_num"] % 1 == 0)
    preco_ok = df["preco_num"] >= 0

    df["problema_qtd"] = ~qtd_ok
    df["problema_preco"] = ~preco_ok
    df["problema_num"] = df["problema_qtd"] | df["problema_preco"]

    print("\n--- QUANTIDADE E PRECO ---")
    print("Pedidos com quantidade invalida:", df["problema_qtd"].sum())
    print("Pedidos com preso invalido:", df["problema_preco"].sum())
    print("Pedidos com os dois problemas:",
          (df["problema_qtd"] & df["problema_preco"]).sum())
    print("Total com problema numerico:", df["problema_num"].sum())
    return df


def processar_datas(df):
    """Converte as datas e cria as colunas de ano, mes, dia, hora e ano-mes."""
    df["data_convertida"] = df["data_venda"].apply(converter_data)
    df["data_ok"] = df["data_convertida"].notna()

    df["data_br"] = df["data_convertida"].dt.strftime("%d/%m/%Y").fillna("")
    df["ano"] = df["data_convertida"].dt.strftime("%Y").fillna("")
    df["mes"] = df["data_convertida"].dt.strftime("%m").fillna("")
    df["dia"] = df["data_convertida"].dt.strftime("%d").fillna("")
    df["hora"] = df["data_convertida"].dt.strftime("%H").fillna("")
    df["ano_mes"] = df["data_convertida"].dt.strftime("%Y-%m").fillna("")

    print("\n--- DATAS ---")
    print("Datas validas:", df["data_ok"].sum())
    print("Datas invalidas:", (~df["data_ok"]).sum())
    print(df.loc[df["data_ok"],
                 ["data_venda", "data_br", "ano", "mes", "dia", "hora"]].head(3))
    return df


def analisar_entrega(df):
    """Testa se todo pedido sem data de entrega esta cancelado."""
    df["sem_entrega"] = df["data_entrega"].isna()
    df["cancelado"] = df["status_pedido"].str.strip() == "Cancelado"

    sem_entrega = df["sem_entrega"]
    cancelado = df["cancelado"]

    print("\n--- ENTREGA SEM DATA ---")
    print("Pedidos sem data de entrega:", sem_entrega.sum())
    print("Cancelados:", (sem_entrega & cancelado).sum())
    print("Outros status:", (sem_entrega & ~cancelado).sum())

    if (sem_entrega & ~cancelado).sum() == 0:
        print("A hipotese e verdadeira.")
    else:
        print("A hipotese e falsa: tem pedido sem entrega que nao esta cancelado.")
        print(df.loc[sem_entrega & ~cancelado,
                     ["pedido_id", "data_venda", "status_pedido"]].head(3))
    return df


def main():
    """Executa o projeto do inicio ao fim."""
    print("=" * 55)
    print("FESTA EM CENA - PEDIDOS DE HALLOWEEN")
    print("=" * 55)

    df = ler_arquivo()
    if df is None:
        return

    mostrar_leitura(df)
    df = limpar_categorias(df)
    df = limpar_canais(df)
    df = validar_numeros(df)
    df = processar_datas(df)
    df = analisar_entrega(df)


if __name__ == "__main__":
    main()
