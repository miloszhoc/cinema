from django.forms import *
from .models import *
from django.contrib.admin import widgets as admin_widget
from django.forms.models import modelformset_factory

ReservationFormSet = modelformset_factory(Reservation, fields=('ticket_id', 'showtime_id'))
formset = ReservationFormSet(queryset=Reservation.objects.all())


class MovieModelForm(ModelForm):
    class Meta:
        model = Movie
        labels = {
            'title': 'Tytuł filmu',
            'director': 'Reżyser',
            'release_date': 'Data premiery',
            'duration': 'Czas trwania',
            'description': 'Opis',
            'link': 'Link do serwisu z opiniami',
            'thumbnail': 'Link do miniatury',
            'trailer_youtube_id': 'ID trailera z serwisu Youtube'
        }
        fields = ['title', 'director',
                  'release_date', 'duration',
                  'description', 'link',
                  'thumbnail', 'trailer_youtube_id']
        widgets = {
            'release_date': NumberInput(attrs={'min': 1800}),
            'duration': TextInput(attrs={'class': 'timepicker', 'autocomplete': 'off'}),
        }


class ShowtimeModelForm(ModelForm):
    class Meta:
        model = Showtime
        labels = {'movie_id': 'Film',
                  'start_date': 'Godzina i data rozpoczęcia',
                  'show_break': 'Przerwa po seansie',
                  }

        fields = ['movie_id', 'start_date', 'show_break']
        widgets = {
            'start_date': admin_widget.AdminSplitDateTime(),
            'show_break': TextInput(attrs={'class': 'timepicker', 'autocomplete': 'off'})}


class ReservationModelForm(ModelForm):
    class Meta:
        model = Reservation
        labels = {'showtime_id': 'Seans', }

        fields = ['showtime_id']

    def __init__(self, showtime_id, *args, **kwargs):
        super(ReservationModelForm, self).__init__(*args, **kwargs)
        # self.fields['ticket_id'].queryset = Reservation.objects.filter(showtime_id=self.showtime_id)

        # jesli user zostal przekierowany na ta strone z seansu o id 23,
        # to seans automatycznie podstawia sie w polu bez mozliwosci zmiany
        self.fields['showtime_id'].initial = showtime_id
        self.fields['showtime_id'].disabled = True


class TicketModelForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['client_id', 'seat_id']

    def __init__(self, client_id, *args, **kwargs):
        super(TicketModelForm, self).__init__(*args, **kwargs)

        self.fields['client_id'].initial = client_id
        # self.fields[''].disabled = True


class ReservationTicketModelForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['client_id', 'ticket_id']

    def __init__(self, reservation_id, client_id, *args, **kwargs):
        super(ReservationTicketModelForm, self).__init__(*args, **kwargs)
        self.fields['client_id'].initial = client_id
        self.fields['client_id'].disabled = True
        self.fields['ticket_id'].queryset = Ticket.objects.filter(reservation__reservation_id=reservation_id)


class TicketTypeModelForm(ModelForm):
    class Meta:
        model = TicketType
        labels = {'type': 'Typ biletu',
                  'price': 'Cena'}

        fields = ['ticket_id', 'type', 'price']


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
