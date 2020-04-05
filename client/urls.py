from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexMovieListView.as_view(), name='index-client'),
    path('cennik/', views.cennik, name='price-list-client'),
    path('kontakt/', views.kontakt, name='contact-client'),
    path('okinie/', views.okinie, name='about-client'),
    path('repertuar/', views.RepertuarShowtimeListView.as_view(), name='repertoire-list-client'),

    # film
    path('film/<int:pk>', views.FilmMovieDetailView.as_view(), name='movie-details-client'),

    # rezerwacja
    path('rezerwuj-miejsce/<int:showtime_id>', views.reservation_form, name='reservation-form-client'),
    path('bilety/', views.ticket_types_client, name='reservation-tickets-client'),
    path('podsumowanie/', views.summary_client, name='summary-client'),

    # rezerwacje - decyzje
    # https://stackoverflow.com/questions/32950432/django-urls-uuid-not-working
    path('potwierdz/<uuid:id>', views.rezerwacja_potwierdz, name='reservation-accept-client'),
    path('anuluj/<uuid:id>', views.rezerwacja_anuluj, name='reservation-deny-client'),
]
