import json
import os
from collections import defaultdict


def get_posts_all():
    with open(os.path.join(os.path.dirname(__file__), 'data/posts.json'), encoding='utf-8') as file:
        data = json.load(file)
        return {i['pk']: i for i in data}


posts = get_posts_all()


def get_bookmarks():
    with open(os.path.join(os.path.dirname(__file__), 'data/bookmarks.json'), encoding='utf-8') as file:
        data = json.load(file)
        return {i['pk']: i for i in data}


def add_bookmark(new_bookmarks):
    with open(os.path.join(os.path.dirname(__file__), 'data/bookmarks.json'), 'r+', encoding='utf-8') as file:
        bookmarks = json.load(file)
        bookmarks.append(new_bookmarks)
        file.seek(0)  # записывает данные в начало файла
        json.dump(bookmarks, file, ensure_ascii=False, indent=4)


def del_bookmark(id):
    bookmarks = get_bookmarks()  # Получить все закладки
    if id in bookmarks:
        bookmarks.pop(id)  # Удалить закладку по id
        with open(os.path.join(os.path.dirname(__file__), 'data/bookmarks.json'), 'w', encoding='utf-8') as file:
            json.dump(list(bookmarks.values()), file, ensure_ascii=False, indent=4)
    else:
        return '<h1>Нет пользователя с таким ID<h1>'


def get_post_by_pk(pk: int) -> dict | None:
    if pk in posts:
        return posts[pk]
    return None


def get_posts_by_user(user_name):
    return [user for user in posts.values() if user_name.lower() in user['poster_name']]


def get_comments_by_post_id(post_id: int):
    with open(os.path.join(os.path.dirname(__file__), 'data/comments.json'), encoding='utf-8') as file:
        comments = json.load(file)
        result = defaultdict(list)
        for comment in comments:
            result[comment['post_id']].append(comment)
        if post_id in result:
            return result[post_id]


def get_posts_by_tegs(user_tegs):
    return [user for user in posts.values() if user_tegs.lower() in user.get('tags', '')]


def search_for_posts(query):
    return [i for i in posts.values() if query.lower() in i['content'].lower()]
