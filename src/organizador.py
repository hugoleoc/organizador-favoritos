# Biblioteca que interpreta HTML e facilita a busca de tags
from bs4 import BeautifulSoup

# Caminho do arquivo exportado pelo Chrome, relativo à raiz do projeto
CAMINHO_ENTRADA = "dados/favoritos.html"


def ler_favoritos(caminho):
    """Lê o arquivo HTML e retorna uma lista de dicionários com título e URL."""

    # Abre o arquivo em modo leitura, com UTF-8 para preservar acentos
    with open(caminho, encoding="utf-8") as arquivo:
        # Converte o conteúdo em uma árvore que o BeautifulSoup consegue percorrer
        sopa = BeautifulSoup(arquivo, "html.parser")

    favoritos = []

    # Busca todas as tags <a>, que são os links salvos
    for link in sopa.find_all("a"):
        # get("href") retorna a URL, ou None se o atributo não existir
        url = link.get("href")

        # Ignora âncoras sem URL
        if not url:
            continue

        # Guarda o título (texto do link) e a URL em um dicionário
        favoritos.append({
            "titulo": link.get_text(strip=True),  # strip=True remove espaços extras
            "url": url,
        })

    return favoritos


# Bloco executado apenas quando o arquivo é rodado diretamente
if __name__ == "__main__":
    itens = ler_favoritos(CAMINHO_ENTRADA)
    print(f"Total de favoritos lidos: {len(itens)}")

    # Mostra os cinco primeiros para conferência
    for item in itens[:5]:
        print(item["titulo"], "->", item["url"])