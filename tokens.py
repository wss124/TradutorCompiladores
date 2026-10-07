"""Tokens do tradutor: tipos de token, estrutura do token e erro de compilacao."""

from dataclasses import dataclass
from enum import Enum


class Tipo(Enum):
    MATEXPR = "'Matexpr'"
    TYPE = "tipo (int ou float)"
    ID = "identificador"
    NUM = "numero"
    LCHAVE = "'{'"
    RCHAVE = "'}'"
    LPAREN = "'('"
    RPAREN = "')'"
    PVIRG = "';'"
    MAIS = "'+'"
    MENOS = "'-'"
    VEZES = "'*'"
    DIV = "'/'"
    EOF = "fim do arquivo"


@dataclass
class Token:
    tipo: Tipo
    lexema: str
    linha: int


class ErroCompilacao(Exception):
    pass