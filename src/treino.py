# Ferramentas de pré-processamento, modelo e avaliação do scikit-learn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline

# Caminho do CSV rotulado, relativo à raiz do projeto
CAMINHO_DADOS = "dados/amostra_rotulagem.csv"

# Semente fixa, para o resultado ser reproduzível
SEMENTE = 42


def preparar_texto(tabela):
    """Junta título e URL em um único texto por linha, para o TF-IDF."""

    # fillna("") evita erro com células vazias; a URL ajuda quando o título é genérico
    return (tabela["titulo"].fillna("") + " " + tabela["url"].fillna("")).str.lower()


def treinar():
    """Treina o classificador de categoria principal e imprime as métricas."""

    # Lê o CSV rotulado e descarta linhas sem categoria
    tabela = pd.read_csv(CAMINHO_DADOS).dropna(subset=["categoria"])

    # Remove as páginas que falharam no carregamento; não são um tema
    tabela = tabela[tabela["categoria"] != "Sem categoria"]

    # Texto de entrada (X) e rótulo de saída (y)
    X = preparar_texto(tabela)
    y = tabela["categoria"]

    # Pipeline une TF-IDF e regressão logística, para o vetorizador ser ajustado só nos dados de treino de cada dobra
    modelo = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2)),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )

    # Duas dobras, porque a menor classe restante tem poucos exemplos
    validacao = StratifiedKFold(n_splits=2, shuffle=True, random_state=SEMENTE)

    # Gera uma previsão para cada linha, sempre com dados que o modelo não viu naquela dobra
    previsto = cross_val_predict(modelo, X, y, cv=validacao)

    # Relatório com precisão, revocação e F1 por categoria
    print(classification_report(y, previsto, zero_division=0))


if __name__ == "__main__":
    treinar()