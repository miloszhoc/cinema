import django.forms
from django.core.mail import send_mail
from django.db import transaction
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from worker.models import *
from . import forms
# nalezy uzywac metody timezone.now(),
# aby wyeliminowac problem "RuntimeWarning: DateTimeField Showtime.start_date received a naive datetime
# while time zone support is active."
from django.utils import timezone
from cinema.settings import EMAIL_HOST_USER
from django.template import loader
from django.contrib import messages
from django.shortcuts import get_object_or_404


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

        # obecny czas w strefie czasowej CET
        tz_now = timezone.now()
        # context['events'] = Event.objects.all()  # todo dodac sortowanie wg daty
        # wyswietla filmy ktore sa grane dzisiaj,
        # oraz data rozpoczecia jest w przyszlosci - czyli od obecnej godziny do północy
        # context['today'] = Movie.objects.filter(showtime__start_date__day=tz_now.day,
        #                                         showtime__start_date__gte=tz_now).distinct()
        context['today'] = Movie.objects.filter(showtime__start_date__day=tz_now.day,
                                                showtime__start_date__gte=tz_now).distinct()
        # jutrzejszy dzień  - godzina 00:00:00
        tomorrow = tz_now - timezone.timedelta(hours=tz_now.hour,
                                               minutes=tz_now.minute,
                                               seconds=tz_now.second) + timezone.timedelta(days=1)

        context['future'] = Movie.objects.filter(movie_id__in=Showtime.objects.values('movie_id'),
                                                 showtime__start_date__gt=tomorrow).distinct()

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

    s_form = forms.SeatForm(taken_seats=taken_seats)

    # siedzenia wolne
    seats = Seat.objects
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

    if request.POST:
        taken = []
        for i in request.POST.lists():
            if i[0].startswith('seats_row_'):
                taken.extend(i[1])

        r_form = forms.ReservationModelForm(request.POST)
        r_form.fields['showtime_id'].widget = r_form.fields['showtime_id'].hidden_widget()
        client_form = forms.ClientModelForm(request.POST)

        if client_form.is_valid() and r_form.is_valid():
            request.session['taken'] = taken
            request.session['data'] = request.POST

            if len(taken) > 10:
                messages.add_message(request, messages.ERROR, 'Możesz zarezerwować maksymalnie 10 miejsc!')
            else:
                return redirect('summary-client')

    return render(request, 'client/rezerwacja_na_seans.html', context={'showtime_id': showtime_id,
                                                                       'showtime': showtime,
                                                                       'client_form': client_form,
                                                                       'reservation_form': r_form,
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
                                                                       'taken_seats': taken_seats,
                                                                       's_form': s_form})


