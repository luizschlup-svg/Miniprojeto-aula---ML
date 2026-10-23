# Relatório — Festa em Cena

## O que eu fiz

Analizei 1.500 pedidos fictícios de fantasias e acessórios de Halloween, de agosto a novembro de 2024 e 2025, nos canais Mercado, Loja física e Web. Cada linha é um pedido de um produto só, mas pode ter várias unidades.

Li o arquivo com Pandas sem mexer no original. Criei colunas novas para guardar as versões limpas e os avisos de problema, sem inventar nenhum valor.

## Limpeza dos dados

Nas categorias usei `strip()`, `lower()` e `re.sub()` para tirar espaços e pontuaçao. Das 1.500 linhas, 18 estavam vazias e viraram "sem categoria". Outras 131 tinham espaços, pontuação ou letras maiúsculas e foram corrigidas. No fim ficaram 979 fantasias, 503 acessórios e 18 sem categoria.

Os canais foram padronizados para Mercado, Loja física e Web, e todos foram reconhecidos.

Encontrei 7 quantidades inválidas, todas com -1, e 12 preços vazios. Nenhum pedido tinha os dois problemas, então o total ficou em 19. Marquei e separei esses pedidos, mas não corrigi os valores.

Quatro datas de venda estavam com o texto "data_invalida". Elas ficaram fora das contagens por período e não foram trocadas pela data de hoje.

## Entrega sem data

A hipótese era que todo pedido sem `data_entrega` estaria cancelado. Ela é falsa. Dos 143 pedidos sem entrega, 109 são Cancelado, mas 34 têm outro status. Os exemplos são os pedidos 1170 e 990, os dois Concluído, e o 740, também Concluído, com data de venda inválida.

Então não posso usar "sem data de entrega" como sinonimo de cancelamento. O campo deve continuar vazio.

## Duas descobertas

1. **Canal:** a Web registra 666 pedidos (44,4%), a Loja física 551 (36,7%) e o Mercado 283 (18,9%). O site tem mais pedidos, mas isso não quer dizer mais receita: a conta inclui cancelados e devolvidos e não olha valor.

2. **Período:** outubro soma 803 dos 1.496 pedidos com data válida (53,7%), sendo 393 em 2024 e 410 em 2025. Foi o mês com mais pedidos nos dois anos. O resultado faz sentido com o Halloween, mas a base é fictícia e só tem quatro meses por ano, então não dá para generalizar.

## Conclusão

A base ficou organizada o suficiente para contagens descritivas, mas não serve para falar de receita nem do mercado real. Custos e descontos não entraram na análise.
