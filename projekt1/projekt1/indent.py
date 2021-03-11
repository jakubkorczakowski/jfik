import copy


class IndentLexer(object):
    def __init__(self, lexer):
        self.indents = [0]  
        self.tokens = []    
        self.lexer = lexer

    def input(self, *args, **kwds):
        self.lexer.input(*args, **kwds)

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next

    def token(self):
        if self.tokens:
            return self.tokens.pop(0)

        while 1:
            token = self.lexer.next_token()

            if not token or token.type != 'WHITESPACE':
                return token

            whitespace = token.value[1:] 
            change = self._calc_indent(whitespace)
            if change:
                break

        if change == 1:
            token = token._replace(type='INDENT')
            return token

        assert change < 0
        change += 1
        token = token._replace(type='DEDENT')

        while change:
            self.tokens.append(copy.copy(token))
            change += 1

        return token

    def _calc_indent(self, whitespace):
        "returns a number representing indents added or removed"
        n = len(whitespace)
        indents = self.indents
        if n > indents[-1]:
            indents.append(n)
            return 1

        if n == indents[-1]:
            return 0

        i = 0
        while n < indents[-1]:
            indents.pop()
            if n > indents[-1]:
                raise SyntaxError("wrong indentation level")
            i -= 1
        return i
