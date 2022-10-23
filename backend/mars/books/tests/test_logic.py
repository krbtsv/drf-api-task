from django.contrib.auth.models import User
from django.test import TestCase

from books.logic import set_rating
from books.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='Max', last_name='Karabtsov')
        user2 = User.objects.create(username='user2', first_name='Bugs', last_name='Banny')
        user3 = User.objects.create(username='user3', first_name='0', last_name='1')

        self.book_1 = Book.objects.create(title='test book 1', price=10, author_name='author 1', creator=user1)

        UserBookRelation.objects.create(user=user1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=self.book_1, like=True, rate=5)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))
