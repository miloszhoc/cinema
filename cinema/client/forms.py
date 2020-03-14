from django.forms import *
from django.forms.utils import ErrorList

from worker.models import *


class ReservationModelForm(ModelForm):
    class Meta:
        model = Reservation
        labels = {'showtime_id': '', }
        fields = ['showtime_id', ]

    def __init__(self, *args, **kwargs):
        super(ReservationModelForm, self).__init__(*args, **kwargs)

        # pass initial data to form https://www.geeksforgeeks.org/initial-form-data-django-forms/
        if 'initial' in kwargs:
            self.showtime_id = kwargs['initial']['showtime_id']
            taken_seats = Ticket.objects.filter(showtime_id=self.showtime_id)
            # jesli user zostal przekierowany na ta strone z seansu o id 23,
            # to seans automatycznie podstawia sie w polu bez mozliwosci zmiany
            self.fields['showtime_id'].initial = self.showtime_id

            # https://stackoverflow.com/questions/4662848/disabled-field-is-not-passed-through-workaround-needed
            # jesli pole bylo ustawione jako disabled, to nie wysylalo się w poscie
            self.fields['showtime_id'].widget.attrs['style'] = 'display:none;'

    class Media:
        js = ('js/hover_reservation.js',)


class ClientModelForm(ModelForm):
    class Meta:
        model = Client
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
            'phone_number': 'Numer telefonu'
        }
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class ConfirmReservationForm(Form):
    text_field = CharField(max_length=255, widget=TextInput(attrs={'size': '40', 'hidden': ''}), label='')


class SeatForm(Form):
    seats_row_a = ModelMultipleChoiceField(label='a', queryset=Seat.objects.filter(row_number='A'),
                                           widget=CheckboxSelectMultiple)
    seats_row_b = ModelMultipleChoiceField(label='b', queryset=Seat.objects.filter(row_number='B'),
                                           widget=CheckboxSelectMultiple)
    seats_row_c = ModelMultipleChoiceField(label='c', queryset=Seat.objects.filter(row_number='C'),
                                           widget=CheckboxSelectMultiple)
    seats_row_d = ModelMultipleChoiceField(label='d', queryset=Seat.objects.filter(row_number='D'),
                                           widget=CheckboxSelectMultiple)
    seats_row_e = ModelMultipleChoiceField(label='e', queryset=Seat.objects.filter(row_number='E'),
                                           widget=CheckboxSelectMultiple)
    seats_row_f = ModelMultipleChoiceField(label='f', queryset=Seat.objects.filter(row_number='F'),
                                           widget=CheckboxSelectMultiple)
    seats_row_g = ModelMultipleChoiceField(label='g', queryset=Seat.objects.filter(row_number='G'),
                                           widget=CheckboxSelectMultiple)
    seats_row_h = ModelMultipleChoiceField(label='h', queryset=Seat.objects.filter(row_number='H'),
                                           widget=CheckboxSelectMultiple)
    seats_row_i = ModelMultipleChoiceField(label='i', queryset=Seat.objects.filter(row_number='I'),
                                           widget=CheckboxSelectMultiple)
    seats_row_j = ModelMultipleChoiceField(label='j', queryset=Seat.objects.filter(row_number='J'),
                                           widget=CheckboxSelectMultiple)

    def __init__(self, taken_seats, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
                 error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None,
                 renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)

        self.fields['seats_row_a'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_b'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_c'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_d'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_e'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_f'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_g'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_h'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_i'].initial = (taken_seats.values_list('seat_id', flat=True))
        self.fields['seats_row_j'].initial = (taken_seats.values_list('seat_id', flat=True))
