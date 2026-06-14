# ============================================================
#   main.py — Ponto de entrada do compilador
# ============================================================

from lexer import Lexer
from symbol_table import SymbolTable


# --- Código-fonte de exemplo --------------------------------

SOURCE = """
// Programa de exemplo
int x = 10;
int y = 20;

if (x != y) {
    print("diferente");
}

while (x > 0) {
    x = x - 1;
}
"""


# --- Execução -----------------------------------------------

def main():
    table  = SymbolTable("symbols.db")
    lexer  = Lexer(SOURCE, table)
    tokens = lexer.tokenize()

    # tokens gerados
    print("=== TOKENS ===")
    print(f"{'TYPE':<16} {'VALUE':<12} LINE")
    print("-" * 36)
    for token in tokens:
        print(f"{token.type:<16} {token.value:<12} {token.line}")

    # tabela de símbolos resultante
    print("\n=== TABELA DE SÍMBOLOS ===")
    print(f"{'NAME':<12} {'TYPE':<14} {'FIRST LINE':<12} {'OCCURRENCES':<11} INITIAL VALUE")
    print("-" * 60)
    for sym in table.all():
        line  = sym["first_line"]  or "-"
        value = sym["initial_value"] or "-"
        print(f"{sym['name']:<12} {sym['type']:<14} {str(line):<12} {sym['occurrences']:<11} {value}")

    table.close()


if __name__ == "__main__":
    main()