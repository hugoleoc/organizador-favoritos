# Biblioteca para manipular tabelas
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

# Funções já testadas do projeto
from src.organizador import ler_favoritos, remover_duplicatas
from src.treino import preparar_texto

# Caminhos, relativos à raiz do projeto
CAMINHO_FAVORITOS = "dados/favoritos.html"
CAMINHO_ROTULADA = "dados/amostra_rotulagem.csv"
CAMINHO_REVISAO = "dados/revisao.csv"

# Tamanho do lote por rodada
TAMANHO_LOTE = 50


def selecionar_revisao():
    """Prevê categorias dos favoritos não rotulados e grava o lote de menor confiança."""

    # Carrega a amostra já rotulada, descartando linhas sem categoria e "Sem categoria"
    rotulada = pd.read_csv(CAMINHO_ROTULADA, dtype=str).dropna(subset=["categoria"])
    rotulada = rotulada[rotulada["categoria"] != "Sem categoria"]

    # Treina o modelo com todos os itens rotulados (sem validação, pois o objetivo é prever)
    modelo = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2)),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )
    modelo.fit(preparar_texto(rotulada), rotulada["categoria"])

    # Lê todos os favoritos únicos
    favoritos = pd.DataFrame(remover_duplicatas(ler_favoritos(CAMINHO_FAVORITOS)))

    # Remove as URLs já presentes na amostra, para não rotular duas vezes
    ja_rotulados = set(pd.read_csv(CAMINHO_ROTULADA, dtype=str)["url"])
    favoritos = favoritos[~favoritos["url"].isin(ja_rotulados)].copy()

    # Probabilidade de cada classe; a maior delas é a confiança da previsão
    probabilidades = modelo.predict_proba(preparar_texto(favoritos))
    favoritos["previsto"] = modelo.predict(preparar_texto(favoritos))
    favoritos["confianca"] = probabilidades.max(axis=1)

    # Ordena da menor para a maior confiança e pega o lote
    lote = favoritos.sort_values("confianca").head(TAMANHO_LOTE)

    # Coluna para você preencher com a categoria correta
    lote["categoria"] = ""

    # Salva em dados/ (fora do Git)
    lote[["titulo", "url", "previsto", "confianca", "categoria"]].to_csv(
        CAMINHO_REVISAO, index=False, encoding="utf-8-sig"
    )
    print(f"Lote de {len(lote)} itens gravado em {CAMINHO_REVISAO}.")


if __name__ == "__main__":
    selecionar_revisao()