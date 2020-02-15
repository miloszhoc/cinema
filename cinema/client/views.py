from django.shortcuts import render
from django.views.generic import ListView, DetailView
from worker.models import *
# nalezy uzywac metody timezone.now(),
# aby wyeliminowac problem "RuntimeWarning: DateTimeField Showtime.start_date received a naive datetime
# while time zone support is active."
from django.utils import timezone


class IndexMovieListView(ListView):
    template_name = 'client/index.html'
    model = Movie

    # wyswietla tylko filmy, ktorych seans zaczyna sie w przyszlosci
    # ukrywa filmy, ktore nie maja seansu, oraz te, ktorych czas rozpoczecia juz minal
    # eliminuje duplikaty w przypadku dodania wiecej niz jednego filmu
    pass

    # queryset = Movie.objects.filter(movie_id__in=Showtime.objects.all(),
    #                                 showtime__start_date__gt=timezone.now()).distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexMovieListView, self).get_context_data(**kwargs)

        # context['events'] = Event.objects.all()  # todo dodac sortowanie wg daty
        # wyswietla filmy ktore sa grane dzisiaj,
        # oraz data rozpoczecia jest w przyszlosci - czyli od obecnej godziny do północy
        context['today'] = Movie.objects.filter(showtime__start_date__day=timezone.now().day,
                                                showtime__start_date__gte=timezone.now()).distinct()
        # obecny czas w strefie czasowej CET
        tz_now = timezone.now()

        # jutrzejszy dzień  - godzina 00:00:00
        tomorrow = tz_now - timezone.timedelta(hours=tz_now.hour,
                                               minutes=tz_now.minute,
                                               seconds=tz_now.second) + timezone.timedelta(days=1)

        context['future'] = Movie.objects.filter(movie_id__in=Showtime.objects.values('movie_id'),
                                                 showtime__start_date__gt=timezone.now() + timezone.timedelta(
                                                     days=1)).distinct()

        return context


class FilmMovieDetailView(DetailView):
    template_name = 'client/film.html'
    model = Movie

    # wyswietla tylko filmy, ktorych seans zaczyna sie w przyszlosci, sortuje po dacie rozpoczecia
    def get_context_data(self, **kwargs):
        context = super(FilmMovieDetailView, self).get_context_data(**kwargs)
        context['showtime'] = Showtime.objects.filter(movie_id=self.get_object(),
                                                      start_date__gte=timezone.now()).order_by('start_date')
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


# w zakładce seanse na 14 dni od dnia dzisiejszego
# lista dat od dnia dzisiejszego, które w templatce sa porownywane z datami seansow, jesli data seansu jest rowna dacie
# na liscie dat, to seans jest wypisywany na ekranie
class RepertuarShowtimeListView(ListView):
    template_name = 'client/repertuar.html'

    # wszystkie seanse od dzisiaj, które nie powtarzaja sie
    queryset = Showtime.objects.filter(movie_id__movie_id__in=Showtime.objects.all(),
                                       movie_id__showtime__start_date__gt=timezone.now()).distinct()
    model = Showtime

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['showtime_dates'] = Showtime.objects.filter(start_date__gte=timezone.now()).select_related()
        # 14 dni od dzisiejszego dnia
        context['dates'] = list(map(lambda x: timezone.now() + timezone.timedelta(days=x), range(14)))
        return context


# def repertuar(request):
#     return render(request, 'client/repertuar.html', context={})


def rezerwacja(request):
    return render(request, 'client/rezerwacja.html', context={})
