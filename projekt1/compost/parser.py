TOP_LEVEL_STATEMENTS = ['services', 'volumes', 'networks']
STATEMENTS = [
    'build', 'ports', 'image', 'volumes', 'environment', 'networks',
    'deploy', 'ID'
]

VALUES = ['NUMBER', 'STRING']

# TODO my_list, dwie wartości w backend newline - poprawić


class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.token = next(self.scanner)

    def take_token(self, token_type):
        if self.token.type != token_type:
            print(self.token)
            print(next(self.scanner))
            self.error("Unexpected token: %s" % self.token.type)
        if token_type != 'EOF':
            self.token = next(self.scanner)

    def error(self, msg):
        print(self.token)
        print(next(self.scanner))
        raise RuntimeError('Parser error, %s' % msg)

    # Starting symbol
    def start(self):
        # start -> version_stmt program EOF
        if self.token.type == 'version':
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
        # statement -> services_stmt
        if self.token.type == 'services':
            self.services_stmt()
        # statement -> volumes_stmt
        elif self.token.type == 'volumes':
            self.volumes_stmt()
        # statement -> networks_stmt
        elif self.token.type == 'networks':
            self.networks_stmt()
        else:
            self.error("Epsilon not allowed")

    # version_stmt -> version ASSIGN STRING
    def version_stmt(self):
        if self.token.type == 'version':
            self.take_token('version')
            self.take_token('ASSIGN')
            self.take_token('STRING')
            print("version_stmt OK")
        else:
            self.error("Epsilon not allowed")

    def services_stmt(self):
        # services_stmt -> services ASSIGN  my_list
        self.take_token('services')
        self.take_token('ASSIGN')
        if self.token.type == 'INDENT':
            self.take_token('INDENT')
            self.my_list()
            self.take_token('DEDENT')
            print("services_stmt OK")
        # services_stmt -> services ASSIGN
        else:
            print("services_stmt OK")

    def my_list(self):
        # my_list -> INDENT my_list assign_stmt INDENT elements DEDENT DEDENT  
        if self.token.type in STATEMENTS:
            self.assign_stmt()
            if self.token.type == 'INDENT':
                self.take_token('INDENT')
                self.elements()
                self.take_token('DEDENT')
            self.my_list()
            print("my_list OK")
        # my_list -> eps
        else:
            print("my_list OK")

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
        else:
            self.error("element not OK")

    def hyphen_list(self):
        # hyphen_list -> hyphen_list hyphen_element
        if self.token.type == 'HYPHEN':
            self.hyphen_element()
            self.hyphen_list()
            print("hyphen_list OK")
        else:
            print("hyphen_list OK")

    def hyphen_element(self):
        # hyphen_list -> hyphen_list hyphen_element
        if self.token.type == 'HYPHEN':
            self.take_token('HYPHEN')
            self.value()
            print("hyphen_element OK")
        else:
            print("hyphen_element OK")

    def assign_stmt(self):
        # assign_stmt -> ID ASSIGN value END
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('ASSIGN')
            print("ID OK")
        # assign_stmt -> volumes ASSIGN value END
        elif self.token.type == 'volumes':
            self.take_token('volumes')
            self.take_token('ASSIGN')
            print("volumes OK")
        # assign_stmt -> build ASSIGN value END
        elif self.token.type == 'build':
            self.take_token('build')
            self.take_token('ASSIGN')
            print("build OK")
        # assign_stmt -> ports ASSIGN value END
        elif self.token.type == 'ports':
            self.take_token('ports')
            self.take_token('ASSIGN')
            print("ports OK")
        # assign_stmt -> image ASSIGN value END
        elif self.token.type == 'image':
            self.take_token('image')
            self.take_token('ASSIGN')
            print("image OK")
        # assign_stmt -> environment ASSIGN value END
        elif self.token.type == 'environment':
            self.take_token('environment')
            self.take_token('ASSIGN')
            print("environment OK")
        # assign_stmt -> networks ASSIGN value END
        elif self.token.type == 'networks':
            self.take_token('networks')
            self.take_token('ASSIGN')
            print("networks OK")
        # assign_stmt -> deploy ASSIGN value END
        elif self.token.type == 'deploy':
            self.take_token('deploy')
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

    def volumes_stmt(self):
        # volumes_stmt -> volumes ASSIGN  my_list
        self.take_token('volumes')
        self.take_token('ASSIGN')
        if self.token.type == 'INDENT':
            self.take_token('INDENT')
            self.my_list()
            self.take_token('DEDENT')
            print("volumes_stmt OK")
        # volumes_stmt -> volumes ASSIGN
        else:
            print("volumes_stmt OK")

    def networks_stmt(self):
        # networks_stmt -> networks ASSIGN my_list
        self.take_token('networks')
        self.take_token('ASSIGN')
        if self.token.type == 'INDENT':
            self.take_token('INDENT')
            self.my_list()
            self.take_token('DEDENT')
            print("networks_stmt OK")
        # networks_stmt -> networks ASSIGN
        else:
            print("networks_stmt OK")
