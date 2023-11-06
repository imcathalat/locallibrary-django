from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(BookInstance)
#admin.site.register(Book)



class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    fields = [('title', 'author'), 'summary', 'isbn', ('language', 'genre')]
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ('book', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability',{
            'fields': ('status', 'due_back')
        })
    )


# Registrando as models para o admin do django