TOP_LEVEL_STATEMENTS = ['SERVICES', 'VOLUMES', 'NETWORKS']
STATEMENTS = [
    'BUILD', 'PORTS', 'IMAGE', 'VOLUMES', 'ENVIRONMENT', 'NETWORKS',
    'DEPLOY', 'ID'
]
VALUES = ['NUMBER', 'STRING']


class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.token = next(self.scanner)

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error(
                f"Unexpected token: got {token_type}, " +
                f"expected {self.token.type}" +
                f" in line {self.token.line}" +
                f" in column {self.token.column}"
            )
        if token_type != 'EOF':
            self.token = next(self.scanner)

    def error(self, msg):
        print(self.token)
        raise RuntimeError(f'Parser error, {msg}')

    # Starting symbol
    def start(self):
        # start -> version_stmt program EOF
        if self.token.type == 'VERSION':
            self.version_stmt()
            self.program()
            self.take_token('EOF')
        else:
            self.error("Epsilon not allowed")

    def program(self):
        # program -> statement program
        if self.token.type in TOP_LEVEL_STATEMENTS:
            self.statement()
            self.program()
        # program -> eps
        else:
            pass

    def statement(self):
        # statement -> assign_stmt elements
        self.assign_stmt()
        if self.token.type == 'INDENT':
            self.take_token('INDENT')
            self.elements()
            self.take_token('DEDENT')
            print("statement OK")
        else:
            print("statement OK")

    # version_stmt -> VERSION ASSIGN STRING
    def version_stmt(self):
        if self.token.type == 'VERSION':
            self.take_token('VERSION')
            self.take_token('ASSIGN')
            self.take_token('STRING')
            print("version_stmt OK")
        else:
            self.error("Epsilon not allowed")

    def elements(self):
        # elements -> elements assign_stmt element
        if self.token.type in STATEMENTS \
                or self.token.type in VALUES \
                or self.token.type == 'INDENT':
            self.assign_stmt()
            self.element()
            self.elements()
            print("elements OK")
        else:
            print("elements OK")

    def element(self):
        # element -> value
        if self.token.type in ['NUMBER', 'STRING']:
            self.value()
            print("element OK")
        elif self.token.type == 'INDENT':
            self.take_token('INDENT')
            # element -> INDENT value DEDENT
            if self.token.type in ['NUMBER', 'STRING']:
                self.value()
                self.take_token('DEDENT')
                print("element OK")
            # element -> INDENT hyphen_list DEDENT
            if self.token.type == 'HYPHEN':
                self.hyphen_list()
                self.take_token('DEDENT')
                print("element OK")
            # element -> INDENT elements DEDENT
            else:
                self.elements()
                self.take_token('DEDENT')
                print("element OK")
        # element -> eps    
        else:
            print("element OK")

    def hyphen_list(self):
        # hyphen_list -> hyphen_list hyphen_element
        if self.token.type == 'HYPHEN':
            self.hyphen_element()
            self.hyphen_list()
            print("hyphen_list OK")
        else:
            print("hyphen_list OK")

    def hyphen_element(self):
        # hyphen_element -> HYPHEN value
        if self.token.type == 'HYPHEN':
            self.take_token('HYPHEN')
            self.value()
            print("hyphen_element OK")
        else:
            print("hyphen_element OK")

    def assign_stmt(self):
        # assign_stmt -> ID ASSIGN value
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('ASSIGN')
            print("ID OK")
        # assign_stmt -> services ASSIGN value
        elif self.token.type == 'SERVICES':
            self.take_token('SERVICES')
            self.take_token('ASSIGN')
            print("services OK")
        # assign_stmt -> volumes ASSIGN value
        elif self.token.type == 'VOLUMES':
            self.take_token('VOLUMES')
            self.take_token('ASSIGN')
            print("volumes OK")
        # assign_stmt -> build ASSIGN value
        elif self.token.type == 'BUILD':
            self.take_token('BUILD')
            self.take_token('ASSIGN')
            print("build OK")
        # assign_stmt -> ports ASSIGN value
        elif self.token.type == 'PORTS':
            self.take_token('PORTS')
            self.take_token('ASSIGN')
            print("ports OK")
        # assign_stmt -> image ASSIGN value
        elif self.token.type == 'IMAGE':
            self.take_token('IMAGE')
            self.take_token('ASSIGN')
            print("image OK")
        # assign_stmt -> environment ASSIGN value
        elif self.token.type == 'ENVIRONMENT':
            self.take_token('ENVIRONMENT')
            self.take_token('ASSIGN')
            print("environment OK")
        # assign_stmt -> networks ASSIGN value
        elif self.token.type == 'NETWORKS':
            self.take_token('NETWORKS')
            self.take_token('ASSIGN')
            print("networks OK")
        # assign_stmt -> deploy ASSIGN value
        elif self.token.type == 'DEPLOY':
            self.take_token('DEPLOY')
            self.take_token('ASSIGN')
            print("deploy OK")
        else:
            self.error("Epsilon not allowed")

    def value(self):
        # value -> NUMBER
        if self.token.type == 'NUMBER':
            self.take_token('NUMBER')
        # value -> STRING
        elif self.token.type == 'STRING':
            self.take_token('STRING')
        else:
            self.error("Epsilon not allowed")
