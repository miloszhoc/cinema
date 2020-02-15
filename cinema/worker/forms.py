from django.forms import *
from .models import *
from django.contrib.admin import widgets as admin_widget


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
            'duration': TimeInput(attrs={'class': 'timepicker', 'autocomplete': 'off', 'type': 'time'}),
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
            'show_break': TimeInput(attrs={'class': 'timepicker', 'autocomplete': 'off'})}


class ReservationModelForm(ModelForm):
    class Meta:
        model = Reservation
        labels = {'showtime_id': 'Seans',
                  'client_id': 'Klient',
                  'cost': 'Należność',
                  'is_paid': 'Czy zapłacono'}

        fields = ['showtime_id', 'client_id', 'cost', 'is_paid', 'ticket_id']
