from django.shortcuts import render
from django.views.generic import ListView, DetailView
from worker.models import *


class IndexMovieListView(ListView):
    template_name = 'client/index.html'
    model = Movie
    queryset = Movie.objects.all()


class FilmMovieDetailView(DetailView):
    template_name = 'client/film.html'
    model = Movie

    def get_context_data(self, **kwargs):
        context = super(FilmMovieDetailView, self).get_context_data(**kwargs)
        context['showtime'] = Showtime.objects.filter(movie_id=self.get_object())
        return context


def index(request):
    return render(request, 'client/index.html', context={})


def cennik(request):
    return render(request, 'client/cennik.html', context={})


def kontakt(request):
    return render(request, 'client/kontakt.html', context={})


def okinie(request):
    return render(request, 'client/okinie.html', context={})


def repertuar(request):
    return render(request, 'client/repertuar.html', context={})


def rezerwacja(request):
    return render(request, 'client/rezerwacja.html', context={})
