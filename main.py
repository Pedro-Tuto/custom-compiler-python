# ============================================================
#   main.py — Ponto de entrada do compilador
# ============================================================

from lexer import Lexer


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
    lexer  = Lexer(SOURCE)
    tokens = lexer.tokenize()

    print(f"{'TYPE':<16} {'VALUE':<12} LINE")
    print("-" * 36)
    for token in tokens:
        print(f"{token.type:<16} {token.value:<12} {token.line}")


if __name__ == "__main__":
    main()