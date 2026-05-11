# ============================================================
#   token.py — Definição dos tokens da linguagem
# ============================================================

from dataclasses import dataclass


# --- Tipos de token -----------------------------------------

class TokenType:
    # Literais
    NUMBER      = "NUMBER"
    STRING      = "STRING"

    # Identificadores e palavras-chave
    IDENTIFIER  = "IDENTIFIER"
    KEYWORD     = "KEYWORD"

    # Operadores
    ARITH_OP    = "ARITH_OP"       # + - * /
    ASSIGN_OP   = "ASSIGN_OP"      # =
    COMPARE_OP  = "COMPARE_OP"     # == != < >

    # Delimitadores
    DELIMITER   = "DELIMITER"      # ( ) { } ; ,

    # Especiais
    EOF         = "EOF"
    INVALID     = "INVALID"


# --- Palavras reservadas da linguagem -----------------------

KEYWORDS = {"if", "else", "while", "print", "int", "float", "return"}


# --- Estrutura de um token ----------------------------------

@dataclass
class Token:
    type:   str
    value:  str
    line:   int

    def __repr__(self):
        return f"Token({self.type:<14} | '{self.value}' | line {self.line})"