from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from books.models import Book, UserBookRelation
from books.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', first_name='Max', last_name='Karabtsov')
        user2 = User.objects.create(username='user2', first_name='Bugs', last_name='Banny')
        user3 = User.objects.create(username='user3', first_name='0', last_name='1')

        book_1 = Book.objects.create(title='test book 1', price=10, author_name='author 1', creator=user1)
        book_2 = Book.objects.create(title='test book 2', price=15, author_name='author 2')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True, rate=5)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'title': 'test book 1',
                'price': '10.00',
                'author_name': 'author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'creator_name': 'user1',
                'readers': [
                    {
                        'first_name': 'Max',
                        'last_name': 'Karabtsov'
                    },
                    {
                        'first_name': 'Bugs',
                        'last_name': 'Banny'
                    },
                    {
                        'first_name': '0',
                        'last_name': '1'
                    },
                ]
            },
            {
                'id': book_2.id,
                'title': 'test book 2',
                'price': '15.00',
                'author_name': 'author 2',
                'annotated_likes': 2,
                'rating': '3.50',
                'creator_name': '',
                'readers': [
                    {
                        'first_name': 'Max',
                        'last_name': 'Karabtsov'
                    },
                    {
                        'first_name': 'Bugs',
                        'last_name': 'Banny'
                    },
                    {
                        'first_name': '0',
                        'last_name': '1'
                    },
                ]
            },
        ]
        self.assertEqual(expected_data, data)
