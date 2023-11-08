from django.urls import path
from django.views.generic import RedirectView
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail')
    # como exatamente essa pk vai receber um valor? ja na view?
]
