from django.db import transaction
from django.forms import modelformset_factory
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from worker.models import *
from . import forms
# nalezy uzywac metody timezone.now(),
# aby wyeliminowac problem "RuntimeWarning: DateTimeField Showtime.start_date received a naive datetime
# while time zone support is active."
from django.utils import timezone
from .forms import ReservationModelForm


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


@transaction.atomic
def reservation_form(request, **kwargs):  # kwargs przekazywanie z urls
    showtime_id = kwargs['showtime_id']
    showtime = Showtime.objects.get(showtime_id=showtime_id)

    # pass initial data to form https://www.geeksforgeeks.org/initial-form-data-django-forms/
    initial = {'showtime_id': showtime_id}
    r_form = forms.ReservationModelForm(initial=initial)
    client_form = forms.ClientModelForm()

    # lista zajetych siedzien
    taken_seats = Ticket.objects.filter(showtime_id=showtime_id).values_list('seat_id', flat=True)
    # siedzenia wolne
    seats = Seat.objects
    ticket = Ticket.objects
    seats_row_a = seats.filter(row_number='A')
    seats_row_b = seats.filter(row_number='B')
    seats_row_c = seats.filter(row_number='C')
    seats_row_d = seats.filter(row_number='D')
    seats_row_e = seats.filter(row_number='E')
    seats_row_f = seats.filter(row_number='F')
    seats_row_g = seats.filter(row_number='G')
    seats_row_h = seats.filter(row_number='H')
    seats_row_i = seats.filter(row_number='I')
    seats_row_j = seats.filter(row_number='J')

    ticket_formset = modelformset_factory(Ticket,
                                          fields=('seat_id', 'tickettype_id'),
                                          labels={'seat_id': 'Miejsce',
                                                  'tickettype_id': 'Typ Biletu'},
                                          extra=1,
                                          can_delete=True)
    ticket_form = ticket_formset(queryset=Ticket.objects.none())
    if request.POST:
        if 'ticket_number' in request.POST:
            ticket_formset = modelformset_factory(Ticket,
                                                  fields=('seat_id', 'tickettype_id'),
                                                  labels={'seat_id': 'Miejsce',
                                                          'tickettype_id': 'Typ Biletu'},
                                                  extra=int(request.POST['ticket_select']), can_delete=True)

            ticket_form = ticket_formset(queryset=Ticket.objects.none())
        else:
            # https://www.youtube.com/watch?v=FnZgy-y6hGA
            ticket_form = ticket_formset(request.POST)

            r_form = forms.ReservationModelForm(request.POST)
            client_form = forms.ClientModelForm(request.POST)

            if ticket_form.is_valid() and (client_form.is_valid() and r_form.is_valid()):
                showtime = Showtime.objects.get(showtime_id=showtime_id)  # obiekt seansu
                client = client_form.save()
                reservation = r_form.save(commit=False)
                reservation.client_id = client

                # https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/#many-to-many-relationships
                instances = ticket_form.save(commit=False)

                # get total price
                total_price = 0
                for instance in instances:
                    total_price += TicketType.objects.get(ticket_id=instance.tickettype_id_id).price

                reservation.cost = total_price
                reservation.save()

                for instance in instances:
                    instance.client_id = client
                    instance.showtime_id = showtime
                    instance.save()
                    reservation.ticket_id.add(instance)

                r_form.save_m2m()
                return redirect(reverse('movie-details-client', kwargs={'pk': str(showtime.movie_id.movie_id)}))

    return render(request, 'client/rezerwacja_na_seans.html', context={'showtime': showtime,
                                                                       'showtime_id': showtime_id,
                                                                       'client_form': client_form,
                                                                       'reservation_form': r_form,
                                                                       'ticket_form': ticket_form,
                                                                       'ticket_number': [i for i in
                                                                                         range(1, 11)],
                                                                       'seats_row_a': seats_row_a,
                                                                       'seats_row_b': seats_row_b,
                                                                       'seats_row_c': seats_row_c,
                                                                       'seats_row_d': seats_row_d,
                                                                       'seats_row_e': seats_row_e,
                                                                       'seats_row_f': seats_row_f,
                                                                       'seats_row_g': seats_row_g,
                                                                       'seats_row_h': seats_row_h,
                                                                       'seats_row_i': seats_row_i,
                                                                       'seats_row_j': seats_row_j,
                                                                       'taken_seats': taken_seats})


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


def rezerwacja(request):
    return render(request, 'client/rezerwacja.html', context={})
