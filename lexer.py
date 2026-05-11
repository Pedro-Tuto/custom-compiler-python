# ============================================================
#   lexer.py — Analisador léxico
# ============================================================

from typing import List, Optional
from tokens import Token, TokenType, KEYWORDS


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos    = 0       # posição atual no código-fonte
        self.line   = 1       # linha atual (para rastreamento de erros)
        self.tokens: List[Token] = []

    # --- Utilitários de navegação ---------------------------

    def current(self) -> Optional[str]:
        """Caractere na posição atual, ou None se chegou ao fim."""
        return self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self) -> Optional[str]:
        """Próximo caractere sem consumir (lookahead de 1)."""
        nxt = self.pos + 1
        return self.source[nxt] if nxt < len(self.source) else None

    def advance(self) -> str:
        """Consome e retorna o caractere atual; atualiza o número de linha."""
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
        return ch

    # --- Ignorar espaços e comentários ----------------------

    def skip_whitespace_and_comments(self):
        """Pula espaços em branco e comentários de linha (//)."""
        while self.current() is not None:
            if self.current() in " \t\r\n":
                self.advance()
            elif self.current() == "/" and self.peek() == "/":
                # comentário: ignora até o fim da linha
                while self.current() not in (None, "\n"):
                    self.advance()
            else:
                break

    # --- Leitores de token ----------------------------------

    def read_number(self) -> Token:
        """Lê um literal numérico inteiro ou decimal."""
        line, value = self.line, ""

        while self.current() and self.current().isdigit():
            value += self.advance()

        # parte decimal opcional
        if self.current() == "." and self.peek() and self.peek().isdigit():
            value += self.advance()
            while self.current() and self.current().isdigit():
                value += self.advance()

        return Token(TokenType.NUMBER, value, line)

    def read_identifier(self) -> Token:
        """Lê um identificador e verifica se é palavra-chave."""
        line, value = self.line, ""

        while self.current() and (self.current().isalnum() or self.current() == "_"):
            value += self.advance()

        token_type = TokenType.KEYWORD if value in KEYWORDS else TokenType.IDENTIFIER
        return Token(token_type, value, line)

    def read_string(self) -> Token:
        """Lê uma string delimitada por aspas duplas."""
        line = self.line
        self.advance()  # consome a aspa inicial

        value = ""
        while self.current() and self.current() != '"':
            value += self.advance()

        if self.current() == '"':
            self.advance()  # consome a aspa final

        return Token(TokenType.STRING, value, line)

    def read_operator_or_delimiter(self) -> Token:
        """Lê operadores (simples e compostos) e delimitadores."""
        line = self.line
        ch   = self.advance()

        # operadores compostos: == !=
        if ch in ("=", "!") and self.current() == "=":
            return Token(TokenType.COMPARE_OP, ch + self.advance(), line)

        if ch in ("<", ">"):   return Token(TokenType.COMPARE_OP, ch, line)
        if ch == "=":          return Token(TokenType.ASSIGN_OP,  ch, line)
        if ch in "+-*/":       return Token(TokenType.ARITH_OP,   ch, line)
        if ch in "(){};,":     return Token(TokenType.DELIMITER,   ch, line)

        return Token(TokenType.INVALID, ch, line)

    # --- Método principal -----------------------------------

    def tokenize(self) -> List[Token]:
        """Percorre o código-fonte e retorna a lista completa de tokens."""
        while True:
            self.skip_whitespace_and_comments()

            if self.current() is None:
                self.tokens.append(Token(TokenType.EOF, "EOF", self.line))
                break

            ch = self.current()

            if ch.isdigit():              self.tokens.append(self.read_number())
            elif ch.isalpha() or ch == "_": self.tokens.append(self.read_identifier())
            elif ch == '"':               self.tokens.append(self.read_string())
            else:                         self.tokens.append(self.read_operator_or_delimiter())

        return self.tokens