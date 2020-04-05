from django.contrib import messages
from django.core.mail import send_mail
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
from cinema.settings import EMAIL_HOST_USER
from django.template import loader
from django.utils import timezone
from django.http import JsonResponse


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


# typy biletów
class TicketTypeListView(LoginRequiredMixin, ListView):
    queryset = models.TicketType.objects.filter(deleted=False)
    model = models.TicketType
    template_name = 'worker/typy_biletow/typy_lista.html'
    paginate_by = 10
    # sortowanie asc po id, czyli wg kolejnosci dodania
    ordering = ['ticket_id']


# lista archiwalnych seansow
class TicketTypeArchiveListView(LoginRequiredMixin, ListView):
    queryset = models.TicketType.objects.filter(deleted=True)
    model = models.TicketType
    paginate_by = 10
    ordering = ['ticket_id']
    template_name = 'worker/typy_biletow/typy_lista.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['deleted_list'] = True  # do oznaczenie, czy lista zawiera usuniete typy biletów
        return context


class TicketTypeCreateView(LoginRequiredMixin, CreateView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/dodaj_typ.html'
    form_class = forms.TicketTypeModelForm
    success_url = reverse_lazy('tickettype-list-worker')


class TicketTypeDetailView(LoginRequiredMixin, DetailView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/szczegoly_typu.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        # zwraca true jesli istnieje typ biletu powiazany z biletem
        # potrzebne do usuwania - calkowicie usuwac mozna tylko typy biletow,
        # ktore nie sa powiazane z zadnym biletem
        # jesli typ biletu jest powiazany z biletem, to nie mozna go usunac, tylko oznaczyc jako usuniety
        # oznaczyć może tylko administrator, oznaczonego typu biletu klient nie może wyrabrać podczas rezerwacji miejsc
        context['tickettype_exists'] = models.Ticket.objects.filter(tickettype_id=self.object).exists()
        return context


class TicketTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/dodaj_typ.html'
    form_class = forms.TicketTypeModelForm
    success_url = reverse_lazy('tickettype-list-worker')

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.TicketType, ticket_id=id_)


class TicketTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/usun_typ.html'
    success_url = reverse_lazy('tickettype-list-worker')


# rezerwacje
@login_required
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

            return redirect('reservation-tickets-worker')

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


@login_required
def ticket_types_worker(request, **kwargs):
    if 'data' in request.session:
        taken = request.session.get('taken')
        data = request.session.get('data')
        showtime_id = data['showtime_id']

        paid = data['paid'] if data.get('paid') else ''
        confirmed = data['confirmed'] if data.get('confirmed') else ''
        confirmation_email = data['confirmation_email'] if data.get('confirmation_email') else ''

        reservation_initial = {'showtime_id': data['showtime_id'],
                               'confirmed': confirmed,
                               'paid': paid,
                               'confirmation_email': confirmation_email}

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

        r_form.fields['confirmed'].widget = r_form.fields['confirmed'].hidden_widget()
        r_form.fields['paid'].widget = r_form.fields['paid'].hidden_widget()
        r_form.fields['confirmation_email'].widget = r_form.fields['confirmation_email'].hidden_widget()

        ticket_formset = modelformset_factory(models.Ticket,
                                              fields=('seat_id', 'tickettype_id'),
                                              labels={'seat_id': '',
                                                      'tickettype_id': 'Typ Biletu'},
                                              extra=len(taken),
                                              widgets={'seat_id': django.forms.Select(attrs={'hidden': ''})},
                                              max_num=60)  # pracownik moze zarezerwowac cala sale

        ticket_form = ticket_formset(queryset=models.Ticket.objects.none(), initial=[{'seat_id': z} for z in taken])

        # pokazuje tylko typy biletów, które nie są usunięte
        # https://simpleisbetterthancomplex.com/questions/2017/03/22/how-to-dynamically-filter-modelchoices-queryset-in-a-modelform.html
        for form in ticket_form:
            form.fields['tickettype_id'].queryset = models.TicketType.objects.filter(deleted=False)

        if request.POST:
            r_form = forms.ReservationModelForm(request.POST)
            client_form = forms.ClientModelForm(request.POST)
            ticket_form = ticket_formset(request.POST)

            # pokazuje tylko typy biletów, które nie są usunięte
            for form in ticket_form:
                form.fields['tickettype_id'].queryset = models.TicketType.objects.filter(deleted=False)

            if ticket_form.is_valid() and (client_form.is_valid() and r_form.is_valid()):
                request.session['formset_data'] = ticket_form.data

                return redirect('summary-worker')

            client_form.fields['first_name'].widget = client_form.fields['first_name'].hidden_widget()
            client_form.fields['last_name'].widget = client_form.fields['last_name'].hidden_widget()
            client_form.fields['email'].widget = client_form.fields['email'].hidden_widget()
            client_form.fields['phone_number'].widget = client_form.fields['phone_number'].hidden_widget()

            r_form.fields['showtime_id'].widget = r_form.fields['showtime_id'].hidden_widget()
            r_form.fields['confirmed'].widget = r_form.fields['confirmed'].hidden_widget()
            r_form.fields['paid'].widget = r_form.fields['paid'].hidden_widget()
            r_form.fields['confirmation_email'].widget = r_form.fields['confirmation_email'].hidden_widget()

        return render(request, 'worker/rezerwacje/wybierz_typy_biletow.html', context={'taken': taken,
                                                                                       'ticket_form': ticket_form,
                                                                                       'reservation_form': r_form,
                                                                                       'client_form': client_form,
                                                                                       'client_initial': client_initial,
                                                                                       'reservation_initial': reservation_initial,
                                                                                       'showtime': showtime})
    else:
        taken = ''
        ticket_form = ''
        r_form = ''
        client_form = ''
        reservation_initial = ''
        client_initial = ''
        showtime = ''
        return render(request, 'worker/rezerwacje/wybierz_typy_biletow.html', context={'taken': taken,
                                                                                       'ticket_form': ticket_form,
                                                                                       'reservation_form': r_form,
                                                                                       'client_form': client_form,
                                                                                       'client_initial': client_initial,
                                                                                       'reservation_initial': reservation_initial,
                                                                                       'showtime': showtime})


# pracownik moze zarezerwowac dowolna ilosc biletow
@transaction.atomic
@login_required
def summary(request, **kwargs):
    if 'formset_data' in request.session:
        formset_data = request.session['formset_data']

        # wyliczanie koncowej ceny do wyswietlenia userowi
        total_price = 0
        for k, v in formset_data.items():
            if k.endswith('tickettype_id'):
                total_price += models.TicketType.objects.get(ticket_id=v).price

        taken = request.session.get('taken')
        data = request.session.get('data')
        showtime_id = data['showtime_id']

        paid = data['paid'] if data.get('paid') else ''
        confirmed = data['confirmed'] if data.get('confirmed') else ''
        confirmation_email = data['confirmation_email'] if data.get('confirmation_email') else ''

        reservation_initial = {'showtime_id': data['showtime_id'],
                               'confirmed': confirmed,
                               'paid': paid,
                               'confirmation_email': confirmation_email}

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

        r_form.fields['confirmed'].widget = r_form.fields['confirmed'].hidden_widget()
        r_form.fields['paid'].widget = r_form.fields['paid'].hidden_widget()
        r_form.fields['confirmation_email'].widget = r_form.fields['confirmation_email'].hidden_widget()

        ticket_formset = modelformset_factory(models.Ticket,
                                              fields=('seat_id', 'tickettype_id'),
                                              labels={'seat_id': '',
                                                      'tickettype_id': ''},
                                              extra=len(taken),
                                              widgets={'seat_id': django.forms.Select(attrs={'hidden': '', }),
                                                       'tickettype_id': django.forms.Select(attrs={'hidden': '', })},
                                              max_num=60)  # pracownik moze zarezerwowac cala sale

        ticket_form = ticket_formset(queryset=models.Ticket.objects.none(), data=formset_data)

        db_ticket_types = models.TicketType.objects.all()

        if request.POST:
            r_form = forms.ReservationModelForm(request.POST)
            client_form = forms.ClientModelForm(request.POST)
            ticket_form = ticket_formset(request.POST)

            if ticket_form.is_valid() and (client_form.is_valid() and r_form.is_valid()):
                showtime = models.Showtime.objects.get(showtime_id=showtime_id)  # obiekt seansu
                client = client_form.save()
                reservation = r_form.save(commit=False)
                reservation.client_id = client

                # https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/#many-to-many-relationships
                instances = ticket_form.save(commit=False)

                # get total price
                # zapisuje cene biletu, aby w przy zmiane cennika ceny juz zakupionych biletow pozostaly takie same
                total_price = 0
                for instance in instances:
                    price = models.TicketType.objects.get(ticket_id=instance.tickettype_id_id).price
                    total_price += price
                    instance.price = price

                reservation.cost = total_price
                reservation.save()

                for instance in instances:
                    instance.client_id = client
                    instance.showtime_id = showtime
                    instance.save()
                    reservation.ticket_id.add(instance)

                r_form.save_m2m()
                # https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
                # https://stackoverflow.com/questions/29466796/sending-a-html-email-in-django
                if reservation.confirmation_email and not reservation.confirmed:
                    html_mail = loader.render_to_string(template_name='client/rezerwacja/email.html',
                                                        context={'first_name': client.first_name,
                                                                 'last_name': client.last_name,
                                                                 'reservation': reservation,
                                                                 'domain': request.META['HTTP_HOST']})

                    mail = send_mail(subject='Potwierdzenie rezerwacji',
                                     message='',
                                     from_email=EMAIL_HOST_USER,
                                     recipient_list=[client.email, ],
                                     fail_silently=True,
                                     html_message=html_mail)
                    if mail:
                        messages.add_message(request, messages.SUCCESS,
                                             'Rezerwacja została pomyślnie utworzona, na adres'
                                             'mailowy klienta została wysłana wiadomość z potwierdzeniem.'
                                             'Jeśli klient nie potwierdzi rezerwacji w ciągu 30 minut, '
                                             'to zostanie ona usunięta z systemu')
                    else:
                        confirm_url = request.META['HTTP_HOST'] + reverse('reservation-accept-client',
                                                                          kwargs={'id': str(
                                                                              reservation.reservation_confirmation_code)})
                        reject_url = request.META['HTTP_HOST'] + reverse('reservation-deny-client',
                                                                         kwargs={'id': str(
                                                                             reservation.reservation_confirmation_code)})

                        messages.add_message(request,
                                             messages.ERROR,
                                             'Wystąpił problem z wysłaniem wiadomości. Prosimy o ręczne potwierdzenie rezerwacji pod linkiem: \n'
                                             + confirm_url + '\nW celu odzucenia rezerwacji prosimy przejść pod adres\n' + reject_url)
                else:
                    messages.add_message(request, messages.SUCCESS,
                                         'Rezerwacja została pomyślnie zakutalizowana! \n'
                                         'Uwaga! Nie została zaznaczona opcja wysyłki wiadomości email do klienta.')
                request.session.pop('taken')
                request.session.pop('data')
                request.session.pop('formset_data')
                return redirect(reverse('showtime-details-worker', kwargs={'pk': showtime_id}))

        return render(request, 'worker/rezerwacje/podsumowanie.html', context={'taken': taken,
                                                                               'ticket_form': ticket_form,
                                                                               'reservation_form': r_form,
                                                                               'client_form': client_form,
                                                                               'client_initial': client_initial,
                                                                               'reservation_initial': reservation_initial,
                                                                               'showtime': showtime,
                                                                               'total': total_price,
                                                                               'db_ticket_types': db_ticket_types})
    else:
        taken = ''
        ticket_form = ''
        r_form = ''
        client_form = ''
        reservation_initial = ''
        client_initial = ''
        showtime = ''
        total_price = ''
        return render(request, 'worker/rezerwacje/podsumowanie.html', context={'taken': taken,
                                                                               'ticket_form': ticket_form,
                                                                               'reservation_form': r_form,
                                                                               'client_form': client_form,
                                                                               'client_initial': client_initial,
                                                                               'reservation_initial': reservation_initial,
                                                                               'showtime': showtime,
                                                                               'total': total_price})


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

    # pokazuje tylko typy biletów, które nie są usunięte
    for form in ticket_form:
        form.fields['tickettype_id'].queryset = models.TicketType.objects.filter(deleted=False)

    if request.POST:
        if 'ticket_num' in request.POST:
            ticket_formset = modelformset_factory(models.Ticket,
                                                  fields=('seat_id', 'tickettype_id'),
                                                  labels={'seat_id': 'Miejsce',
                                                          'tickettype_id': 'Typ Biletu', },
                                                  extra=int(request.POST['ticket_select']),
                                                  max_num=60, can_delete=True)

            ticket_form = ticket_formset(queryset=models.Ticket.objects.none(), initial=tickets_initial)

            # pokazuje tylko typy biletów, które nie są usunięte
            for form in ticket_form:
                form.fields['tickettype_id'].queryset = models.TicketType.objects.filter(deleted=False)
        else:
            # current objects
            reservation_object = get_object_or_404(models.Reservation, reservation_id=reservation_id)
            client_object = get_object_or_404(models.Client, client_id=reservation.client_id.client_id)

            r_form = forms.ReservationModelForm(request.POST, instance=reservation_object)
            r_form.fields['showtime_id'].widget = r_form.fields['showtime_id'].hidden_widget()

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
                # zapisuje cene biletu, aby w przy zmiane cennika ceny juz zakupionych biletow pozostaly takie same
                total_price = 0
                for instance in instances:
                    price = models.TicketType.objects.get(ticket_id=instance.tickettype_id_id).price
                    total_price += price
                    instance.price = price

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

                # https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
                # https://stackoverflow.com/questions/29466796/sending-a-html-email-in-django
                if reservation.confirmation_email and not reservation.confirmed:
                    html_mail = loader.render_to_string(template_name='client/rezerwacja/email.html',
                                                        context={'first_name': client.first_name,
                                                                 'last_name': client.last_name,
                                                                 'reservation': reservation,
                                                                 'domain': request.META['HTTP_HOST']})

                    mail = send_mail(subject='Potwierdzenie rezerwacji',
                                     message='',
                                     from_email=EMAIL_HOST_USER,
                                     recipient_list=[client.email, ],
                                     fail_silently=True,
                                     html_message=html_mail)
                    if mail:
                        messages.add_message(request, messages.SUCCESS,
                                             'Rezerwacja została pomyślnie utworzona, na adres'
                                             'mailowy klienta została wysłana wiadomość z potwierdzeniem.'
                                             'Jeśli klient nie potwierdzi rezerwacji w ciągu 30 minut, '
                                             'to zostanie ona usunięta z systemu')
                    else:
                        confirm_url = request.META['HTTP_HOST'] + reverse('reservation-accept-client',
                                                                          kwargs={'id': str(
                                                                              reservation.reservation_confirmation_code)})
                        reject_url = request.META['HTTP_HOST'] + reverse('reservation-deny-client',
                                                                         kwargs={'id': str(
                                                                             reservation.reservation_confirmation_code)})

                        messages.add_message(request,
                                             messages.ERROR,
                                             'Wystąpił problem z wysłaniem wiadomości. Prosimy o ręczne potwierdzenie rezerwacji pod linkiem: \n'
                                             + confirm_url + '\nW celu odzucenia rezerwacji prosimy przejść pod adres\n' + reject_url)
                else:
                    messages.add_message(request, messages.SUCCESS,
                                         'Rezerwacja została pomyślnie zakutalizowana! \n'
                                         'Uwaga! Nie została zaznaczona opcja wysyłki wiadomości email do klienta.')
                return redirect(reverse('showtime-details-worker', kwargs={'pk': str(showtime.showtime_id)}))

    return render(request, 'worker/rezerwacje/edytuj-rezerwacje.html', context={'reservation': reservation,
                                                                                'r_form': r_form,
                                                                                'client_form': client_form,
                                                                                'ticket_form': ticket_form,
                                                                                'ticket_number': [x for x in
                                                                                                  range(1, 61)], })


class ReservationConfirmPay(LoginRequiredMixin, UpdateView):
    model = models.Reservation
    template_name = 'worker/rezerwacje/potwierdz_oplac_rezerwacje.html'
    form_class = forms.PayForReservationForm

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.Reservation, reservation_id=id_)

    def get_success_url(self):
        showtime = self.get_object().showtime_id.showtime_id
        return reverse('showtime-details-worker', kwargs={'pk': showtime})


