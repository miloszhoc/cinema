from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexMovieListView.as_view(), name='index-client'),
    path('cennik/', views.cennik, name='price-list-client'),
    path('kontakt/', views.kontakt, name='contact-client'),
    path('okinie/', views.okinie, name='about-client'),

    # detail views
    path('movie/<int:pk>', views.FilmMovieDetailView.as_view(), name='movie-details-client'),
    path('rezerwuj-miejsce/<int:showtime_id>', views.reservation_form, name='reservation-form-client'),

    # list views
    path('repertuar/', views.RepertuarShowtimeListView.as_view(), name='repertoire-list-client'),
    # rezerwacje
    # https://stackoverflow.com/questions/32950432/django-urls-uuid-not-working
    path('potwierdz/<uuid:id>', views.rezerwacja_potwierdz, name='reservation-accept-client'),
    path('anuluj/<uuid:id>', views.rezerwacja_anuluj, name='reservation-deny-client'),
    path('podsumowanie/', views.summary_client, name='summary-client'),
]
