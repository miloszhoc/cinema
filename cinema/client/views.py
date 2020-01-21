from django.shortcuts import render
from django.views.generic import ListView, DetailView
from worker.models import *
import datetime


class IndexMovieListView(ListView):
    template_name = 'client/index.html'
    model = Movie

    # wyswietla tylko filmy, ktorych seans zaczyna sie w przyszlosci
    # ukrywa filmy, ktore nie maja seansu, oraz te, ktorych czas rozpoczecia juz minal
    # eliminuje duplikaty w przypadku dodania wiecej niz jednego filmu
    queryset = Movie.objects.filter(movie_id__in=Showtime.objects.all(),
                                    showtime__start_date__gt=datetime.datetime.now()).distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexMovieListView, self).get_context_data(**kwargs)
        # wyswietla filmy ktore sa grane dzisiaj,
        # oraz data rozpoczecia jest w przyszlosci - czyli od obecnej godziny do północy
        context['today'] = Movie.objects.filter(showtime__start_date__day=datetime.date.today().day,
                                                showtime__start_date__gte=datetime.datetime.now()).distinct()
        return context


class FilmMovieDetailView(DetailView):
    template_name = 'client/film.html'
    model = Movie

    # wyswietla tylko filmy, ktorych seans zaczyna sie w przyszlosci
    def get_context_data(self, **kwargs):
        context = super(FilmMovieDetailView, self).get_context_data(**kwargs)
        context['showtime'] = Showtime.objects.filter(movie_id=self.get_object(),
                                                      start_date__gte=datetime.datetime.now())
        return context


class RezerwacjaNaSeansShowtimeDetailView(DetailView):
    template_name = 'client/rezerwacja_na_seans.html'
    model = Showtime

    # queryset = Showtime.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RezerwacjaNaSeansShowtimeDetailView, self).get_context_data(**kwargs)
        # tylko zajete miejsca lako lista zawierajaca tylko id siedzen
        # potrzebna, aby iterowac po siedzeniach w rzedzie i sprawdzac czy dane siedzenie jest zajete
        context['taken_seats'] = [seat[0] for seat in
                                  Ticket.objects.filter(showtime_id=self.get_object()).values_list('seat_id')]

        context['seats_row_a'] = Seat.objects.filter(row_number='A')
        context['seats_row_b'] = Seat.objects.filter(row_number='B')
        context['seats_row_c'] = Seat.objects.filter(row_number='C')
        context['seats_row_d'] = Seat.objects.filter(row_number='D')
        context['seats_row_e'] = Seat.objects.filter(row_number='E')
        context['seats_row_f'] = Seat.objects.filter(row_number='F')
        context['seats_row_g'] = Seat.objects.filter(row_number='G')
        context['seats_row_h'] = Seat.objects.filter(row_number='H')
        context['seats_row_i'] = Seat.objects.filter(row_number='I')
        context['seats_row_j'] = Seat.objects.filter(row_number='J')

        return context


#

# def index(request):
#     return render(request, 'client/index.html', context={})


def cennik(request):
    return render(request, 'client/cennik.html', context={})


def kontakt(request):
    return render(request, 'client/kontakt.html', context={})


def okinie(request):
    return render(request, 'client/okinie.html', context={})


class RepertuarShowtimeListView(ListView):
    template_name = 'client/repertuar.html'
    paginate_by = 10
    ordering = ['-date']
    # wszystkie seanse od dzisiaj, które nie powtarzaja sie
    queryset = Showtime.objects.filter(start_date__gte=datetime.datetime.today())
    model = Showtime

    def test_dates(self, all):
        out = {}
        for object in range(len(all) - 1):
            data = {}
            dates = set()
            for o2 in range(object, len(all)):
                if all[object]['movie_id_id'] == all[o2]['movie_id_id']:
                    dates.add(all[o2]['start_date'])
                    data[str((all[o2]['showtime_id']))] = dates
                    out[str(all[object]['movie_id_id'])] = data
                else:
                    dates = set()
        return out

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['movies_dates'] = self.test_dates(self.queryset.values())
        print(context['movies_dates'])
        return context


# def repertuar(request):
#     return render(request, 'client/repertuar.html', context={})


def rezerwacja(request):
    return render(request, 'client/rezerwacja.html', context={})
