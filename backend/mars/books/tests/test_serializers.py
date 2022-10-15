from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django.test import TestCase

from books.models import Book, UserBookRelation
from books.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')

        book_1 = Book.objects.create(title='test book 1', price=10, author_name='author 1')
        book_2 = Book.objects.create(title='test book 2', price=15, author_name='author 2')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'title': 'test book 1',
                'price': '10.00',
                'author_name': 'author 1',
                'likes_count': 3,
                'annotated_likes': 3,
            },
            {
                'id': book_2.id,
                'title': 'test book 2',
                'price': '15.00',
                'author_name': 'author 2',
                'likes_count': 2,
                'annotated_likes': 2
            },
        ]
        self.assertEqual(expected_data, data)
