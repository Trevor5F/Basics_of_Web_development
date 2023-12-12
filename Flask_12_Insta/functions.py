import json

def list_posts():
    with open('posts.json', encoding='utf-8') as file:
        return json.load(file)


def add_posts(new_post):
    with open('posts.json', 'w', encoding='utf-8') as file:
        json.dump(new_post, file, ensure_ascii=False, indent=4)

