from django.test import TestCase

from books.models import Book
from books.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(title='test book 1', price=10)
        book_2 = Book.objects.create(title='test book 2', price=15)
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'title': 'test book 1',
                'price': '10.00'
            },
            {
                'id': book_2.id,
                'title': 'test book 2',
                'price': '15.00'
            },
        ]
        self.assertEqual(expected_data, data)