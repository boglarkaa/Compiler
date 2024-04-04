from lex import *


def main():
    source = "LET foobar = 123"
    lexer = Lexer(source)

    while lexer.peek() != "\0":
        print(lexer.current_character)
        lexer.next_character()


main()
