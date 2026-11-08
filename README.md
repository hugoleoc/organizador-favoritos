# Organizador de Favoritos

Ferramenta em Python que lê os favoritos exportados do Chrome, remove duplicatas e agrupa as páginas por categoria de conteúdo.

## Entrada
Arquivo HTML exportado pelo Chrome (Gerenciador de favoritos → Exportar favoritos).

## Saída
Lista de favoritos sem duplicatas, organizada nas categorias abaixo.

## Regra de duplicata
Dois favoritos são duplicados quando têm a mesma URL normalizada:
- domínio em minúsculas;
- barra final removida;
- parâmetros de rastreamento (`utm_*`) removidos.

## Categorias
Arquitetura, Arte, IA, Computação, Leis, Ética, Educação, Cultura, Comunicação, Física, Química, Biologia, Saúde e Trabalho.