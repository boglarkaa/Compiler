import sys
import enum


class Lexer:
    def __init__(self, source):
        self.source = source + '\n'  # source code to lex as a string
        self.current_character = ''
        self.current_position = -1
        self.next_character()

    # Process the next character
    def next_character(self):
        self.current_position += 1
        if self.current_position >= len(self.source):
            self.current_position = '\0'  # end of file
        else:
            self.current_character = self.source[self.current_position]

    # Return the lookahead character
    def peek(self):
        if self.current_position + 1 >= len(self.source):
            return '\0'
        return self.source[self.current_position + 1]

    # Invalid token, print error message
    def abort(self, message):
        sys.exit("Lexing error: " + message)

    # Skip whitespace, except newlines
    def skip_whitespace(self):
        while self.current_character == ' ' or self.current_character == '\t' or self.current_character == '\r':
            self.next_character()

    # Skip comments in the code
    def skip_comment(self):
        if self.current_character == '#':
            while self.current_character != '\n':
                self.next_character()

    # Return the nest token
    def get_token(self):
        self.skip_whitespace()
        self.skip_comment()
        token = None
        # check the first character of this token to see if we can decide what it is
        # if it is a multiple character operator
        if self.current_character == '+':
            token = Token(self.current_character, TokenType.PLUS)
        elif self.current_character == '-':
            token = Token(self.current_character, TokenType.MINUS)
        elif self.current_character == '*':
            token = Token(self.current_character, TokenType.ASTERISK)
        elif self.current_character == '/':
            token = Token(self.current_character, TokenType.SLASH)
        elif self.current_character == '=':
            if self.peek() == '=':
                last_character = self.current_character
                self.next_character()
                token = Token(last_character + self.current_character, TokenType.EQEQ)
            else:
                token = Token(self.current_character, TokenType.EQ)
        elif self.current_character == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                last_character = self.current_character
                self.next_character()
                token = Token(last_character + self.current_character, TokenType.GTEQ)
            else:
                token = Token(self.current_character, TokenType.GT)
        elif self.current_character == '<':
            # Check whether this is token is < or <=
            if self.peek() == '=':
                last_character = self.current_character
                self.next_character()
                token = Token(last_character + self.current_character, TokenType.LTEQ)
            else:
                token = Token(self.current_character, TokenType.LT)
        elif self.current_character == '!':
            if self.peek() == '=':
                last_character = self.current_character
                self.next_character()
                token = Token(last_character + self.current_character, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.current_character == '\n':
            token = Token(self.current_character, TokenType.NEWLINE)
        elif self.current_character == '\0':
            token = Token('', TokenType.EOF)
        elif self.current_character == '\"':
            self.next_character()
            start_position = self.current_position

            while self.current_character != '\"':
                if (self.current_character == '\r' or self.current_character == '\n' or self.current_character == '\t'
                        or self.current_character == '\\' or self.current_character == '%'):
                    self.abort("Illegal character in string")
                self.next_character()
            token_text = self.source[start_position:self.current_position]
            token = Token(token_text, TokenType.STRING)
        elif self.current_character.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            start_position = self.current_position
            while self.peek().isdigit():
                self.next_character()
            if self.peek() == '.':  # Decimal!
                self.next_character()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit():
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.next_character()

            token_text = self.source[start_position: self.current_position + 1]  # Get the substring.
            token = Token(token_text, TokenType.NUMBER)
        elif self.current_character.isalpha():
            start_position = self.current_position
            while self.peek().isalnum():
                self.next_character()
            token_text = self.source[start_position: self.current_position + 1]
            keyword = Token.check_if_keyword(token_text)
            if keyword is None:
                token = Token(token_text, TokenType.IDENT)
            else:
                token = Token(token_text, keyword)
        else:
            # unknown character
            self.abort("Unknown character: " + self.current_character)
        self.next_character()
        return token


class Token:
    def __init__(self, token_text, token_kind):
        self.text = token_text
        self.kind = token_kind

    @staticmethod
    def check_if_keyword(token_text):
        for kind in TokenType:
            if kind.name == token_text and 100 <= kind.value <= 200:
                return kind
        return None


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
