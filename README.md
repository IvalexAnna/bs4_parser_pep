##Проект парсинга pep

[](https://github.com/4its/bs4_parser_pep/blob/master/README.md#%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82-%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3%D0%B0-pep)

Простой парсер, предназначенный для получения информации с сайта [https://python.org](https://python.org/). В частности:

- предоставить ссылки на страницы изменений в разных версиях Python;
- предоставить ссылки на документации по версиям Python;
- загрузить документацию в формате pdf для актуальной версии Python;
- сформировать отчет по документам PEP(_Python Enhancement Proposal_).

## Технологии

[](https://github.com/4its/bs4_parser_pep/blob/master/README.md#%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8)

- [**Python**](https://docs.python.org/3.12/)
- [**requests-cache**](https://pypi.org/project/requests-cache/1.0.0/)
- [**tqdm**](https://pypi.org/project/tqdm/4.66.4/)
- [**beautifulsoup4**](https://pypi.org/project/beautifulsoup4/4.12.3/)
- [**lxml**](https://pypi.org/project/lxml/5.2.2/)
- [**prettytable**](https://pypi.org/project/prettytable/2.1.0/)

## Использование

[](https://github.com/4its/bs4_parser_pep/blob/master/README.md#%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)

### Требования

[](https://github.com/4its/bs4_parser_pep/blob/master/README.md#%D1%82%D1%80%D0%B5%D0%B1%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)

Для запуска проекта, необходим [Python](https://www.python.org/) v3.9+.

### Клонирование проекта

[](https://github.com/4its/bs4_parser_pep/blob/master/README.md#%D0%BA%D0%BB%D0%BE%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0)

Выполните команду для клонирования и перехода в проект:

```shell
git clone https://github.com/4its/bs4_parser_pep.git && cd bs4_parser_pep
```

### Виртуальное окружение

Для создания и активации окружения:

```shell
python -m venv venv %% source venv/bin/activate
```

### Установка зависимостей

Для установки зависимостей, выполните команду:

```shell
pip install -r requirements.txt
```

## Команды

#### Вывод справки

```shell
python src/main.py -h
```

Примеры команд:

- Получение списка ссылок на изменения по версиям Python в файле .csv
    
    ```shell
    python src/main.py whats-new -o file
    ```
    
- Получение списка ссылок на изменения по версиям Python в консоль(PrettyPrint)
    
    ```shell
    python src/main.py whats-new -o pretty
    ```
    
- Получение списка ссылок на изменения по версиям Python в консоль(PrettyPrint) _без использования кеширования_:
    
    ```shell
    python src/main.py whats-new -с -o pretty
    ```
    
- Получение статистики документам PEP c выводом в консоль:
    
    ```shell
    python src/main.py pep
    ```
    
- [**Ivanova Anna**](https://github.com/IvalexAnna)