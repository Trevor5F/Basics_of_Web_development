import logging
from json import JSONDecodeError
from flask import render_template, Blueprint, request
from ..functions import list_posts

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


@main_blueprint.route('/')
def index_page():
    return render_template("index.html")


# создаем объект логгера
search_logger = logging.getLogger('search_logger')
search_logger.setLevel(logging.INFO)

# создаем обработчик для записи логов в файл
file_handler = logging.FileHandler('search.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

# добавляем обработчик в логгер
search_logger.addHandler(file_handler)


@main_blueprint.route('/search')
def search():
    try:
        search_by = request.args.get('i')
        if not search_by:
            return '<h1>Пустой запрос<h1>'

        # записываем сообщение об успешном выполнении поиска
        search_logger.info(f'Поиск по запросу "{search_by}" выполнен успешно')

        posts = [i for i in list_posts() if search_by.lower() in i['content'].lower()]
        return render_template("post_list.html", search_by=search_by, posts=posts)

    except FileNotFoundError:
        # записываем сообщение об ошибке при загрузке файла
        search_logger.error('Файл "posts.json" отсутствует')
        return '<h1>Файл "posts.json" отсутствует<h1>'

    except JSONDecodeError:
        # записываем сообщение об ошибке при преобразовании файла
        search_logger.error("Файл не удается преобразовать")
        return '<h1>Файл не удается преобразовать<h1>'
