from catalog.models import BookInstance, Author, Book, Genre, Language
from django import forms

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
import datetime





# class RenewBookForm(forms.Form):
#     renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

#     def clean_renewal_date(self):
#         data = self.cleaned_data['renewal_date']

#         # Check if a date is not in the past.
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))

#         # Check if a date is in the allowed range (+4 weeks from today).
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

#         # Remember to always return the cleaned data.
#         return data


class RenewBookModelForm(forms.ModelForm):

    # def clean_due_back(self):
    #     data = self.cleaned_data['due_back']

    #     if data < datetime.date.today():
    #         raise ValidationError(_('Invalid date - renewal in past'))
        
    #     if data > datetime.date.today() + datetime.timedelta(weeks=4):
    #         raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
    #     return data

    def set_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data
    
    class Meta:
        model = BookInstance
        fields = ['due_back']
        widgets = {
            'due_back': forms.DateInput(attrs={'class': 'form-control form-control-rounded mb-2'})
        }
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}

class CreateAuthorForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Primeiro Nome', 'class': 'form-control form-control-rounded mb-2'}
    ))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Segundo Nome', 'class': 'form-control form-control-rounded mb-2'}
    ))

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-rounded mb-2'}
    ))

    date_of_death = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-rounded mb-2'}
    ))

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
        

class CreateBookForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Titulo', 'class': 'form-control form-control-rounded mb-2'}
    ))

    summary = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Description of the book', 'class': 'form-control form-control-rounded mb-2', 'rows': '2'}
    ))

    isbn = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': '13 character ISBN', 'class': 'form-control form-control-rounded mb-2'}
    ))

    author = forms.ModelChoiceField(
        queryset= Author.objects.all(),
        to_field_name='first_name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control form-control-rounded mb-2'})
    )

    genre = forms.ModelChoiceField(
        queryset= Genre.objects.all(),
        to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control form-control-rounded mb-2'})
    )

    language = forms.ModelChoiceField(
        queryset= Language.objects.all(),
        to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control form-control-rounded mb-2'})
    )

    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'author', 'language', 'genre']

