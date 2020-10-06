# primitive_parser
В папке primitive_parser лежит парсер написанный методом рекурсивного спуска
Чтобы проверить файл на корректность

`./main.py filename`

Чтобы прогнать тесты:

`pytest .`

# yacc_parser
В папке yacc_parser лежит парсер сгенерированный yacc.
Чтобы проверить файл на корректность и получить AST 

`./main.py filename [outputfilename]`

Чтобы получить красочное красивое AST)

`./main.py --pretty filename`

Чтобы прогнать тесты 

`pytest .`

