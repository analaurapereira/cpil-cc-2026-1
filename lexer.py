# Código fonte em "calculator language" para análise léxica

from os import POSIX_FADV_NOREUSE
source = """
read a
read b
read c

result := (a + b) * c
write result
"""

# Caracteres considerados "em branco"
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
    lexeme = " "
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
        pass

    def display_error(ch: str) -> None:
        pass

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

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1002)

                else:
                    display_error(ch)

            case 20:
                if ch == "a":
                    lexeme, state = go_to_state(ch, 30)
                
                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 100)

                else:
                    display_error(ch)

            case 30:
                if ch == "d":
                    lexeme, state = go_to_state(ch, 40)
                
                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1001)

                else:
                    display_error(ch)

            case 40:
                if is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)
                
                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1002)
                
                else:
                    display_error(ch)


            case 50:
                if is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1001)

                else:
                    display_error(ch)

            case 60:  
                if ch == "r":
                    lexeme, state = go_to_state(ch, 70)

                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1001)

                else:
                    display_error(ch)

            case 70:
                if ch == "i":
                    lexeme, state = go_to_state(ch, 80)

                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1001)

                else:
                    display_error(ch)

            case 80: 
                if ch == "t":
                    lexeme, state = go_to_state(ch, 90)

                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1001)

                else:
                    display_error(ch)

            case 90:  
                if ch == "e":
                    lexeme, state = go_to_state(ch, 100)

                elif is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1001)

                else:
                    display_error(ch)

            case 100: 
                if is_alphanum(ch):
                    lexeme, state = go_to_state(ch, 50)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1003)

                else:
                    display_error(ch)

            case 110: 
                if is_digit(ch):
                    lexeme, state = go_to_state(ch, 110)

                elif ch == ".":
                    lexeme, state = go_to_state(ch, 120)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1004)

                else:
                    display_error(ch)

            case 120:  
                if is_digit(ch):
                    lexeme, state = go_to_state(ch, 120)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1004)

                else:
                    display_error(ch)

            case 130:  
                if is_digit(ch):
                    lexeme, state = go_to_state(ch, 140)

                else:
                    display_error(ch)

            case 140:  
                if is_digit(ch):
                    lexeme, state = go_to_state(ch, 140)

                elif ch in BLANKS:
                    lexeme, state = accept(ch, 1004)

                else:
                    display_error(ch)

            case 150:  
                if ch == "=":
                    lexeme, state = accept(ch, 1005)

                else:
                    display_error(ch)
