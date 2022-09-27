from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from books.serializers import BooksSerializer


class BooksAPITestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(title='test book 1', price='10')
        book_2 = Book.objects.create(title='test book 2', price='15')
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([book_1, book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)



