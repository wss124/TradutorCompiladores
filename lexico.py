
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

def eh_digito(ch):
    return "0" <= ch <= "9"

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

    def ignorar_brancos_e_comentarios(self):
        """Ignora espacos, tabulacoes, saltos de linha e comentarios estilo C."""
        while not self.fim():
            ch = self.atual()
            if ch in " \t\n\r":
                self.avancar()
            elif ch == "/" and self.proximo() == "/":        
                while not self.fim() and self.atual() != "\n":
                    self.avancar()
            elif ch == "/" and self.proximo() == "*":      
                linha_inicio = self.linha
                self.avancar()
                self.avancar()
                while True:
                    if self.fim():
                        raise self.erro(f"comentario aberto na linha {linha_inicio} nao foi fechado")
                    if self.atual() == "*" and self.proximo() == "/":
                        self.avancar()
                        self.avancar()
                        break
                    self.avancar()
            else:
                return

    def proximo_token(self):
        self.ignorar_brancos_e_comentarios()
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
            if eh_digito(self.atual()) or self.atual() == "_":
               raise self.erro(f"identificador invalido iniciado por '{lex}' (use apenas letras)")
            if lex == "Matexpr":
                return Token(Tipo.MATEXPR, lex, lin)
            if lex in ("int", "float"):
                return Token(Tipo.TYPE, lex, lin)   
            return Token(Tipo.ID, lex, lin)

        # num: inteiro (123) ou ponto flutuante (12.5)
        if eh_digito(ch):
            inicio = self.pos
            while not self.fim() and eh_digito(self.atual()):
                self.avancar()
            if self.atual() == ".":
                self.avancar()
                if not eh_digito(self.atual()):
                    raise self.erro("numero mal formado: esperado digito apos o '.'")
                while not self.fim() and eh_digito(self.atual()):
                    self.avancar()
                if eh_letra(self.atual()):
                    raise self.erro("numero mal formado: letra logo apos o numero")
            return Token(Tipo.NUM, self.fonte[inicio:self.pos], lin)

        
        if ch in SIMBOLOS:
            self.avancar()
            return Token(SIMBOLOS[ch], ch, lin)

        raise self.erro(f"caractere invalido '{ch}'")