
from tokens import Tipo, Token, ErroCompilacao


SIMBOLOS = {
    "{": Tipo.LCHAVE, "}": Tipo.RCHAVE,
    "(": Tipo.LPAREN, ")": Tipo.RPAREN,
    ";": Tipo.PVIRG,
    "+": Tipo.MAIS, "-": Tipo.MENOS,
    "*": Tipo.VEZES, "/": Tipo.DIV,
}

def eh_letra(ch):
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z")


class Lexer:
    def __init__(self, fonte):
        self.fonte = fonte
        self.pos = 0
        self.linha = 1

    def fim(self):
        return self.pos >= len(self.fonte)

    def atual(self):
        return self.fonte[self.pos] if not self.fim() else ""

    def proximo(self):
        return self.fonte[self.pos + 1] if self.pos + 1 < len(self.fonte) else ""

    def avancar(self):
        if self.atual() == "\n":
            self.linha += 1
        self.pos += 1

    def erro(self, msg):
        return ErroCompilacao(f"Erro lexico na linha {self.linha}: {msg}")

    def ignorar_brancos(self):
        """Ignora espacos, tabulacoes e saltos de linha."""
        while not self.fim() and self.atual() in " \t\n\r":
            self.avancar()

    def proximo_token(self):
        self.ignorar_brancos()
        lin = self.linha

        if self.fim():
            return Token(Tipo.EOF, "EOF", lin)

        ch = self.atual()

        # id, type ou Matexpr: apenas letras do alfabeto
        if eh_letra(ch):
            inicio = self.pos
            while not self.fim() and eh_letra(self.atual()):
                self.avancar()
            lex = self.fonte[inicio:self.pos]
            if lex == "Matexpr":
                return Token(Tipo.MATEXPR, lex, lin)
            if lex in ("int", "float"):
                return Token(Tipo.TYPE, lex, lin)
            return Token(Tipo.ID, lex, lin)
        
        if ch in SIMBOLOS:
            self.avancar()
            return Token(SIMBOLOS[ch], ch, lin)

        raise self.erro(f"caractere invalido '{ch}'")