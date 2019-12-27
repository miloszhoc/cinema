from django.db import models
from django.urls import reverse


class Clients(models.Model):
    client_id = models.AutoField(primary_key=True, null=False)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)

    def __str__(self):
        name = str(self.first_name) + ' ' + str(self.last_name)
        return name

    def get_absolute_url(self):
        return reverse('worker:worker-client-details', kwargs={'client_id': self.client_id})


class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True, null=False)
    movie_title = models.CharField(max_length=255)
    movie_director = models.CharField(max_length=255)
    release_date = models.IntegerField()
    duration = models.DurationField(null=False)
    description = models.TextField(null=True)
    link = models.CharField(max_length=255, null=True)
    thumbnail = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.movie_title


class Seats(models.Model):
    seat_id = models.AutoField(primary_key=True)
    seat_number = models.IntegerField(null=True)

    def __str__(self):
        return str(self.seat_number)


class Showtime(models.Model):
    showtime_id = models.AutoField(primary_key=True, null=False)
    movie_id = models.ForeignKey(Movies, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    show_break = models.DurationField(default=0)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.showtime_id)


class TicketTypes(models.Model):
    ticket_id = models.AutoField(primary_key=True, null=False)
    type = models.CharField(max_length=40)
    price = models.IntegerField()

    def __str__(self):
        return self.type


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True, null=False)
    client_id = models.ForeignKey(Clients, on_delete=models.PROTECT)
    tickettype_id = models.ForeignKey(TicketTypes, on_delete=models.PROTECT)
    seat_id = models.ForeignKey(Seats, on_delete=models.PROTECT)


class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True, null=False)
    # client_id = models.ForeignKey(Clients, on_delete=models.ValueRange)  # do not delete client data
    ticket_id = models.ForeignKey(Ticket, on_delete=models.PROTECT)  # do not delete ticket type
    showtime_id = models.ForeignKey(Showtime, on_delete=models.PROTECT)  # do not delete showtime
    # seat_id = models.ForeignKey(Seats, on_delete=models.PROTECT)  # do not delete seat

    def __str__(self):
        return str(self.reservation_id)
