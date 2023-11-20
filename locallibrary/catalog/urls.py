from django.urls import path,re_path
from django.views.generic import RedirectView
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name="authors_detail"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path(r'allbooks/', views.LoanedBooksForLIbraryans.as_view(), name="allbooks-borrowed"),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'), # pq n usar o (?P<pk>\d+)?
    # como exatamente essa pk vai receber um valor? ja na view?
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]
