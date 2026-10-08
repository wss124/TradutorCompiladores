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
        self.decls()
        self.stmts()
        self.match(Tipo.RCHAVE)
         # decls -> decl decls | e
    def decls(self):
        if self.lookahead.tipo == Tipo.TYPE:
            self.decl()
            self.decls()
        # senao: producao vazia

    # decl -> type id ;
    def decl(self):
        self.match(Tipo.TYPE)
        self.match(Tipo.ID)
        self.match(Tipo.PVIRG)
        # stmts -> stmt stmts | e      (FOLLOW(stmts) = { '}' })
    def stmts(self):
       if self.lookahead.tipo not in (Tipo.RCHAVE, Tipo.EOF):
           self.stmt()
           self.stmts()
   # stmt -> block | expr ;
    def stmt(self):
       if self.lookahead.tipo == Tipo.LCHAVE:
           self.block()
       else:
           self.expr()
           self.match(Tipo.PVIRG)

    # expr -> term restoE
    def expr(self):
        self.term()
        self.resto_e()

    # restoE -> + term {print('+')} restoE | - term {print('-')} restoE | e
    def resto_e(self):
        if self.lookahead.tipo == Tipo.MAIS:
            self.match(Tipo.MAIS); self.term(); self.resto_e()
        elif self.lookahead.tipo == Tipo.MENOS:
            self.match(Tipo.MENOS); self.term(); self.resto_e()

    # term -> fact restoT
    def term(self):
        self.fact()
        self.resto_t()

    # restoT -> * fact {print('*')} restoT | / fact {print('/')} restoT | e
    def resto_t(self):
        if self.lookahead.tipo == Tipo.VEZES:
            self.match(Tipo.VEZES); self.fact(); self.resto_t()
        elif self.lookahead.tipo == Tipo.DIV:
            self.match(Tipo.DIV); self.fact(); self.resto_t()

    # fact -> ( expr ) | num {print(num)} | id {print(id)}
    def fact(self):
        if self.lookahead.tipo == Tipo.LPAREN:
            self.match(Tipo.LPAREN)
            self.expr()
            self.match(Tipo.RPAREN)
        elif self.lookahead.tipo in (Tipo.NUM, Tipo.ID):
            self.match(self.lookahead.tipo)
        else:
            raise self.erro("'(', numero ou identificador", self.lookahead.linha)