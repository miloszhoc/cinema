from django.shortcuts import render
from django.shortcuts import redirect
import django.forms
from . import models
from . import forms
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
# https://stackoverflow.com/questions/10275164/django-generic-views-using-decorator-login-required
# Jeśli klasy listview, detailview itd rozszerzają tę klasę, to wejście pod adres jest niemożliwe bez logowania
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


# aby dostac się do strony wymagane jest zalogowanie, jeśli user nie jest zalogowany,
# to przekierowuje do templatki, która jest podana w settings.py jako LOGIN_URL
@login_required()
def panel(request):
    return render(request, 'worker/panel.html', context={})


# jesli zalogowany user wejdzie na strone logowania, to prekierowuje do panelu,
# w przeciwnym wypadku pozwala się zalogować
def main(request):
    if request.user.is_authenticated:
        return redirect('panel')
    else:
        return render(request, 'main.html', context={})


@login_required()
def add_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.cleaned_data.get('username')

    return render(request, 'worker/uzytkownicy/dodaj_uzytkownika.html', context={'form': form})


# typy biletów
class TicketTypeListView(LoginRequiredMixin, ListView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/typy_lista.html'
    paginate_by = 10
    # sortowanie asc po id, czyli wg kolejnosci dodania
    ordering = ['ticket_id']


class TicketTypeCreateView(LoginRequiredMixin, CreateView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/dodaj_typ.html'
    form_class = forms.TicketTypeModelForm
    success_url = reverse_lazy('tickettype-list-worker')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    # def get_form(self, form_class=None):
    #     form = super(TicketTypeCreateView, self).get_form()
    #     form.fields['ticket_id'].queryset =


class TicketTypeDetailView(LoginRequiredMixin, DetailView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/szczegoly_typu.html'


class TicketTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/dodaj_typ.html'
    form_class = forms.TicketTypeModelForm
    success_url = reverse_lazy('tickettype-list-worker')

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.TicketType, ticket_id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class TicketTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/usun_typ.html'
    success_url = reverse_lazy('tickettype-list-worker')


# rezerwacje
@login_required
@transaction.atomic
def reservation_form(request, **kwargs):  # kwargs przekazywanie z urls
    showtime_id = kwargs['showtime_id']
    # pass initial data to form https://www.geeksforgeeks.org/initial-form-data-django-forms/
    initial = {'showtime_id': showtime_id}

    r_form = forms.ReservationModelForm(initial=initial)
    client_form = forms.ClientModelForm()

    # lista zajetych siedzien
    taken_seats = models.Ticket.objects.filter(showtime_id=showtime_id).values_list('seat_id', flat=True)

    s_form = forms.SeatForm(taken_seats=taken_seats)

    # siedzenia wolne
    seats = models.Seat.objects

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
        client_form = forms.ClientModelForm(request.POST)

        if client_form.is_valid() and r_form.is_valid():
            request.session['taken'] = taken
            request.session['data'] = request.POST

            return redirect('summary-worker')

    return render(request, 'worker/rezerwacje/dodaj_rezerwacje.html', context={'showtime_id': showtime_id,
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
@login_required
def summary(request, **kwargs):
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

    showtime = models.Showtime.objects.get(showtime_id=showtime_id)

    r_form = forms.ReservationModelForm(initial=reservation_initial)
    r_form.fields['showtime_id'].widget = r_form.fields['showtime_id'].hidden_widget()

    client_form = forms.ClientModelForm(initial=client_initial)
    client_form.fields['first_name'].widget = client_form.fields['first_name'].hidden_widget()
    client_form.fields['last_name'].widget = client_form.fields['last_name'].hidden_widget()
    client_form.fields['email'].widget = client_form.fields['email'].hidden_widget()
    client_form.fields['phone_number'].widget = client_form.fields['phone_number'].hidden_widget()

    ticket_formset = modelformset_factory(models.Ticket,
                                          fields=('seat_id', 'tickettype_id'),
                                          labels={'seat_id': '',
                                                  'tickettype_id': 'Typ Biletu'},
                                          extra=len(taken),
                                          widgets={'seat_id': django.forms.Select(attrs={'hidden': ''})},
                                          max_num=10)

    ticket_form = ticket_formset(queryset=models.Ticket.objects.none(), initial=[{'seat_id': z} for z in taken])

    if request.POST:
        r_form = forms.ReservationModelForm(request.POST)
        client_form = forms.ClientModelForm(request.POST)
        ticket_form = ticket_formset(request.POST)

        if ticket_form.is_valid() and (client_form.is_valid() and r_form.is_valid()):
            showtime = models.Showtime.objects.get(showtime_id=showtime_id)  # obiekt seansu
            client = client_form.save()
            reservation = r_form.save(commit=False)
            reservation.client_id = client
            reservation.confirmed = True

            # https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/#many-to-many-relationships
            instances = ticket_form.save(commit=False)

            # get total price
            total_price = 0
            for instance in instances:
                total_price += models.TicketType.objects.get(ticket_id=instance.tickettype_id_id).price

            reservation.cost = total_price
            reservation.save()

            for instance in instances:
                instance.client_id = client
                instance.showtime_id = showtime
                instance.save()
                reservation.ticket_id.add(instance)

            r_form.save_m2m()
            return redirect(reverse('showtime-details-worker', kwargs={'pk': showtime_id}))

    return render(request, 'worker/rezerwacje/podsumowanie.html', context={'taken': taken,
                                                                           'ticket_form': ticket_form,
                                                                           'reservation_form': r_form,
                                                                           'client_form': client_form,
                                                                           'client_initial': client_initial,
                                                                           'reservation_initial': reservation_initial,
                                                                           'showtime': showtime})


@login_required
@transaction.atomic
def reservation_update(request, **kwargs):
    reservation_id = kwargs['reservation_id']
    reservation = models.Reservation.objects.get(reservation_id=reservation_id)

    # bilety przekazywane jako initial do formset factory
    tickets_initial = reservation.ticket_id.values('seat_id', 'tickettype_id')

    showtime_id = reservation.showtime_id.showtime_id

    reservation_initial = {'showtime_id': reservation.showtime_id.showtime_id,
                           'confirmed': reservation.confirmed,
                           'paid': reservation.paid}
    r_form = forms.ReservationModelForm(initial=reservation_initial)

    client_initial = {'first_name': reservation.client_id.first_name,
                      'last_name': reservation.client_id.last_name,
                      'email': reservation.client_id.email,
                      'phone_number': reservation.client_id.phone_number}
    client_form = forms.ClientModelForm(initial=client_initial)

    ticket_formset = modelformset_factory(models.Ticket,
                                          fields=('seat_id', 'tickettype_id'),
                                          labels={'seat_id': 'Miejsce',
                                                  'tickettype_id': 'Typ Biletu', },
                                          extra=len(reservation.ticket_id.values()),
                                          max_num=10, can_delete=True)

    ticket_form = ticket_formset(queryset=models.Ticket.objects.none(), initial=tickets_initial)

    if request.POST:
        if 'ticket_num' in request.POST:
            ticket_formset = modelformset_factory(models.Ticket,
                                                  fields=('seat_id', 'tickettype_id'),
                                                  labels={'seat_id': 'Miejsce',
                                                          'tickettype_id': 'Typ Biletu', },
                                                  extra=int(request.POST['ticket_select']),
                                                  max_num=10, can_delete=True)

            ticket_form = ticket_formset(queryset=models.Ticket.objects.none(), initial=tickets_initial)

        else:
            # current objects
            reservation_object = get_object_or_404(models.Reservation, reservation_id=reservation_id)
            client_object = get_object_or_404(models.Client, client_id=reservation.client_id.client_id)

            r_form = forms.ReservationModelForm(request.POST, instance=reservation_object)
            ticket_form = ticket_formset(request.POST)
            client_form = forms.ClientModelForm(request.POST, instance=client_object)

            if ticket_form.is_valid() and (client_form.is_valid() and r_form.is_valid()):
                showtime = models.Showtime.objects.get(showtime_id=showtime_id)  # obiekt seansu
                client = client_form.save()
                reservation = r_form.save(commit=False)
                reservation.client_id = client

                # https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/#many-to-many-relationships
                instances = ticket_form.save(commit=False)

                # get total price
                total_price = 0
                for instance in instances:
                    total_price += models.TicketType.objects.get(ticket_id=instance.tickettype_id_id).price

                reservation.cost = total_price
                reservation.save()

                tickets = models.Ticket.objects.filter(reservation__reservation_id=reservation_id)

                # usuwa wszytkie bilety powiązane z rezerwacją, oraz rezerwację
                for t in tickets.iterator():
                    t.delete()

                for instance in instances:
                    instance.client_id = client
                    instance.showtime_id = showtime
                    instance.save()
                    reservation.ticket_id.add(instance)

                r_form.save_m2m()
                return redirect(reverse('movie-details-worker', kwargs={'pk': str(showtime.movie_id.movie_id)}))

    return render(request, 'worker/rezerwacje/edytuj-rezerwacje.html', context={'reservation': reservation,
                                                                                'r_form': r_form,
                                                                                'client_form': client_form,
                                                                                'ticket_form': ticket_form,
                                                                                'ticket_number': [x for x in
                                                                                                  range(1, 11)], })


# seanse
class ShowtimeListView(LoginRequiredMixin, ListView):
    model = models.Showtime
    paginate_by = 10
    ordering = ['-showtime_id']
    template_name = 'worker/seanse/seans_lista.html'


class ShowtimeDetailView(LoginRequiredMixin, DetailView):
    model = models.Showtime
    template_name = 'worker/seanse/szczegoly_seansu.html'

    # w templatce polazuje tylko rezerwacje na konkretny seans + bilety, ktore byly zakupione w ramach rezerwacji
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = models.Reservation.objects.filter(showtime_id=self.get_object())
        context['tickets'] = models.Ticket.objects.filter(showtime_id=self.get_object())
        return context


class ShowtimeCreateView(LoginRequiredMixin, CreateView):
    model = models.Showtime
    template_name = 'worker/seanse/dodaj_seans.html'
    form_class = forms.ShowtimeModelForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ShowtimeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Showtime
    template_name = 'worker/seanse/dodaj_seans.html'
    form_class = forms.ShowtimeModelForm

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.Showtime, showtime_id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ShowtimeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Showtime
    template_name = 'worker/seanse/usun_seans.html'
    success_url = reverse_lazy('showtime-list-worker')


# filmy
class MovieListView(LoginRequiredMixin, ListView):
    model = models.Movie
    template_name = 'worker/filmy/lista_filmow.html'
    paginate_by = 10
    # sortowanie asc po id, czyli wg kolejnosci dodania
    ordering = ['movie_id']


class MovieDetailView(LoginRequiredMixin, DetailView):
    model = models.Movie
    template_name = 'worker/filmy/szczegoly_filmu.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = models.Movie
    template_name = 'worker/filmy/dodaj_film.html'
    form_class = forms.MovieModelForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Movie
    template_name = 'worker/filmy/dodaj_film.html'
    form_class = forms.MovieModelForm

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.Movie, movie_id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Movie
    template_name = 'worker/filmy/usun_film.html'
    success_url = reverse_lazy('movie-list-worker')
