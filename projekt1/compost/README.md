# Prosty walidator plików Docker Compose w formacie YAML

Program na pierwszy projekt z przedmiotu **Języki formalne i kompilatory, Laboratoria**.

Program działa w schemacie:
- skanuje plik wejściowy i przetwarza tekst na tokeny - `scanner.py`,
- sprawdza poziom wcięć w pliku - `indent.py`,
- waliduje składnie pliku wejściowego - `parser.py`.

Plik wejściowy definiowany jest jako `string` w pliku `validator.py`.

Program uruchamiany jest poprzez polecenie:

```
$ python3 validator.py
```

Gramatyka BNF użyta w walidatorze:

```
start -> version_stmt program EOF

program -> statement program
program -> eps

version_stmt -> VERSION ASSIGN STRING

statement -> assign_stmt elements

elements -> elements assign_stmt element
elements -> eps

element -> value
element -> INDENT value DEDENT
element -> INDENT hyphen_list DEDENT
element -> INDENT elements DEDENT
element -> eps

hyphen_list -> hyphen_list hyphen_element

hyphen_element -> HYPHEN value

assign_stmt -> ID ASSIGN value
assign_stmt -> services ASSIGN value
assign_stmt -> volumes ASSIGN value
assign_stmt -> build ASSIGN value
assign_stmt -> ports ASSIGN value
assign_stmt -> image ASSIGN value
assign_stmt -> environment ASSIGN value
assign_stmt -> networks ASSIGN value
assign_stmt -> deploy ASSIGN value

value -> NUMBER
value -> STRING
```