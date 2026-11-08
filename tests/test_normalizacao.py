# Importa a função que vamos implementar em src/organizador.py
from src.organizador import normalizar_url, remover_duplicatas

def test_remove_duplicatas_mantem_primeira_ocorrencia():
    # Duas URLs que só diferem por http/https e utm_* devem virar uma só
    favoritos = [
        {"titulo": "Página A", "url": "http://site.com/pagina/"},
        {"titulo": "Página A (cópia)", "url": "https://site.com/pagina?utm_source=x"},
        {"titulo": "Outra", "url": "https://site.com/outra"},
    ]
    resultado = remover_duplicatas(favoritos)
    assert len(resultado) == 2
    assert resultado[0]["titulo"] == "Página A"


def test_http_vira_https():
    # http e https do mesmo endereço devem ser tratados como iguais
    assert normalizar_url("https://site.com/pagina/") == "https://site.com/pagina"

def test_dominio_em_minusculas_caminho_preservado():
    # O domínio é case-insensitive, mas o caminho pode diferenciar páginas
    assert normalizar_url("https://Exemplo.COM/Pagina") == "https://exemplo.com/Pagina"

def test_remove_barra_final():
    # /pagina/ e /pagina apontma para o mesmo conteúdo na prática
    assert normalizar_url("https://site.com/pagina/") == "https://site.com/pagina"

def test_remove_parametros_utm_mantem_busca():
    # utm_* é rastreamento e sai; q= altera o conteúdo e fica
    url = "https://site.com/busca?utm_source=x&q=python"
    assert normalizar_url(url) == "https://site.com/busca?q=python"
