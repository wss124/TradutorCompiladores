import sys

from tokens import ErroCompilacao
from lexico import Lexer
from sintatico import Parser


def main():
    if len(sys.argv) < 2:
        print("Uso: python tradutor.py <arquivo>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            fonte = f.read()
    except OSError:
        print(f"Erro: nao foi possivel abrir o arquivo '{sys.argv[1]}'", file=sys.stderr)
        sys.exit(1)

    try:
        Parser(Lexer(fonte)).program()
        print("Traducao concluida sem erros.")
    except ErroCompilacao as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()