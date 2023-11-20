import datetime
from django import forms 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a ate between now and 4 weeks (default 3). ")

    def clean_renewall_date(self):
        data = self.cleaned_data['renewall_date'] ## valida o form 'renewall_date' e armazena a data passada no field para a variável data

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data