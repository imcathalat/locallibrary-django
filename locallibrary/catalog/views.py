from catalog.models import Book, Author, BookInstance, Genre
from django.shortcuts import render
from django.views import generic


def index(request):
    
    num_books = Book.objects.all(). count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre_romance = Book.objects.all().filter(genre = 1).count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    request.session.modified = True

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre_romance': num_genre_romance,
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 3

    queryset = Book.objects.all()
    #a query retorna uma lista? isso é um método slicing?

    template_name = 'book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        context['some_data'] = 'This is just some data'

        return context
    
class BookDetailView(generic.DetailView):

    model = Book
    template_name = 'catalog/book_detail.html'

class AuthorListView(generic.ListView):
    model: Author
    paginate_by = 2

    queryset = Author.objects.all()
    context_object_name = 'author_list'

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 4

    

    
    