@login_required
@transaction.atomic
def reservation_delete(request, **kwargs):
    reservation_id = kwargs['reservation_id']
    reservation = models.Reservation.objects.get(reservation_id=reservation_id)
    form = forms.DeleteReservationForm(initial={'text_field': reservation_id})
    if request.POST:
        form = forms.DeleteReservationForm(request.POST, initial={'text_field': reservation_id})

        if form.is_valid() and get_object_or_404(models.Reservation, reservation_id=reservation_id):
            reservation = models.Reservation.objects.get(reservation_id=reservation_id)
            tickets = models.Ticket.objects.filter(reservation__reservation_id=reservation_id)
            # usuwa wszytkie bilety powiązane z rezerwacją, oraz rezerwację
            for t in tickets.iterator():
                t.delete()
            reservation.delete()

            models.Client.objects.get(client_id=reservation.client_id.client_id).delete()

            messages.add_message(request, messages.SUCCESS, 'Rezerwacja została pomyślnie usunięta.')
            return redirect(reverse('showtime-details-worker', kwargs={'pk': str(reservation.showtime_id.showtime_id)}))
        else:
            # https://www.kodefork.com/questions/30/how-to-pass-a-message-when-we-redirect-to-some-template-from-django-views/
            messages.add_message(request, messages.ERROR, 'Nie można usunąć!')
    return render(request, 'worker/rezerwacje/usun_rezerwacje.html', context={'reservation_id': reservation_id,
                                                                              'form': form,
                                                                              'reservation': reservation})


