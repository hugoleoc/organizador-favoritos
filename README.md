# Organizador de Favoritos

Ferramenta em Python que lê os favoritos exportados do Chrome, remove duplicatas e agrupa as páginas por categoria de conteúdo.

## Entrada
Arquivo HTML exportado pelo Chrome (Gerenciador de favoritos → Exportar favoritos).

## Saída
Lista de favoritos sem duplicatas, organizada nas categorias abaixo.

## Regra de duplicata
Dois favoritos são duplicados quando têm a mesma URL normalizada. A normalização segue estas etapas:
- esquema `http` e `https` tratados como iguais (ambos viram `https`);
- domínio em minúsculas;
- barra final removida;
- parâmetros de rastreamento (`utm_*`) removidos;
- parâmetros de busca (`?q=...`) mantidos, pois alteram o conteúdo da página.

## Categorias
Arquitetura, Arte, IA, Computação, Leis, Ética, Educação, Cultura, Comunicação, Física, Química, Biologia, Saúde e Trabalho.

## Como executar

```bash
conda create -n favoritos python=3.11 -y
conda activate favoritos
pip install beautifulsoup4 pandas scikit-learn pytest
python -m pytest -v
python -m src.amostra
python -m src.treino
```

## Estrutura

- `src/organizador.py`: leitura, normalização, remoção de duplicatas e classificação por palavras-chave.
- `src/amostra.py`: gera a amostra aleatória de favoritos para rotulagem.
- `src/treino.py`: treina o classificador TF-IDF com regressão logística.
- `tests/`: testes automatizados com pytest.
- `docs/`: documentação dos resultados.

## Status

Fase 1 concluída: pipeline de leitura, limpeza e classificação com dados rotulados manualmente. Resultados em `docs/resultados_baseline.md`.