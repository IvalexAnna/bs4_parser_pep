from pathlib import Path

MAIN_DOC_URL = "https://docs.python.org/3/"
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
MAIN_PEP_URL = "https://peps.python.org/"

TQDM_NCOLS: int = 100


class Logs:
    DIRECTORY = BASE_DIR / "logs"
    FILENAME = "parser.log"
    FILE_PATH = DIRECTORY / FILENAME


class Texts:
    START_PARSE = "Парсер запущен!"
    FINISH_PARSE = "Парсер завершил работу."
    COMMAND_ARGS = "Аргументы командной строки: {}"
    FILE_RESULT = "Файл с результатами был сохранён: {}"
    TAG_NOT_FOUND = "Не найден тег {} {}"
    RESPONSE_ERROR = "Ошибка при загрузке страницы {}. Подробности: {}"
    PARSER_DESCRIPTION = "Парсер документации Python"
    PARSER_MODE = "Режимы работы парсера"
    PARSER_CACHE_CLEAN = "Очистка кеша"
    PARSER_OUTPUTS = "Дополнительные способы вывода данных"
    STATUS_NOT_MATCH = (
        "Несовпадающие статусы: {} Статус в карточке: {} Ожидаемые статусы: {}"
    )
    TQDM_DESCRIPTION = "Парсим список PEP"
    LOAD_ARCHIVE = "Архив был загружен и сохранён: {}"
    ERROR_WHEN_RUN = "Возникла ошибка при работе программы: {}"
    NOTHING_FOUND = "Ничего не нашлось"
    MAXBYTES: int = 10**6
    BACKUPCONT: int = 5


EXPECTED_STATUS = {
    "A": ("Active", "Accepted"),
    "D": ("Deferred",),
    "F": ("Final",),
    "P": ("Provisional",),
    "R": ("Rejected",),
    "S": ("Superseded",),
    "W": ("Withdrawn",),
    "": ("Draft", "Active"),
}
