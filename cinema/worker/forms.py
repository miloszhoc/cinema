from django.forms import *
from .models import *


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


class ShowtimeModelForm(ModelForm):
    class Meta:
        model = Showtime
        labels = {'movie_id': 'Film',
                  'start_date': 'Godzina Rozpoczęcia',
                  'show_break': 'Przerwa po seansie',
                  }

        fields = ['movie_id', 'start_date', 'show_break']
