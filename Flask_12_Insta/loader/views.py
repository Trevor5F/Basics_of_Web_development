import logging
from json import JSONDecodeError
from flask import render_template, Blueprint, request
from ..functions import list_posts, add_posts

loader_blueprint = Blueprint('loader_blueprint',__name__, url_prefix='/post', template_folder='templates')

@loader_blueprint.route('/form')
def post_page():
    return render_template("post_form.html")

# создаем объект логгера
search_logger = logging.getLogger('search_logger')
search_logger.setLevel(logging.INFO)

# создаем обработчик для записи логов в файл
file_handler = logging.FileHandler('search.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s - %(request)s'))


@loader_blueprint.route('/upload', methods=['POST'])
def add_post():
    try:
        pic = request.files.get("picture")
        # Сохранить информацию о запросе в переменной request_data
        request_data = f"{request.method} {request.path} {request.environ['SERVER_PROTOCOL']}"
        if not pic:
            search_logger.error(f'Oшибка загрузки {request_data}')
            return '<h1>Oшибка загрузки<h1>'
        else:
            filename = pic.filename
            pic.save(f"uploads/images/{filename}")

            content = request.values['content']

            new_post = {
                'pic': f'uploads/images/{filename}',
                'content': content
            }
            posts = list_posts()
            posts.append(new_post)
            add_posts(posts)
            if filename.split(".")[-1] not in ['png', 'jpeg', 'jpg']:
                search_logger.error('Загруженный файл - не картинка')
                return '<h1>Загруженный файл - не картинка<h1>'

        return render_template("post_uploaded.html", pic=f'/uploads/images/{filename}', content=content)

    except FileNotFoundError:
        search_logger.error('Файл "posts.json" отсутствует')
        return '<h1>Файл "posts.json" отсутствует<h1>'
    except JSONDecodeError:
        search_logger.error("Файл не удается преобразовать")
        return '<h1>Файл не удается преобразовать<h1>'

