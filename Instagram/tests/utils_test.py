import unittest

from ..utils import get_post_by_pk, get_posts_by_user, get_comments_by_post_id, search_for_posts, get_posts_all

class TestFunctions(unittest.TestCase):

    def test_get_posts_all(self):
        posts = get_posts_all()
        self.assertIsInstance(posts, dict)
        self.assertGreater(len(posts), 0)

    def test_get_post_by_pk(self):
        posts = get_posts_all()
        post = get_post_by_pk(1)
        self.assertIsInstance(post, dict)
        self.assertEqual(post, posts[1])
        self.assertIsNone(get_post_by_pk(100))

    def test_get_posts_by_user(self):
        user_posts = get_posts_by_user('leo')
        self.assertIsInstance(user_posts, list)
        self.assertGreater(len(user_posts), 0)
        for post in user_posts:
            self.assertEqual(post['poster_name'].lower(), 'leo')

    def test_get_comments_by_post_id(self):
        comments = get_comments_by_post_id(1)
        self.assertIsInstance(comments, list)
        self.assertGreater(len(comments), 0)
        for comment in comments:
            self.assertEqual(comment['post_id'], 1)

    def test_search_for_posts(self):
        query = 'еда'
        result = search_for_posts(query)
        self.assertIsInstance(result, dict)
        self.assertIn(query.lower(), result['content'].lower())

if __name__ == '__main__':
    unittest.main()
