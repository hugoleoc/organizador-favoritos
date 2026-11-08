# Biblioteca para manipular a tabela de rótulos
import pandas as pd

CAMINHO = "dados/amostra_rotulagem.csv"

# Grafias corrigidas para as 14 categorias do README
CORRECOES = {
    "Lei": "Leis",
    "Sem Categoria": "Sem categoria",
}

def normalizar():
    # Lê o CSV mantendo tudo como texto
    tabela = pd.read_csv(CAMINHO, dtype=str)

    # Remove espaços no início e no fim de cada rótulo
    tabela["categoria"] = tabela["categoria"].str.strip()

    # Troca as grafias incorretas pelas oficiais
    tabela["categoria"] = tabela["categoria"].replace(CORRECOES)

    # Grava o arquivo corrigido; o original continua no disco até você sobrescrever
    tabela.to_csv(CAMINHO, index=False, encoding="utf-8-sig")

    # Mostra a contagem final
    print(tabela["categoria"].value_counts(dropna=False))

if __name__ == "__main__":
    normalizar()