# seanse
# lista seansow ktore sie odbeda
class ShowtimeListView(LoginRequiredMixin, ListView):
    queryset = models.Showtime.objects.filter(start_date__gte=timezone.now())
    model = models.Showtime
    paginate_by = 10
    ordering = ['start_date']
    template_name = 'worker/seanse/seans_lista.html'


# lista archiwalnych seansow
class ShowtimeArchiveListView(LoginRequiredMixin, ListView):
    queryset = models.Showtime.objects.filter(start_date__lte=timezone.now())
    model = models.Showtime
    paginate_by = 10
    ordering = ['-showtime_id']
    template_name = 'worker/seanse/seans_lista.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['deleted_list'] = True  # do oznaczenie, czy lista zawiera usuniete filmy
        return context


class ShowtimeDetailView(LoginRequiredMixin, DetailView):
    model = models.Showtime
    template_name = 'worker/seanse/szczegoly_seansu.html'

    # w templatce polazuje tylko rezerwacje na konkretny seans + bilety, ktore byly zakupione w ramach rezerwacji
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = models.Reservation.objects.filter(showtime_id=self.get_object())
        context['tickets'] = models.Ticket.objects.filter(showtime_id=self.get_object())
        context['time_now'] = timezone.now()
        return context


class ShowtimeCreateView(LoginRequiredMixin, CreateView):
    model = models.Showtime
    template_name = 'worker/seanse/dodaj_seans.html'
    form_class = forms.ShowtimeModelForm


class ShowtimeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Showtime
    template_name = 'worker/seanse/dodaj_seans.html'
    form_class = forms.ShowtimeModelForm

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.Showtime, showtime_id=id_)


class ShowtimeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Showtime
    template_name = 'worker/seanse/usun_seans.html'
    success_url = reverse_lazy('showtime-list-worker')


# filmy
class MovieListView(LoginRequiredMixin, ListView):
    queryset = models.Movie.objects.filter(deleted=False)
    model = models.Movie
    template_name = 'worker/filmy/lista_filmow.html'
    paginate_by = 10
    # sortowanie asc po id, czyli wg kolejnosci dodania
    ordering = ['-movie_id']


class MovieDeletedListView(LoginRequiredMixin, ListView):
    queryset = models.Movie.objects.filter(deleted=True)
    model = models.Movie
    template_name = 'worker/filmy/lista_filmow.html'
    paginate_by = 10
    # sortowanie asc po id, czyli wg kolejnosci dodania
    ordering = ['-movie_id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['deleted_list'] = True  # do oznaczenie, czy lista zawiera usuniete filmy
        return context


class MovieDetailView(LoginRequiredMixin, DetailView):
    model = models.Movie
    template_name = 'worker/filmy/szczegoly_filmu.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        # zwraca true jesli istnieje seans powiazany z filmem
        # potrzebne do usuwania - calkowicie usuwac mozna tylko filmy,
        # ktore nie sa powiazane z zadnym seansem
        # jesli film jest powiazany z seansem, to nie mozna go usunac, tylko oznaczyc jako usuniety
        # oznaczyć może tylko administrator, z tak oznaczonego filmu nie można utworzyć seansu
        context['showtime'] = models.Showtime.objects.filter(movie_id=self.object).exists()
        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = models.Movie
    template_name = 'worker/filmy/dodaj_film.html'
    form_class = forms.MovieModelForm


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Movie
    template_name = 'worker/filmy/dodaj_film.html'
    form_class = forms.MovieModelForm

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.Movie, movie_id=id_)


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Movie
    template_name = 'worker/filmy/usun_film.html'
    success_url = reverse_lazy('movie-list-worker')


