import collections
import re
import os

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])


class Scanner:

    def __init__(self, input):
        self.tokens = []
        self.current_token_number = 0
        input = os.linesep.join([s for s in input.splitlines() if s])
        input += '\n'
        for token in self.tokenize(input):
            self.tokens.append(token)
 
    def tokenize(self, input_string):
        token_specification = [
            ('VERSION',     r'version'),
            ('SERVICES',    r'services'),
            ('BUILD',       r'build'),
            ('PORTS',       r'ports'),
            ('IMAGE',       r'image'),
            ('VOLUMES',     r'volumes'),
            ('ENVIRONMENT', r'environment'),
            ('NETWORKS',    r'networks'),
            ('DEPLOY',      r'deploy'),
            ('NUMBER',      r'\d+(\.\d*)?(?=[ \n])'),       # Integer or decimal number
            ('ASSIGN',      r':(?=[\n ]?)'),
            ('HYPHEN',      r'-'),                          # Statement terminator
            ('ID',          r'[A-Z_a-z-]+(?=[ :][ \n])'),   # Identifiers
            ('WHITESPACE',  r'\n[ ]*(?!=\n)'),          # Double space indent
            ('STRING',      r'"?[A-Za-z0-9:_=./-]+"?(?!:)'),
            ('SKIP',        r'[ \t]'),
        ]
        tok_regex = '|'.join(
            '(?P<%s>%s)' % pair for pair in token_specification
        )
        get_token = re.compile(tok_regex).match
        line_number = 1
        current_position = line_start = 0
        match = get_token(input_string)
        while match is not None:
            type = match.lastgroup
            if type == 'WHITESPACE':
                line_start = current_position
                line_number += 1
                value = match.group(type)
                yield Token(type, value, line_number, match.start()-line_start)
            elif type != 'SKIP':    
                value = match.group(type)
                yield Token(type, value, line_number, match.start()-line_start)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError(
                'Error: Unexpected character ' +
                f'{input_string[current_position]} on line {line_number}'
            )
        yield Token('EOF', '', line_number, current_position-line_start)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number-1 < len(self.tokens):
            return self.tokens[self.current_token_number-1]
        else:
            return None
