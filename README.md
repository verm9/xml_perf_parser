
1. ТЗ использует оптимизацию с C extension для парсинга xml данных. Чтобы установить её, запустите из директории с проектом:  
\# python setup.py install  
  , чтобы установить parsermodule. Для установки понадобится Visual C++ компилятор (на windows). Больше информации здесь: https://wiki.python.org/moin/WindowsCompilers.  
Для отключения этой оптимизации установите значение по-умолчанию optimization = False ( def process_xml_data(content: bytes, optimization: bool = False) -> (Level, List[Object]) ):
2. При выполнении ТЗ учитывалось, что важна именно структура xml, а не его "pretty output" (отступы, пробелы в некоторых местах).
3. Для запуска проекта не требуются не стандартные python библиотеки. Однако если хотите xml c красивым выводом и запустить тесты, то:  
$ pip install -r requirements.txt
4. Для запуска теста:  
$ pytest  
  из директории с проектом
