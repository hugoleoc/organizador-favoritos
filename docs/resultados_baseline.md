# Resultados baseline: classificação de favoritos

**Data:** 8 de novembro de 2026
**Commit:** 057a8a1
**Script:** `src/treino.py`

## Objetivo

Medir o desempenho inicial de um classificador de texto que atribui uma categoria principal a cada favorito, usando título e URL como entrada.

## Dados

- **Fonte:** exportação HTML dos favoritos do Chrome, lida por `src/organizador.py`.
- **Tratamento:** remoção de duplicatas por URL normalizada.
- **Amostra:** 150 itens sorteados sem reposição, com semente 42 (`src/amostra.py`).
- **Rotulagem:** manual, com uma categoria principal por item.
- **Exclusão:** 7 itens marcados como `Sem categoria` foram removidos do treino, pois são páginas que falharam no carregamento e não representam um tema. Restaram **143 itens**.

## Configuração do modelo

- **Entrada:** título e URL concatenados, em minúsculas.
- **Vetorização:** TF-IDF com unigramas e bigramas (`ngram_range=(1, 2)`).
- **Classificador:** regressão logística com `class_weight="balanced"` e `max_iter=1000`.
- **Avaliação:** validação cruzada estratificada com 2 dobras e semente 42.

Duas dobras foram escolhidas porque a menor classe tinha 2 exemplos. Com essa configuração, o modelo treina com cerca de metade dos dados por vez, então os números abaixo tendem a ser **pessimistas**.

## Resultados

### Leitura

- **Accuracy de 0.55** contra um acaso de cerca de 10% (10 categorias). Há sinal nos dados.
- **Categorias com desempenho razoável:** `Cultura`, `Computação`, `Trabalho`, `Leis` e `Educação`. Títulos e domínios dessas categorias são informativos.
- **Categorias zeradas:** `Arte`, `Ética`, `Saúde` e `Comunicação`. Têm entre 2 e 3 exemplos no total, o que não permite aprendizado. A causa é volume, não o código.
- **Arquitetura** tem precisão e revocação baixas, e tende a se confundir com `Educação` e `Trabalho`. Isso pode indicar fronteira entre as categorias mal definida, além de falta de dados.

## Limitações

- Amostra pequena (143 itens após exclusões), com classes desbalanceadas.
- Classes com 2 a 3 exemplos produzem métricas sem significância estatística.
- Validação com 2 dobras subestima o desempenho.
- Títulos genéricos ou vazios limitam a informação disponível ao modelo.
- Páginas que falharam no carregamento foram excluídas e não foram testadas.
- A rotulagem foi feita por uma única pessoa, sem medida de concordância.

## Próximos passos

1. Ampliar a rotulagem das categorias fracas (meta de 10 a 15 exemplos por classe).
2. Revisar as definições de Arquitetura, Educação e Trabalho, com critérios escritos para os casos de fronteira.
3. Repetir o treino com `n_splits=5` quando a amostra crescer.
4. Comparar o `macro avg` de cada rodada com este baseline.

## Reprodução

```bash
conda activate favoritos
python -m src.amostra
python -m src.treino
```