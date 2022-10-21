from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from books.models import Book, UserBookRelation


class BooksReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    creator_name = serializers.CharField(source='creator.username', default='', read_only=True)
    readers = BooksReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'author_name', 'annotated_likes', 'rating', 'creator_name', 'readers')


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
