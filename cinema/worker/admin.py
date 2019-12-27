from django.contrib import admin
from .models import *

admin.site.register(Reservations)
admin.site.register(Movies)
admin.site.register(TicketTypes)
admin.site.register(Clients)
admin.site.register(Showtime)
admin.site.register(Seats)
admin.site.register(Ticket)
