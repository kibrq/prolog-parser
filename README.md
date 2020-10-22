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

# project
В папке project лежит парсер способный дополнительно распознавать кастомные операторы, вложенные комментарии и soft-keywords.

Синтаксис для операторов

`operator [operator_name] [operator_prior] [operator_assoc] (:- EXPR . | .)`

- operator_name состоит из небукв, типа -+;,>< и тд
- operator_prior число от 0 до 9
- operator_assoc либо 'L' либо 'R'
