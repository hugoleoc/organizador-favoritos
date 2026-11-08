# Biblioteca para manipular tabelas e gravar CSV
import pandas as pd

# Reutilizamos as funções já testadas do organizador
from src.organizador import ler_favoritos, remover_duplicatas

# Caminhos de entrada e saída, relativos à raiz do projeto
CAMINHO_ENTRADA = "dados/favoritos.html"
CAMINHO_SAIDA = "dados/amostra_rotulagem.csv"

# Tamanho da amostra e semente aleatória (garante o mesmo sorteio em outras execuções)
TAMANHO_AMOSTRA = 150
SEMENTE = 42


def gerar_amostra():
    """Sorteia favoritos únicos e grava um CSV para rotulagem manual."""

    # Lê os favoritos e remove duplicatas, para não rotular o mesmo link duas vezes
    itens = remover_duplicatas(ler_favoritos(CAMINHO_ENTRADA))

    # Converte a lista de dicionários em uma tabela (DataFrame)
    tabela = pd.DataFrame(itens)

    # Sorteia linhas sem reposição; frac=1 embaralha tudo e head pega as primeiras
    amostra = tabela.sample(n=min(TAMANHO_AMOSTRA, len(tabela)), random_state=SEMENTE)

    # Cria a coluna de rótulo vazia, para você preencher
    amostra["categoria"] = ""

    # Grava o CSV com codificação UTF-8 com BOM, para o Excel abrir os acentos corretamente
    amostra.to_csv(CAMINHO_SAIDA, index=False, encoding="utf-8-sig")

    print(f"Amostra gravada em {CAMINHO_SAIDA} com {len(amostra)} itens.")


if __name__ == "__main__":
    gerar_amostra()