from django.contrib import admin
from .models import *

admin.site.register(Reservation)
admin.site.register(Movie)
admin.site.register(TicketType)
admin.site.register(Client)
admin.site.register(Showtime)
admin.site.register(Seat)
admin.site.register(Ticket)
# admin.site.register(Event)
