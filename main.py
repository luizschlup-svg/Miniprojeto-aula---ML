"""
Mini-projeto: Festa em Cena
Analize dos pedidos de Halloween de 2024 e 2025.

Para rodar:
    python main.py
"""

import sys

import pandas as pd

# para os acentos aparecerem certos no terminal
sys.stdout.reconfigure(encoding="utf-8")

arquivo = "data/halloween_vendas.csv"


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


def main():
    """Executa o projeto do inicio ao fim."""
    print("=" * 55)
    print("FESTA EM CENA - PEDIDOS DE HALLOWEEN")
    print("=" * 55)

    df = ler_arquivo()
    if df is None:
        return

    mostrar_leitura(df)


if __name__ == "__main__":
    main()
