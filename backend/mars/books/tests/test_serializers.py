from django.contrib.auth.models import User
from django.test import TestCase

from books.models import Book
from books.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        self.user = User.objects.create(username='username')
        book_1 = Book.objects.create(title='test book 1', price=10, author_name='author 1', creator=self.user)
        book_2 = Book.objects.create(title='test book 2', price=15, author_name='author 2', creator=self.user)
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'title': 'test book 1',
                'price': '10.00',
                'author_name': 'author 1',
                'creator': 1
            },
            {
                'id': book_2.id,
                'title': 'test book 2',
                'price': '15.00',
                'author_name': 'author 2',
                'creator': 1
            },
        ]
        self.assertEqual(expected_data, data)
