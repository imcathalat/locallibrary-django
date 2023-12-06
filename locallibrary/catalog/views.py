import datetime

from catalog.models import Book, Author, BookInstance, Author
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.core.paginator import Paginator

from catalog.forms import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



def BASE(request):
    return render(request, 'base.html')

def index(request):

    num_books = Book.objects.all(). count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre_romance = Book.objects.all().filter(genre = 1).count()
    num_borrowed_books = BookInstance.objects.all().filter(status__exact='o').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    request.session.modified = True

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'num_borrowed_books': num_borrowed_books
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 3

    queryset = Book.objects.all().order_by('title')
    #a query retorna uma lista? isso é um método slicing?

    template_name = 'book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        return context

def listing(request, page):
        books = Book.objects.all()
        paginator = Paginator(books, per_page=3)
        page_object = paginator.get_page(page)
        context = {"page_obj": page_object}
        return render(request, "catalog/book_list.html", context)

def listing_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 3)
    startswith = request.GET.get("startswith", "")
    books = Book.objects.filter(
        title__startswith=startswith
    )
    paginator = Paginator(books, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"title": book.title} for book in page_obj.object_list ]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        },
        "data": data
    }

    return JsonResponse(payload)

class BookDetailView(generic.DetailView):

    model = Book
    template_name = 'catalog/book_detail.html'

class AuthorListView(generic.ListView):
    model: Author
    paginate_by = 10

    queryset = Author.objects.all()
    context_object_name = 'author_list'

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 4


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        )


class LoanedBooksForLIbraryans(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_libraryans.html'
    paginate_bt = 10


    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )


class RenewBookModelForm(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_mark_returned'

    book_instance = None
    ##print(type(book_instance))

    def get(self, request, pk):
        self.book_instance = BookInstance.objects.get(pk=pk)
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm()

        context = {
            'form': form,
            'book_instance': self.book_instance
        }

        ##return render(reverse(request, 'catalog/book_renew_librarian.html', context))
        return render(request, 'catalog/book_renew_librarian.html', context)
        ##return HttpResponseRedirect(reverse('catalog/book_renew_librarian.html', context))
    
    def post(self, pk, request):
        self.book_instance = BookInstance.objects.get(pk=pk)
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            self.book_instance.due_back = form.cleaned_data['renewal_date']
            self.book_instance.save()

            return HttpResponseRedirect(reverse('allbooks-borrowed')) ##HttpResponseRedirect redireciona 
        ##pra uma URL especifica e o reverse() cria uma url a partir do nome de url setado la na urls.py
        
        else:
            context = {
                'form': form,
                'book_instance': self.book_instance,
            }

            return render(request, 'catalog/book_renew_librarian.html', context)
      

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.change_author'
    success_url = reverse_lazy('authors')

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )
        
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.add_book'

class  BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.delete_book'
    success_url = reverse_lazy('books')
    