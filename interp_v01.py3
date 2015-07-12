"""
July 11, 2015
-------------

Following http://ruslanspivak.com/lsbasi-part1/, this is the first step in a
simple Pascal interpretor. I'm going to make modest changes as we go, which
will probably end up bitting me in the ass if Ruslan goes in a different direction
than I do.

See Also:
    Beazley's Recursive-Descent Parser from the Python Cookbook.
"""

import operator


# ToDO: move TokenTypes into Token
class TokenTypes(object):
    Integer = 'INTEGER'
    Plus = 'PLUS'
    Operator = 'OPERATOR'
    Eof = 'EOF'
    Whitespace = 'WHITESPACE'


class Token(object):
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        """ String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(type=self.token_type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class InterpreterError(Exception):
    pass


class Interpreter(object):
    def __init__(self, text):
        """ Initialize with a text string, eg, '3+5'. """
        self.text = text
        self._text_index = 0
        self.current_token = None

    def error(self):
        raise InterpreterError('Error parsing input')

    def get_next_token(self):
        """ The Lexer. This method is responsible for breaking a sentence
        apart into tokens, one token at a time. """
        text = self.text
        if self.at_text_end():
            return Token(TokenTypes.Eof, None)

        current_char = text[self._text_index]

        if current_char.isdigit():
            return self.get_int_token()

        elif current_char == '+':
            token = Token(TokenTypes.Operator, operator.add)
            self._text_index += 1
            return token

        elif current_char == ' ':
            self._text_index += 1
            return self.get_next_token()

        elif current_char == '-':
            token = Token(TokenTypes.Operator, operator.sub)
            self._text_index += 1
            return token

        else:
            self.error()

    def has_text_left(self):
        return self._text_index < len(self.text) - 1

    def at_text_end(self):
        return self._text_index > len(self.text) - 1

    def get_int_token(self):
        '''
        - we are here because the current index points at an int. The next char
        is either: an int, an op, or EOF.
        If the next char is an int, append it to the current int, otherwise return
        an IntToken.
        '''
        # import pdb; pdb.set_trace()
        int_string = self.text[self._text_index]
        while self.has_text_left():
            self._text_index += 1
            next_char = self.text[self._text_index]
            if next_char.isdigit():
                int_string += next_char
            else:
                break
        return Token(TokenTypes.Integer, int(int_string))

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        print('EAT: current token: %s expected: %s' % (self.current_token, token_type))
        if self.current_token.token_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """
        expr -> INTEGER PLUS INTEGER.

        We are going to be parsing tokens with the expected pattern of Left-Number,
        Operator, Right-Number.
        """
        self.current_token = self.get_next_token()
        print('expr: %s' % self.current_token)

        left = self.current_token
        self.eat(TokenTypes.Integer)

        if self.current_token.token_type == TokenTypes.Operator:
            operation = self.current_token.value
            self.eat(TokenTypes.Operator)

        right = self.current_token
        self.eat(TokenTypes.Integer)
        result = operation(left.value, right.value)
        return result


def main():
    while True:
        # import pdb; pdb.set_trace()
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
            interpreter = Interpreter(text)
            result = interpreter.expr()
            print(result)
        except InterpreterError:
            print("Parsing error!")
            continue


if __name__ == '__main__':
    main()