# usuwa niepotwierdzone rezerwacje, czyli te, ktore nie maja w bazie ustawionej flagi confirmed jako true
# pobiera wszystkie rezerwacje z ostatnich 10min, sprawdza, czy rezerwacje są potwierdzone, jeśli nie są,
# to usuwa wszystkie bilety powiązane z rezerwacją, dane klienta, a takze samą rezerwację,
# wysyła maila z informacją o usunięciu rezerwacji
@transaction.atomic
def delete_unconfirmed_reservation(request):
    errors = []
    clients = []
    now = timezone.now()
    reservation_counter = 0
    ticket_counter = 0

    ten_minutes = now - timezone.timedelta(minutes=10)
    expired_reservations = models.Reservation.objects.filter(reservation_expire__gte=ten_minutes)

    for reservation in expired_reservations:
        if reservation.reservation_expire < now and not reservation.confirmed:
            tickets = models.Ticket.objects.filter(reservation__reservation_id=reservation.reservation_id)
            # usuwa wszytkie bilety powiązane z rezerwacją
            for t in tickets.iterator():
                ticket_counter += 1
                t.delete()
            reservation.delete()  # usuwa rezerwacje

            client = models.Client.objects.get(client_id=reservation.client_id.client_id)

            clients.append(client)

            reservation_counter += 1

            client.delete()  # usuwa dane klienta
    if clients:
        html_mail = loader.render_to_string(template_name='worker/maile/auto_usuwanie_rezerwacji.html')

        mail = send_mail(subject='Usunięta rezerwacja',
                         message='',
                         from_email=EMAIL_HOST_USER,
                         recipient_list=[client.email for client in clients],
                         fail_silently=True,
                         html_message=html_mail)
        if not mail:
            errors.append("can't send email")

    return JsonResponse(data={'deleted_reservations': reservation_counter,
                              'deleted_tickets': ticket_counter,
                              'errors': errors})
