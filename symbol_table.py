# ============================================================
#   symbol_table.py — Tabela de símbolos (SQLite)
# ============================================================

import sqlite3
from tokens import TokenType, KEYWORDS


# --- Símbolos pré-carregados --------------------------------
#     (nome, tipo, valor_inicial)

PRELOADED_SYMBOLS = [
    # palavras-chave da linguagem
    *[(kw, TokenType.KEYWORD, None) for kw in sorted(KEYWORDS)],
    # constantes built-in
    ("true",  TokenType.KEYWORD, "1"),
    ("false", TokenType.KEYWORD, "0"),
    ("null",  TokenType.KEYWORD, "0"),
]


class SymbolTable:
    def __init__(self, db_path: str = "symbols.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()
        self._preload()

    # --- Estrutura do banco ---------------------------------

    def _create_table(self):
        """Cria a tabela se ainda não existir."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS symbols (
                name          TEXT    PRIMARY KEY,
                type          TEXT    NOT NULL,
                initial_value TEXT,
                first_line    INTEGER,
                occurrences   INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()

    def _preload(self):
        """Insere os símbolos pré-definidos (ignora se já existirem)."""
        self.conn.executemany("""
            INSERT OR IGNORE INTO symbols (name, type, initial_value, first_line)
            VALUES (?, ?, ?, NULL)
        """, PRELOADED_SYMBOLS)
        self.conn.commit()

    # --- API pública ----------------------------------------

    def add(self, name: str, type: str, first_line: int):
        """
        Insere um novo símbolo.
        Se já existir, incrementa o contador de ocorrências.
        """
        existing = self.get(name)
        if existing:
            self.conn.execute("""
                UPDATE symbols SET occurrences = occurrences + 1 WHERE name = ?
            """, (name,))
        else:
            self.conn.execute("""
                INSERT INTO symbols (name, type, first_line)
                VALUES (?, ?, ?)
            """, (name, type, first_line))
        self.conn.commit()

    def get(self, name: str) -> dict | None:
        """Retorna o símbolo pelo nome, ou None se não existir."""
        row = self.conn.execute(
            "SELECT * FROM symbols WHERE name = ?", (name,)
        ).fetchone()

        if row is None:
            return None

        cols = ["name", "type", "initial_value", "first_line", "occurrences"]
        return dict(zip(cols, row))

    def all(self) -> list[dict]:
        """Retorna todos os símbolos da tabela."""
        rows = self.conn.execute(
            "SELECT * FROM symbols ORDER BY first_line NULLS FIRST, name"
        ).fetchall()
        cols = ["name", "type", "initial_value", "first_line", "occurrences"]
        return [dict(zip(cols, row)) for row in rows]

    def close(self):
        self.conn.close()