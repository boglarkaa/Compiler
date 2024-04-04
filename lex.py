class Lexer:
    def __init__(self, source):
        self.source = source + '\n'  # source code to lex as a string
        self.current_character = ''
        self.current_position = -1
        self.next_character()

    # Process the next character
    def next_character(self):
        self.current_position += 1
        if self.current_position > len(self.source):
            self.current_position = '\0'  # end of file
        else:
            self.current_character = self.source[self.current_position]

    # Return the lookahead character
    def peek(self):
        if self.current_position + 1 >= len(self.source):
            return "\0"
        return self.source[self.current_position + 1]

    # Invalid token, print error message
    def abort(self, message):
        pass

    # Skip whitespace, except newlines
    def skip_whitespace(self):
        pass

    # Skip comments in the code
    def skip_comment(self):
        pass

    # Return the nest token
    def get_token(self):
        # check the first character of this token to see if we can decide what it is
        # if it is a multiple character operator
        if self.current_character == '+':
            pass
        elif self.current_character == '-':
            pass
        elif self.current_character == '*':
            pass
        elif self.current_character == '/':
            pass
        elif self.current_character == '\n':
            pass
        elif self.current_character == '\0':
            pass
        else:
            # unknown character
            pass
        self.next_character()