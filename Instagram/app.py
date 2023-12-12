import logging
import os

from flask import render_template, Flask, request, json, redirect
from utils import get_posts_all, get_post_by_pk, get_comments_by_post_id, search_for_posts, \
    get_posts_by_user, get_posts_by_tegs, add_bookmark, get_bookmarks, del_bookmark


logging.basicConfig(encoding='utf-8', filename="logs/api.log", level=logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

app = Flask(__name__)


@app.route('/')
def posts_list():
    return render_template('index.html', posts=get_posts_all().values(), len_bookmarks=len(get_bookmarks().values()))

@app.route('/bookmarks')
def bookmarks_list():
    return render_template('bookmarks.html', bookmarks=get_bookmarks().values())

@app.route('/post/<int:pk>')
def user_post(pk):
    comments = get_comments_by_post_id(pk)
    len_coments = len(comments)
    return render_template('post.html', comments=comments, len_coments=len_coments, post=get_post_by_pk(pk))

@app.route('/search/')
def search_posts():
    search_by = request.args.get('s')
    if not search_by:
        return '<h1>Пустой запрос<h1>'
    return render_template('search.html', querys=search_for_posts(search_by))

@app.route('/users/<username>/')
def username(username):
    return render_template('user-feed.html', names=get_posts_by_user(username))

@app.route('/tag/<tagname>')
def tag(tagname):
    return render_template('tag.html', tags=get_posts_by_tegs(tagname), tagname=tagname)


@app.route('/bookmarks/add/<int:postid>', methods=['POST'])
def add_in_bookmarks(postid):
    if postid in get_bookmarks():
        return '<h1>Уже добавлено<h1>'
    else:
        add_bookmark(get_posts_all()[postid])
    return redirect("/", code=302)

@app.route('/bookmarks/remove/<int:postid>', methods=['POST'])
def del_in_bookmarks(postid):
    if postid:
        del_bookmark(postid)
    else:
        return '<h1>Нет пользователя с таким ID<h1>'
    return redirect("/bookmarks", code=302)


#==========================================================
'''Обработка ошибок'''

@app.errorhandler(404)
def page_not_found(error):
    return '<h1>Нет такой страницы<h1>', 404

@app.errorhandler(500)
def internal_server_error(error):
    return '<h1>Ошибка со стороны сервера<h1>', 500
#==========================================================

''' Залогируйте обращения к эндпоинтам API
Используйте стандартный logging, логи должны храниться в папке logs в файле `api.log`.
Формат логов должен быть таким: %(asctime)s [%(levelname)s] %(message)s '''

# Создаем логгер с именем "api"
logger = logging.getLogger("api")
logger.setLevel(logging.INFO)

# Создаем обработчик для записи логов в файл
if not os.path.exists("logs"):
    os.makedirs("logs")
handler = logging.FileHandler("logs/api.log")
handler.setLevel(logging.INFO)

# Создаем форматтер для сообщений логов
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

# Добавляем обработчик к логгеру
logger.addHandler(handler)


@app.route('/api/posts')
def posts():
    logger.info("Запрос /api/posts")
    data = json.dumps(get_posts_all(), ensure_ascii=False, indent=4)
    return f'<pre>{data}</pre>' # данные отображаются в столбик в браузере

@app.route('/api/posts/<int:pk>')
def posts_id(pk):
    logger.info(f"Запрос /api/posts/{pk}")
    data = json.dumps(get_post_by_pk(pk), ensure_ascii=False, indent=4)
    return f'<pre>{data}</pre>'

app.run(debug=False)
