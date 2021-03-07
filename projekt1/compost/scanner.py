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
        print(input)
        for token in self.tokenize(input):
            self.tokens.append(token)
 
    def tokenize(self, input_string):
        keywords = {
            'version', 'services',
            'build', 'ports', 'image', 'volumes',
            'environment', 'networks', 'deploy',
            # 'mode', 'replicas', '', 'volumes', 
            # , 'update_config', 'parallelism', 'restart_policy',
            # 'condition', 'placement', 'max_replicas_per_node', 'constraints',
            # 'labels', 'max_attempts', 'window'
        }  # TODO image regex, ports regex, delay regex, string regex
        token_specification = [
            ('NUMBER',  r'\d+(\.\d*)?(?=[ \n])'),    # Integer or decimal number
            ('ASSIGN',  r':(?=[\n ]?)'),
            ('HYPHEN',  r'-'),              # Statement terminator
            ('ID',      r'[A-Z_a-z-]+(?=[ :][ \n])'),      # Identifiers
            # ('EMPTY_LINE', r'^\s*$'),
            ('WHITESPACE',  r'\n[ ]*(?!=\n)'),  # Double space indent
            
            # ('WHITESPACE',  r'(?<=\n)[ ]*(?!=\n)'),
            # ('OP',      r'[+*\/\-]'),       # Arithmetic operators
            # ('NEWLINE', r'\n'),             # Line endings
            ('STRING', r'"?[A-Za-z0-9:_=./-]+"?(?!:)'),
            ('SKIP',  r'[ \t]'),
            # ('SPACE', r' ')
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
            if type == 'NEWLINE':
                line_start = current_position
                line_number += 1
            # elif type != 'SKIP' and type != 'EMPTY_LINE':
            elif type != 'SKIP':    
                value = match.group(type)
                if type == 'ID' and value in keywords:
                    type = value
                yield Token(type, value, line_number, match.start()-line_start)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError(
                'Error: Unexpected character %r on line %d' %
                (input_string[current_position], line_number)
            )
        yield Token('EOF', '', line_number, current_position-line_start)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number-1 < len(self.tokens):
            return self.tokens[self.current_token_number-1]
        else:
            return None
