from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from books.views import BookViewSet, UserBookRelationView

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBookRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]

urlpatterns += router.urls
