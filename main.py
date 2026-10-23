"""
Mini-projeto: Festa em Cena
Analize dos pedidos de Halloween de 2024 e 2025.

Para rodar:
    python main.py
"""

import re
import sys

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


if __name__ == "__main__":
    main()
