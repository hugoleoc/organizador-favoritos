# Importa a função que vamos implementar em src/organizador.py
from src.organizador import normalizar_url

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
