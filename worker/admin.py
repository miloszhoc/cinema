from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

admin.site.site_header = 'Zarządzanie użytkownikami'
admin.site.site_title = 'Grupy i użytkownicy'
# admin.site.register(Reservation)
# admin.site.register(Movie)
# admin.site.register(TicketType)
# admin.site.register(Client)
# admin.site.register(Showtime)
# admin.site.register(Seat)
# admin.site.register(Ticket)
# admin.site.register(Event)
admin.site.unregister(Group)
