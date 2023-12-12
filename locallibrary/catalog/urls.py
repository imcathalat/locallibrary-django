from django.urls import path,re_path
from django.views.generic import RedirectView
from catalog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:page>', views.listing, name='books-by-page'),
    path('books.json', views.listing_api, name='list-books-api'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name="authors_detail"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path(r'allbooks/', views.LoanedBooksForLIbraryans.as_view(), name="allbooks-borrowed"),
    path('book/<uuid:pk>/renew/', views.RenewBookView.as_view(), name='renew-book-librarian'), # pq n usar o (?P<pk>\d+)?
    # como exatamente essa pk vai receber um valor? ja na view?
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name="book-create"),
    path('book/<int:pk>/update', views.BookUpdate.as_view(), name="book-update"),
    path('book/<int:pk>/delete', views.BookDelete.as_view(), name="book-delete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
