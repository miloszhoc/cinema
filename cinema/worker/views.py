from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.urls import resolve
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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.cleaned_data.get('username')
    else:
        form = UserCreationForm()
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
class ReservationListView(LoginRequiredMixin, ListView):
    model = models.Reservation
    template_name = 'worker/rezerwacje/rezerwacje_lista.html'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = models.Reservation
    template_name = 'worker/rezerwacje/dodaj_rezerwacje.html'
    form_class = forms.ReservationModelForm

    # jesli wystapi blad, to nic nie zostaje zapisane do bazy
    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        client_form = context['client_form']
        if client_form.is_valid() and form.is_valid():
            c = client_form.save()
            f = form.save(commit=False)
            f.client_id = c
            f.save()
            return redirect(reverse('showtime-details-worker', kwargs={'pk': self.kwargs['showtime_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ticket_form'] = forms.TicketModelForm(self.request.POST)
            context['client_form'] = forms.ClientModelForm(self.request.POST)
            context['form'] = forms.ReservationModelForm(self.kwargs['showtime_id'], models.Seat.objects.all(),
                                                         self.request.POST)
        else:
            context['client_form'] = forms.ClientModelForm()
            context['ticket_form'] = forms.TicketModelForm()
            context['form'] = forms.ReservationModelForm(self.kwargs['showtime_id'],
                                                         models.Ticket.objects.filter(
                                                             showtime_id=self.kwargs['showtime_id']),
                                                         models.Seat.objects.all())
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['showtime_id'] = self.kwargs['showtime_id']
        kwargs['taken_seats'] = models.Ticket.objects.filter(showtime_id=self.kwargs['showtime_id'])
        kwargs['all_seats'] = models.Seat.objects.all()
        return kwargs


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
    # siedzenia wolne
    seats = models.Seat.objects
    ticket = models.Ticket.objects
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

    ticket_formset = modelformset_factory(models.Ticket,
                                          fields=('seat_id', 'tickettype_id'),
                                          labels={'seat_id': 'Miejsce',
                                                  'tickettype_id': 'Typ Biletu'},
                                          extra=1,
                                          can_delete=True)
    ticket_form = ticket_formset(queryset=models.Ticket.objects.none())
    if request.POST:
        if 'ticket_number' in request.POST:
            ticket_formset = modelformset_factory(models.Ticket,
                                                  fields=('seat_id', 'tickettype_id'),
                                                  labels={'seat_id': 'Miejsce',
                                                          'tickettype_id': 'Typ Biletu'},
                                                  extra=int(request.POST['ticket_select']), can_delete=True)

            ticket_form = ticket_formset(queryset=models.Ticket.objects.none())
        else:
            # https://www.youtube.com/watch?v=FnZgy-y6hGA
            ticket_form = ticket_formset(request.POST)

            r_form = forms.ReservationModelForm(request.POST)
            client_form = forms.ClientModelForm(request.POST)

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
                return redirect(reverse('showtime-details-worker', kwargs={'pk': kwargs['showtime_id']}))

    return render(request, 'worker/rezerwacje/dodaj_rezerwacje.html', context={'showtime_id': showtime_id,
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


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = models.Reservation
    template_name = 'worker/rezerwacje/szczegoly_rezerwacji.html'


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


# bilety
class TicketCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    template_name = 'worker/bilety/dodaj_bilet.html'
    form_class = forms.ReservationTicketModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['reservation_id'] = self.kwargs['reservation_id']
        kwargs['client_id'] = self.kwargs['client_id']
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # context['taken_seats'] = [seat[0] for seat in
        #                           models.Ticket.objects.filter(showtime_id=self.get_object()).values_list('seat_id')]

        context['seats_row_a'] = models.Seat.objects.filter(row_number='A')
        context['seats_row_b'] = models.Seat.objects.filter(row_number='B')
        context['seats_row_c'] = models.Seat.objects.filter(row_number='C')
        context['seats_row_d'] = models.Seat.objects.filter(row_number='D')
        context['seats_row_e'] = models.Seat.objects.filter(row_number='E')
        context['seats_row_f'] = models.Seat.objects.filter(row_number='F')
        context['seats_row_g'] = models.Seat.objects.filter(row_number='G')
        context['seats_row_h'] = models.Seat.objects.filter(row_number='H')
        context['seats_row_i'] = models.Seat.objects.filter(row_number='I')
        context['seats_row_j'] = models.Seat.objects.filter(row_number='J')
        return context
