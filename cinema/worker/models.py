from django.db import models
from django.urls import reverse


class Client(models.Model):
    client_id = models.AutoField(primary_key=True, null=False)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)

    def __str__(self):
        name = str(self.first_name) + ' ' + str(self.last_name)
        return name

    def get_absolute_url(self):
        return reverse('worker:worker-client-details', kwargs={'client_id': self.client_id})


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    release_date = models.IntegerField()
    duration = models.DurationField(null=False)
    description = models.TextField(null=True)
    link = models.CharField(max_length=255, null=True)
    thumbnail = models.CharField(max_length=255, null=True)
    trailer_youtube_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.movie_id) + '. ' + self.title


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    seat_number = models.CharField(null=True, max_length=2)

    def __str__(self):
        return str(self.seat_number)


class Showtime(models.Model):
    showtime_id = models.AutoField(primary_key=True, null=False)
    movie_id = models.ForeignKey(Movie, on_delete=models.PROTECT)
    start_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    show_break = models.DurationField(default=0)
    end_date = models.DateField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        return str(self.movie_id.title) + ' - ' + str(self.start_date) + ' ' + str(self.start_time)


class TicketType(models.Model):
    ticket_id = models.AutoField(primary_key=True, null=False)
    type = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.type


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True, null=False)
    client_id = models.ForeignKey(Client, on_delete=models.PROTECT)
    tickettype_id = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    seat_id = models.ForeignKey(Seat, on_delete=models.PROTECT)
    showtime_id = models.ForeignKey(Showtime, on_delete=models.PROTECT)


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True, null=False)
    client_id = models.ForeignKey(Client, on_delete=models.PROTECT)
    showtime_id = models.ForeignKey(Showtime, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.reservation_id) + ' - ' + str(self.client_id.first_name) + ' ' + str(
            self.client_id.last_name) + ' - ' + str(self.showtime_id.movie_id.title)
