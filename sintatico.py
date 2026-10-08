"""Analisador sintatico preditivo com esquema de traducao dirigido por sintaxe."""

from tokens import Tipo, ErroCompilacao


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = lexer.proximo_token()

    def erro(self, esperado, lin):
        return ErroCompilacao(
            f"Erro sintatico na linha {lin}: esperado {esperado}, "
            f"mas encontrado '{self.lookahead.lexema}'"
        )

    def match(self, t):
        if self.lookahead.tipo == t:
            self.lookahead = self.lexer.proximo_token()
        else:
            raise self.erro(t.value, self.lookahead.linha)

    # program -> Matexpr block
    def program(self):
        self.match(Tipo.MATEXPR)
        self.block()
        if self.lookahead.tipo != Tipo.EOF:
            raise self.erro(Tipo.EOF.value, self.lookahead.linha)

    # block -> { decls stmts }
    def block(self):
        self.match(Tipo.LCHAVE)
        self.match(Tipo.RCHAVE)