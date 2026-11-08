from src.organizador import classificar

def test_classifica_pelo_titulo():
    # Um titulo com "bim" deve cair na categoria Arquitetura
    favorito = {"titulo": "Guia de BIM para projetos", "url": "https://site.com/guia"}
    assert classificar(favorito) == "Arquitetura"

def test_classifica_pelo_dominio():
    # Um domínio com "github" deve cair em computação
    favorito = {"titulo": "Repositório", "url": "https://github.com/usuario/repo"}
    assert classificar(favorito) == "Computação"

def test_sem_palavra_chave_vai_para_sem_categoria():
    # Quando nada corresponde, o favorito recebe a categoria de fallback
    favorito = {"titulo": "Página qualquer", "url": "https://exemplo.org/xyz"}
    assert classificar(favorito) == "Sem categoria"
