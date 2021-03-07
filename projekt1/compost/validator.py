# Simple example of parsing
# Bartosz Sawicki, 2014-03-13

from scanner import Scanner
from parser import Parser
from indent import IndentLexer

# input_string = '''
# x := 5;
# y := x;
# PRINT 64;
# '''

input_string = '''
version: "3.9"

services:
  wordpress:
    image: wordpress
    build: .
    ports:
      - "8080:80"
    networks:
      - overlay
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_PASSWORD=postgres
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip

  mysql:
    image: mysql
    volumes:
       - db-data:/var/lib/mysql/data
    networks:
       - overlay
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: dnsrr
      placement:
        constraints:
          - "node.role==manager"

volumes:
  db-data:

networks:
  overlay:
  backend:

'''

# print(input_string)
scanner = Scanner(input_string)
# for token in scanner.tokens:
#     print(token)

indent_lexer = IndentLexer(scanner)

# for token in indent_lexer:
#     print(token)


# print(next(indent_lexer))

parser = Parser(indent_lexer)
parser.start()

