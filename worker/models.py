import uuid
from django.db import models
from django.urls import reverse
import datetime
from django.utils import timezone
from PIL import Image


class Client(models.Model):
    client_id = models.AutoField(primary_key=True, null=False)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True)

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
    link = models.URLField(max_length=255, null=True)
    thumbnail = models.ImageField(default='', upload_to='images', max_length=255)
    trailer_youtube_id = models.CharField(max_length=255, null=True)
    deleted = models.BooleanField(default=False)

    # adres pod który zostaniemy przekierowani po dodaniu filmu do bazy (klasa MovieCreateView)
    # w tym przypadku przenosi nas do szczegolow dodanego filmu
    def get_absolute_url(self):
        return reverse('movie-details-worker', kwargs={'pk': self.movie_id})

    def __str__(self):
        return self.title


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    seat_number = models.IntegerField(null=True)
    row_number = models.CharField(null=True, max_length=1)

    def __str__(self):
        return str(self.row_number) + '' + str(self.seat_number)


class Showtime(models.Model):
    showtime_id = models.AutoField(primary_key=True, null=False)
    movie_id = models.ForeignKey(Movie, on_delete=models.PROTECT)
    start_date = models.DateTimeField(null=True)
    show_break = models.DurationField(default=0)
    end_date = models.DateTimeField(null=True, editable=False)

    # nadpisana metoda zapisu, ktora na podstawie trwania filmu okresla czas jego zakonczenia + przerwa po seansie
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.end_date = self.start_date + datetime.timedelta(
            seconds=self.movie_id.duration.seconds) + datetime.timedelta(
            seconds=self.show_break.seconds)
        super(Showtime, self).save()

    # adres pod który zostaniemy przekierowani po dodaniu seansu do bazy (klasa ShowtimeCreateView)
    # w tym przypadku przenosi nas do szczegolow dodanego seansu
    def get_absolute_url(self):
        return reverse('showtime-details-worker', kwargs={'pk': self.showtime_id})

    def __str__(self):
        return str(self.movie_id.title) + ' - ' + str(self.start_date)


class TicketType(models.Model):
    ticket_id = models.AutoField(primary_key=True, null=False)
    type = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    conditions = models.TextField(null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.type


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True, null=False)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    tickettype_id = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    seat_id = models.ForeignKey(Seat, on_delete=models.PROTECT)
    showtime_id = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return str(self.ticket_id) + '. ' + self.client_id.first_name + \
               ' ' + self.client_id.last_name + ' - ' + self.showtime_id.movie_id.title + ' - ' \
               + str(self.showtime_id.start_date)


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True, null=False)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    showtime_id = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paid = models.BooleanField(default=False)
    ticket_id = models.ManyToManyField(Ticket)
    reservation_date = models.DateTimeField(null=True)
    reservation_expire = models.DateTimeField(null=True)
    confirmed = models.BooleanField(default=False)
    # https://stackoverflow.com/questions/16925129/generate-unique-id-in-django-from-a-model-field
    reservation_confirmation_code = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    confirmation_email = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('reservation-details-worker', kwargs={'pk': self.reservation_id})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.reservation_date = timezone.now()
        self.reservation_expire = self.reservation_date + timezone.timedelta(minutes=30)  # rezerwacja wygasa po 30min
        return super(Reservation, self).save()

    def __str__(self):
        return str(self.reservation_id) + '. ' + str(self.client_id.first_name) + ' ' + str(
            self.client_id.last_name) + ' - ' + str(self.showtime_id.movie_id.title) + ' - ' \
               + str(self.showtime_id.start_date)