@transaction.atomic
def summary_client(request, **kwargs):
    taken = request.session.get('taken')
    data = request.session.get('data')
    showtime_id = data['showtime_id']

    paid = data['paid'] if data.get('paid') else ''
    confirmed = data['confirmed'] if data.get('confirmed') else ''

    reservation_initial = {'showtime_id': data['showtime_id'],
                           'confirmed': confirmed,
                           'paid': paid}

    client_initial = {'first_name': data['first_name'],
                      'last_name': data['last_name'],
                      'email': data['email'],
                      'phone_number': data['phone_number']}

    showtime = Showtime.objects.get(showtime_id=showtime_id)

    r_form = forms.ReservationModelForm(initial=reservation_initial)
    r_form.fields['showtime_id'].widget = r_form.fields['showtime_id'].hidden_widget()

    client_form = forms.ClientModelForm(initial=client_initial)
    client_form.fields['first_name'].widget = client_form.fields['first_name'].hidden_widget()
    client_form.fields['last_name'].widget = client_form.fields['last_name'].hidden_widget()
    client_form.fields['email'].widget = client_form.fields['email'].hidden_widget()
    client_form.fields['phone_number'].widget = client_form.fields['phone_number'].hidden_widget()

    ticket_formset = modelformset_factory(Ticket,
                                          fields=('seat_id', 'tickettype_id'),
                                          labels={'seat_id': '',
                                                  'tickettype_id': 'Typ Biletu'},
                                          extra=len(taken),
                                          widgets={'seat_id': django.forms.Select(attrs={'hidden': ''})},
                                          max_num=10)

    ticket_form = ticket_formset(queryset=Ticket.objects.none(), initial=[{'seat_id': z} for z in taken])
    if request.POST:
        r_form = forms.ReservationModelForm(request.POST)
        client_form = forms.ClientModelForm(request.POST)
        ticket_form = ticket_formset(request.POST)

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
            # full_email = EMAIL_HOST_USER + '@' + EMAIL_DOMAIN
            # https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
            # https://stackoverflow.com/questions/29466796/sending-a-html-email-in-django
            html_mail = loader.render_to_string(template_name='client/rezerwacja/email.html',
                                                context={'first_name': client.first_name,
                                                         'last_name': client.last_name,
                                                         'uuid': reservation.reservation_confirmation_code,
                                                         'domain': request.META['HTTP_HOST']})

            print(send_mail(subject='Potwierdzenie rezerwacji',
                            message='',
                            from_email=EMAIL_HOST_USER,
                            recipient_list=[client.email, ],
                            fail_silently=False,
                            html_message=html_mail))

            messages.add_message(request, messages.SUCCESS, 'Rezerwacja została pomyślnie utworzona, na twój adres'
                                                            'mailowy została wysłana wiadomość z potwierdzeniem.'
                                                            'Jeśli nie potwierdzisz rezerwacji w ciągu 30 minut, '
                                                            'to zostanie ona usunięta z systemu')
            return redirect(reverse('movie-details-client', kwargs={'pk': str(showtime.movie_id.movie_id)}))

    return render(request, 'client/podsumowanie.html', context={'taken': taken,
                                                                'ticket_form': ticket_form,
                                                                'reservation_form': r_form,
                                                                'client_form': client_form,
                                                                'client_initial': client_initial,
                                                                'reservation_initial': reservation_initial,
                                                                'showtime': showtime})


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

    queryset = Showtime.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
    model = Showtime

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


def rezerwacja(request):
    return render(request, 'client/rezerwacja.html', context={})


# potwierdza rezerwacje
@transaction.atomic()
def rezerwacja_potwierdz(request, **kwargs):
    reservation_uuid = kwargs['id']
    form = forms.ConfirmReservationForm(initial={'text_field': reservation_uuid})
    if request.POST:
        form = forms.ConfirmReservationForm(request.POST, initial={'text_field': reservation_uuid})

        if form.is_valid() and not get_object_or_404(Reservation,
                                                     reservation_confirmation_code=reservation_uuid).confirmed:
            Reservation.objects.filter(reservation_confirmation_code=reservation_uuid).update(confirmed=True)
            messages.add_message(request, messages.SUCCESS, 'Rezerwacja została pomyślnie potwierdzona.')
            return redirect('index-client')
        else:
            messages.add_message(request, messages.ERROR, 'Rezerwacja została już potwierdzona.')
    return render(request, 'client/rezerwacja/potwierdz_rezerwacje.html', context={'reservation_uuid': reservation_uuid,
                                                                                   'form': form})


# usuwa rezerwacje tylko jesli rezerwacja nie zostala wczesniej potwierdzona
@transaction.atomic()
def rezerwacja_anuluj(request, **kwargs):
    reservation_uuid = kwargs['id']
    form = forms.ConfirmReservationForm(initial={'text_field': reservation_uuid})

    if request.POST:
        form = forms.ConfirmReservationForm(request.POST, initial={'text_field': reservation_uuid})

        if form.is_valid() and not get_object_or_404(Reservation,
                                                     reservation_confirmation_code=reservation_uuid).confirmed:
            reservation = Reservation.objects.get(reservation_confirmation_code=reservation_uuid)
            tickets = Ticket.objects.filter(reservation__reservation_confirmation_code=reservation_uuid)
            # usuwa wszytkie bilety powiązane z rezerwacją, oraz rezerwację
            for t in tickets.iterator():
                t.delete()
            reservation.delete()

            Client.objects.get(client_id=reservation.client_id.client_id).delete()

            messages.add_message(request, messages.SUCCESS, 'Rezerwacja została pomyślnie usunięta.')
            return redirect('index-client')
        else:
            # https://www.kodefork.com/questions/30/how-to-pass-a-message-when-we-redirect-to-some-template-from-django-views/
            messages.add_message(request, messages.ERROR, 'Nie można anulować! Rezerwacja została już potwierdzona.')
    return render(request, 'client/rezerwacja/anuluj_rezerwacje.html', context={'reservation_uuid': reservation_uuid,
                                                                                'form': form})
