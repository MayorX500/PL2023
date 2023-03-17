#!/usr/bin/env python3

from dataclasses import dataclass
import re
import ply.lex as lex

# Define
BLOCKED: int = -2
ERROR: int = -1
SUCCESS: int = 0
BALANCE: int = 1
EXIT: int = 10

# List of token names.   This is always required
tokens: tuple[str] = ("LEVANTAR", "POUSAR", "MOEDA", "NUMERO", "ABORTAR")

# Regular expression rules for simple tokens
t_LEVANTAR: str = r"(?i)levantar"
t_POUSAR: str = r"(?i)pousar"
t_ABORTAR: str = r"(?i)abortar"

# A Regular Expression for phone numbers
def t_NUMERO(t):
    r"(?i)t=(\d+)"
    t.value = t.value[2:].strip()
    return t

# A Regular Expression for coins
def t_MOEDA(t):
    r"(?i)(moeda)(\s\d+[c|e],*)+"
    t.value = t.value.strip()
    t.value = re.sub(r"(?i)moeda ", "", t.value)
    t.value = re.sub(r",","", t.value)
    t.value = re.split(r"\s", t.value)
    return t

# A Regular Expression to ignore spaces, commas and points
def t_ignore_SPACE_POINT_COMMA(t):
    r"[ ,.]+"
    pass
    # No return value. Token discarded

# Track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    #probably should handle this better
    print(f"Command not recognized: {t.value}")
    t.lexer.skip(len(t.value))

# Build the lexer
lexer: lex.lexer = lex.lex()

## Test
test = """levantar
moeda 1c, 2c, 58c 10c, 20c, 50c 1e 2e
t=123456789
abortar
pousar"""

lexer.input(test)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
