import re
import logging
from urllib.parse import urljoin
from collections import defaultdict
import requests_cache

from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    Dirs,
    EXPECTED_STATUS,
    MAIN_DOC_URL,
    MAIN_PEP_URL,
    Texts,
    TQDM_NCOLS,
    Urls,
)
from outputs import control_output
from utils import get_response, find_tag, get_soup


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    response = get_response(session, whats_new_url)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features="lxml")
    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})
    sections_by_python = div_with_ul.find_all("li", attrs={"class": "toctree-l1"})
    results = [("Ссылка на статью", "Заголовок", "Редактор, автор")]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find("a")
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features="lxml")
        h1 = find_tag(soup, "h1")
        dl = find_tag(soup, "dl")
        dl_text = dl.text.replace("\n", " ")
        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")
    sidebar = soup.find("div", {"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")
    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise Exception("Ничего не нашлось")

    results = [("Ссылка на документацию", "Версия", "Статус")]
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"

    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ""
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")
    find_tag(soup, "div", {"role": "main"})
    find_tag(soup, "table", {"class": "docutils"})
    pdf_a4_tag = find_tag(soup, "a", {"href": re.compile(r".+pdf-a4\.zip$")})
    pdf_a4_link = pdf_a4_tag["href"]
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split("/")[-1]
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")

    with open(archive_path, "wb") as file:
        file.write(response.content)


def pep(session):
    soup = get_soup(session, MAIN_PEP_URL)
    section_table = find_tag(soup, "section", {"id": "numerical-index"})
    tbody = find_tag(section_table, "tbody")
    pep_list = tbody.find_all("tr")
    status_sums = defaultdict(int)
    errors = []
    warnings = []
    for pep in tqdm(pep_list, desc=Texts.TQDM_DESCRIPTION, ncols=TQDM_NCOLS):
        status_preview = pep.find("abbr").text
        status_preview = status_preview[1:] if len(status_preview) > 1 else ""
        pep_link = urljoin(MAIN_PEP_URL, pep.find("a")["href"])
        try:
            table = find_tag(
                get_soup(session, pep_link),
                "dl",
                {"class": "rfc2822 field-list simple"},
            )
            status_page = (
                table.find(string="Status").parent.find_next_sibling("dd").string
            )
            status_sums[status_page] += 1
            if status_page not in EXPECTED_STATUS[status_preview]:
                warnings.append(
                    Texts.STATUS_NOT_MATCH.format(
                        pep_link, status_page, EXPECTED_STATUS[status_preview]
                    )
                )
        except ConnectionError as error:
            errors.append(Texts.RESPONSE_ERROR.format(pep_link, error))
    [*map(logging.error, errors)]
    [*map(logging.warning, warnings)]
    return [
        ("Статус", "Количество"),
        *status_sums.items(),
        ("Всего", sum(status_sums.values())),
    ]


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}
def main():
    # Запускаем функцию с конфигурацией логов.
    configure_logging()
    # Отмечаем в логах момент запуска программы.
    logging.info("Парсер запущен!")

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    # Логируем переданные аргументы командной строки.
    logging.info(f"Аргументы командной строки: {args}")

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    # Логируем завершение работы парсера.
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
