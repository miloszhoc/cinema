from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import FormMixin

from . import models
from .forms import (MovieModelForm,
                    ShowtimeModelForm,
                    TicketTypeModelForm,
                    ReservationModelForm,
                    TicketModelForm,
                    ClientModelForm,
                    ReservationTicketModelForm)
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
    form_class = TicketTypeModelForm
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
    form_class = TicketTypeModelForm
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


# class ReservationCreateView(LoginRequiredMixin, View, FormMixin):
#     model = models.Reservation
#     template_name = 'worker/rezerwacje/dodaj_rezerwacje.html'
#
#     # form_class = ReservationModelForm
#
#     def get(self, request, *args, **kwargs):
#         reservation_form = ReservationModelForm
#         client_form = ClientModelForm
#         return render(request, self.template_name, context={'reservation_form': reservation_form,
#                                                             'client_form': client_form})
#
#         # success_url = reverse('showtime-list-worker')
#
#     # queryset = models.Reservation.objects.all()
#     # @transaction.atomic
#     # def form_valid(self, form):
#     #     client = self.client_form.save()
#     #     form = self.reservation_form.save(commit=False)
#     #     form.client_id = client
#     #     # self.object = form.save(commit=False)
#     #     # self.object.name = showtime
#     #     # self.object.save()
#     #     return super(ReservationCreateView, self).form_valid(form)
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     self.client_form = ClientModelForm
#     # context['client_form'] = ClientModelForm
#     # return context
#
#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs['showtime_id'] = self.kwargs['showtime_id']
#     #     return kwargs
#
#     # jesli wystapi blad, to nic nie zostaje zapisane do bazy
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         reservation_form = ReservationModelForm(showtime_id=self.kwargs['showtime_id'])
#         client_form = ClientModelForm(request.POST)
#         print(self.request.pk)
#         if reservation_form.is_valid() and client_form.is_valid():
#             pass
#             # reservation_form
#             # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#             # reservation = reservation_form.save()
#             # client = client_form.save()
#             # reservation.client_id = client.client_id
#             # client.save()
#             # return super().post(request, *args, **kwargs)
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['showtime_id'] = self.kwargs['showtime_id']
#         return kwargs


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = models.Reservation
    template_name = 'worker/rezerwacje/dodaj_rezerwacje.html'
    form_class = ReservationModelForm

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
            context['client_form'] = ClientModelForm(self.request.POST)
            context['form'] = ReservationModelForm(self.kwargs['showtime_id'], self.request.POST)
        else:
            context['client_form'] = ClientModelForm()
            context['form'] = ReservationModelForm(self.kwargs['showtime_id'])

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['showtime_id'] = self.kwargs['showtime_id']
        return kwargs


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = models.Reservation
    template_name = 'worker/rezerwacje/szczegoly_rezerwacji.html'


# @login_required()
# def new_reservation(request):
#     if request.method == 'POST':
#         reservation_form = ReservationModelForm(request.POST)
#         ticket_form = TicketModelForm(request.POST)
#         if reservation_form.is_valid() and ticket_form.is_valid():
#             reservation = reservation_form.save()
#             ticket = ticket_form.save()
#             reservation.ticket_id = ticket
#             ticket.save()
#             return redirect(reverse('reservation-worker'))
#     else:
#         reservation_form = ReservationModelForm()
#         ticket_form = TicketModelForm()
#         print(request.GET)
#     args = {}
#     args.update(csrf(request))
#     args['reservation_form'] = reservation_form
#     args['ticket_form'] = ticket_form
#     return render(request, 'worker/rezerwacje/dodaj_rezerwacje.html', context=args)
#

pass


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
    form_class = ShowtimeModelForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ShowtimeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Showtime
    template_name = 'worker/seanse/dodaj_seans.html'
    form_class = ShowtimeModelForm

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
    form_class = MovieModelForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Movie
    template_name = 'worker/filmy/dodaj_film.html'
    form_class = MovieModelForm

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
    form_class = ReservationTicketModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['reservation_id'] = self.kwargs['reservation_id']
        kwargs['client_id'] = self.kwargs['client_id']
        print(kwargs)
        return kwargs
