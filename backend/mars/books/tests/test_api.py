import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from books.serializers import BooksSerializer


class BooksAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(title='test book 1', price='10', author_name='author 1')
        self.book_2 = Book.objects.create(title='test book 2', price='35', author_name='author 2')
        self.book_3 = Book.objects.create(title='test book author 1', price='25', author_name='author 3')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_id(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        response = self.client.get(url)
        serializer_data = BooksSerializer(self.book_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 10})
        serializer_data = BooksSerializer([self.book_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'author 1'})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BooksSerializer([self.book_1, self.book_3, self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "title": "Python",
            "price": 200,
            "author_name": "Chak Zero"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "title": self.book_1.title,
            "price": 190,
            "author_name": self.book_1.title
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1 = Book.objects.get(id=self.book_1.id)
        self.assertEqual(190, self.book_1.price)

    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())
