# Trabalho I - Compiladores 2026.2

Tradutor de expressoes aritmeticas da notacao **infixa** para a **pos-fixa**, implementado em Python.
O tradutor le um arquivo em disco e exibe o resultado na tela.

> Em desenvolvimento.

## Como executar

````
python tradutor.py exemplo.txt
````

## Gramatica

A gramatica do enunciado precisou de dois ajustes, seguindo o modelo do livro-texto (Aho et al., cap. 2):

1. `stmt -> block` era a unica producao de `stmt`, entao `expr` nao era alcancavel. Foi adicionada `stmt -> expr ;`.
2. `stmts -> stmts stmt` nao tinha caso base. Foi adicionada `stmts -> e`.

Depois, a recursao a esquerda foi eliminada (necessario para o analisador preditivo) e as acoes semanticas foram inseridas:

````
program -> Matexpr block
block   -> { decls stmts }
decls   -> decl decls | e
decl    -> type id ;
stmts   -> stmt stmts | e
stmt    -> block | expr ;
expr    -> term restoE
restoE  -> + term { print('+') } restoE
         | - term { print('-') } restoE
         | e
term    -> fact restoT
restoT  -> * fact { print('*') } restoT
         | / fact { print('/') } restoT
         | e
fact    -> ( expr ) | num { print(num) } | id { print(id) }
````