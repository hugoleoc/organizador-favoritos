# Biblioteca que interpreta HTML e facilita a busca de tags
from bs4 import BeautifulSoup
# No topo do arquivo, junto ao import do BeautifulSoup:
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

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

def normalizar_url(url):
    """Retorna a forma padronizada de uma URL para detecção de duplicatas."""

    # Separa a URL em partes: esquema, domínio, caminho, query e fragmento
    partes = urlsplit(url)

    # http e https são tratados como o mesmo endereço; ambos viram https
    esquema = "https"

    # O domínio não diferencia maiúsculas de minúsculas, então padronizamos
    dominio = partes.netloc.lower()

    # Remove a barra final, exceto quando o caminho é só "/"
    caminho = partes.path
    if len(caminho) > 1 and caminho.endswith("/"):
        caminho = caminho.rstrip("/")

    # Lê os parâmetros da query como pares (chave, valor)
    parametros = parse_qsl(partes.query, keep_blank_values=True)

    # Mantém só os parâmetros que não são de rastreamento (utm_*)
    parametros_uteis = [(k, v) for k, v in parametros if not k.startswith("utm_")]

    # Recria a query, sem alterar a ordem original dos parâmetros
    query = urlencode(parametros_uteis)

    # Monta a URL final; o fragmento (#...) é descartado, pois não muda a página no servidor
    return urlunsplit((esquema, dominio, caminho, query, ""))

def remover_duplicatas(favoritos):
    """Retorna a lista de favoritos sem URLs duplicadas, mantendo a primeira ocorrência."""

    # Lista que vai receber apenas os favoritos únicos, na ordem original
    resultado = []

    # Conjunto com as URLs normalizadas já vistas; consulta em set é rápida
    vistas = set()

    for item in favoritos:
        # Padroniza a URL antes de comparar, para que variações contem como iguais
        chave = normalizar_url(item["url"])

        # Se a URL já apareceu, este favorito é duplicado e é ignorado
        if chave in vistas:
            continue

        # Primeira ocorrência: registra a URL como vista e guarda o favorito
        vistas.add(chave)
        resultado.append(item)

    return resultado

# Bloco executado apenas quando o arquivo é rodado diretamente
if __name__ == "__main__":
    itens = ler_favoritos(CAMINHO_ENTRADA)
    print(f"Total de favoritos lidos: {len(itens)}")

    # Mostra os cinco primeiros para conferência
    for item in itens[:5]:
        print(item["titulo"], "->", item["url"])