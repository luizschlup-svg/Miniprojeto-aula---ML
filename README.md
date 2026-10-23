# Festa em Cena — Análise dos pedidos de Halloween

Mini-projeto do Módulo 1 (Semana 07) do curso de Machine Learning e Python.

A Festa em Cena é uma loja fictícia de fantasias e acessórios de Halloween. A base
tem 1.500 pedidos de agosto a novembro de 2024 e 2025, com problemas de qualidade
colocados de proposito para treinar limpeza de dados.

O programa lê o CSV, arruma os textos, valida os números e as datas, testa uma
hipótese e conta os pedidos por canal e por ano-mês. Todo o código está em
`main.py`.

## Como entender a base

Cada linha é **um pedido de um único produto**. O `pedido_id` identifica o pedido
e não se repete nesta base, então contar linhas é contar pedidos. Já a coluna
`quantidade` mostra quantas unidades vieram no pedido: 3 unidades não são 3 pedidos.

Escolhi quatro colunas para explicar:

| Coluna | O que significa |
|---|---|
| `data_venda` | Data e hora da venda, em texto no formato `AAAA-MM-DD HH:MM:SS`. Uso para agrupar por mês. |
| `categoria` | Tipo do produto (fantasia ou acessório). Vem com espaços, pontuação e maiúsculas diferentes, por isso precisa de limpeza. |
| `canal_venda` | Onde o pedido foi feito: `Mercado`, `Loja física` ou `Web`. Também vem com variações de escrita. |
| `status_pedido` | Situação do pedido: `Concluído`, `Cancelado` ou `Devolvido`. Uso para contar cancelados e testar a hipótese da entrega. |

## Como rodar

1. Coloque o arquivo `halloween_vendas.csv` na pasta `data/`.
2. Instale o Pandas: `pip install pandas`
3. Abra o terminal na pasta do projeto e rode: `python main.py`

O resultado aparece no terminal e três arquivos são salvos na pasta `saida/`.

Se os acentos aparecerem estranhos no PowerShell, rode `chcp 65001` antes de
executar.

## O que o programa faz

1. Lê o CSV com Pandas, usando vírgula e UTF-8, e mostra as primeiras linhas.
2. Limpa as categorias com `strip()`, `lower()` e `re.sub()`. Categoria vazia vira
   `sem categoria`.
3. Padroniza o canal para Mercado, Loja física ou Web.
4. Valida a quantidade (inteiro maior que zero) e o preço (não negativo). Quem tem
   problema é marcado, não corrigido.
5. Converte as datas com `strptime()` e cria as colunas de ano, mês, dia, hora e
   data brasileira.
6. Vê se todo pedido sem data de entrega está cancelado.
7. Conta os pedidos por canal e por ano-mês, mostrando o que ficou de fora.
8. Salva os pedidos com problema e as contagens na pasta `saida/`.

## Resultados

| O que | Número |
|---|---:|
| Linhas lidas | 1.500 |
| Categorias vazias preenchidas | 18 |
| Categorias não vazias alteradas | 131 |
| Pedidos com quantidae inválida | 7 |
| Pedidos com preço inválido | 12 |
| Pedidos com problema numérico | 19 |
| Datas de venda inválidas | 4 |

### Duas descobertas

1. **O canal Web tem mais pedidos:** 666 de 1.500 (44,4%), contra 551 da Loja
   física (36,7%) e 283 do Mercado (18,9%). Isso mostra onde há mais pedidos
   registrados, mas não quer dizer mais receita: a conta inclui cancelados e
   devolvidos e não olha o valor.

2. **Outubro concentra os pedidos:** foram 393 em 2024 e 410 em 2025, o maior mês
   nos dois anos. O resultado combina com o Halloween, mas a base é fictícia e só
   tem quatro meses por ano, então não dá para generalizar.

### Entrega sem data

A hipótese de que todo pedido sem data de entrega estaria cancelado é **falsa**.
Dos 143 pedidos sem entrega, 109 estão cancelados, mas 34 têm outro status. Ou
seja, "sem entrega" não quer dizer "cancelado".

## Regras que adotei

- **Textos:** usei `strip()`, `lower()` e `re.sub()` para tirar espaços e pontuação
  das categorias. Categoria vazia virou `sem categoria`, e os canais foram
  padronizados para `Mercado`, `Loja física` e `Web`.
- **Números:** a quantidade precisa ser um inteiro maior que zero, e o preço
  precisa estar preenchido e ser maior ou igual a zero. Os 7 pedidos com
  quantidade inválida e os 12 com preço vazio foram marcados e separados, sem
  correção.
- **Datas:** usei `strptime()` no formato exato da base. As 4 datas com texto
  inválido ficaram marcadas e fora das contagens, e não troquei nenhuma pela data
  de hoje. As colunas `publico` e `tamanho` não tinham valores vazios.

## Limitações

- A base é fictícia e só tem quatro meses de cada ano, então não serve para tirar
  conclusoes sobre o mercado real.
- As contagens são de pedidos registrados, não de receita.
- Valores inválidos foram marcados e separados, nunca corrigidos ou estimados.

## Reflexão: ML e qualidade de dados

Antes de usar esses dados em Machine Learning, é preciso conferir se eles estão
confiáveis. Se a base tem categoria vazia, quantidade negativa, preço faltando ou
data inválida, o modelo aprende errado. Ele pode achar que um pedido com -1 unidade
é normal ou tratar uma data ruim como se fosse outra qualquer.

Neste projeto eu não treinei nenhum modelo. O objetivo foi só limpar e conhecer a
base. Mesmo assim, dá para ver que a limpeza ajuda, mas não resolve tudo: um modelo
também precisa de dados representativos, de variáveis bem escolhidas e de uma
avaliação feita com dados que ele ainda não viu.

Se eu fosse treinar algo com essa base, teria cuidado com dois problemas:
**overfitting**, quando o modelo decora os dados que viu e vai mal em dados novos,
e **underfitting**, quando ele é simples demais e não aprende nem o padrão básico.
Limpar os dados não evita nenhum dos dois sozinho; também é preciso testar e
comparar os resultados.

Por fim, esta base é fictícia, tem só 1.500 pedidos e quatro meses de cada ano.
Ela serve para aprender a limpar e explorar, mas não para tirar conclusões sobre
o mercado real.

O relatório curto pedido na atividade está em [`report.md`](report.md).
