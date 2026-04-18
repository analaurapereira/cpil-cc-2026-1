# Código fonte em "calculator language" para análise léxica

import sys
from os import POSIX_FADV_NOREUSE


def open_file() -> str:
    if len(sys.argv) < 2:
        print("Forma de usar: phyton lexer.py <nome_arquivo>")
        print("Erro: nome do arquivo não fornecido")
        sys.exit(-1)
    
    filename= sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    except OSError as error:
        print(error)
        sys.exit(-1)
    

# Caracteres considerados "e m branco"
BLANKS = {
    " ",    #Espaço em branco
    "\t",   #Tabulação
    "\n",   #Nova linha
    "\r",   #Retorno de carro
}

#Funçao auxiliares
def is_alpha(c:str) -> bool:
    # Letras maiuscular e minuscular sem acento
    return c.isascii() and c.isalpha()

def is_digit(c:str) -> bool:
    # 0 a 9
    return c.isascii() and c.isdigit()

def is_alphanum(c:str) -> bool:
    # Maiuscul e minuscula sem acento + digito
    return c.isascii() and c.isalnum()


def analyze(source: str) -> None:
    #variáveis de controle
    state = 0
    lexeme = ""
    row = 1
    col = 1
    symbols_table = []

    # Adicione uma quebra de linha ao final do código para possibilitar o processamento 
    # último lexema
    source += "\n"

    # Funçao que opera mudança de estado

    def go_to_state(ch: str, next_state: int) -> tuple[str, int]:
        # Adicione chatual ao lexema e move para o pŕoximo estado
        return lexeme + ch, next_state

    #função que aceita um lexema válido e insere na tabela de simbolos
    def accept(ch: str, terminal: int) -> tuple[str, int]:
        # Se ch for um caracter BLANK, NÃO o adicionamos ao lexema
        lex = lexeme if ch in BLANKS else lexeme + ch
        match terminal:
            case 1001:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "IDENTIFIER",
                    "value": lex
                })
                
            case 1002 | 1003:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "KEYWORD",
                    "value": lex
                })

            case 1004:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "NUMBER",
                    "value": lex
                })
                
            case 1005:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "ASSIGN",
                    "value": lex
                })

            case 1006:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "PLUS",
                    "value": lex
                })
            
            case 1007:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "MINUS",
                    "value": lex
                })
            
            case 1008:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "TIMES",
                    "value": lex
                })

            case 1009:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "DIVIDE",
                    "value": lex
                })
            
            case 1010:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "LPAREN",
                    "value": lex
                })

            case 1011:
                symbols_table.append({
                    "lexeme": lex,
                    "token": "RPAREN",
                    "value": lex
                }) 
        
        return "", 0
    def display_error(ch: str) -> None:
        print(f"ERROR[{row}:{col}]: unexpected char '{ch}' (state{state})")
        sys.exit(-1)

    pos = 0 #posição atual na string
    while pos < len(source):
        ch = source[pos] # Le um caracter do codigo 

        if ch == "\n":
            row += 1
            col = 0   

        match state:
            case 0:
                if ch == "r":
                    lexeme, state = go_to_state(ch, 10)        
                
                elif ch == "w":
                    lexeme, state = go_to_state(ch, 60)

                elif is_alpha(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif is_digit(ch):
                    lexeme, state = go_to_state(ch, 110)

                elif ch == ".":
                    lexeme, state = go_to_state(ch, 130)

                elif ch == ":":
                    lexeme, state = go_to_state(ch, 150)

                elif ch == "+":
                    lexeme, state = accept(ch, 1006)
                    
                elif ch == "-":
                    lexeme, state = accept(ch, 1007)

                elif ch == "*":
                    lexeme, state = accept(ch, 1008)

                elif ch == "/":
                    lexeme, state = accept(ch, 1009)

                elif ch == "(":
                    lexeme, state = accept(ch, 1010)

                elif ch == ")":
                    lexeme, state = accept(ch, 1011)

                elif ch in BLANKS:
                    pass

                else:
                    display_error(ch)

            case 10:
                if ch == "e":
                    lexeme, state = go_to_state(ch,20)
                
                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1001)

            case 20:
                if ch == "a":
                    lexeme, state = go_to_state(ch, 30)
                
                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1001)

            case 30:
                if ch == "d":
                    lexeme, state = go_to_state(ch, 40)
                
                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1001)

            case 40:
                if is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)
                
                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1002)


            case 50:
                if is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1001)

            case 60:  
                if ch == "r":
                    lexeme, state = go_to_state(ch, 70)

                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1001)

            case 70:
                if ch == "i":
                    lexeme, state = go_to_state(ch, 80)

                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1001)

            case 80: 
                if ch == "t":
                    lexeme, state = go_to_state(ch, 90)

                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1001)

            case 90:  
                if ch == "e":
                    lexeme, state = go_to_state(ch, 100)

                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1001)

            case 100: 
                if is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1003)

            case 110: 
                if is_digit(ch):
                    lexeme, state = go_to_state(ch, 110)

                elif ch == ".":
                    lexeme, state = go_to_state(ch, 120)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1004)

            case 120:  
                if is_digit(ch):
                    lexeme, state = go_to_state(ch, 120)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1004)

            case 130:  
                if is_digit(ch):
                    lexeme, state = go_to_state(ch, 140)

                else:
                    display_error(ch)

            case 140:  
                if is_digit(ch):
                    lexeme, state = go_to_state(ch, 140)

                else:
                    pos -= 1
                    col -= 1
                    lexeme, state = accept(" ", 1004)

            case 150:  
                if ch == "=":
                    lexeme, state = accept(ch, 1005)

                else:
                    display_error(ch)
        
        if ch != "\r": col +=1
        pos+=1

    print("----------- TABELA DE SIMBOLOS -----------")
    for symbol in symbols_table: print(symbol)

if __name__ == "__main__":
    source = open_file()
    analyze(source)
        

