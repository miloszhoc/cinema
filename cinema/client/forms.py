from django.forms import *
from django.forms.utils import ErrorList

from worker.models import *
from django.contrib.admin import widgets as admin_widget


class ReservationModelForm(ModelForm):

    class Meta:
        model = Reservation
        labels = {'showtime_id': '', }
        fields = ['showtime_id',]

    def __init__(self, *args, **kwargs):
        super(ReservationModelForm, self).__init__(*args, **kwargs)

        # pass initial data to form https://www.geeksforgeeks.org/initial-form-data-django-forms/
        if 'initial' in kwargs:
            self.showtime_id = kwargs['initial']['showtime_id']
            taken_seats = Ticket.objects.filter(showtime_id=self.showtime_id)
            # jesli user zostal przekierowany na ta strone z seansu o id 23,
            # to seans automatycznie podstawia sie w polu bez mozliwosci zmiany
            self.fields['showtime_id'].initial = self.showtime_id

            # https://stackoverflow.com/questions/4662848/disabled-field-is-not-passed-through-workaround-needed
            # jesli pole bylo ustawione jako disabled, to nie wysylalo się w poscie
            self.fields['showtime_id'].widget.attrs['style'] = 'display:none;'

    class Media:
        js = ('js/hover_reservation.js',)


class ClientModelForm(ModelForm):
    class Meta:
        model = Client
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
            'phone_number': 'Numer telefonu'
        }

        fields = ['first_name', 'last_name', 'email', 'phone_number']
