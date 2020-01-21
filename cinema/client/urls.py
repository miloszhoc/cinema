from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexMovieListView.as_view(), name='index-client'),
    path('cennik/', views.cennik, name='price-list-client'),
    path('kontakt/', views.kontakt, name='contact-client'),
    path('okinie/', views.okinie, name='about-client'),
    # path('repertuar/', views.repertuar, name='repertoire-client'),
    path('rezerwacja/', views.rezerwacja, name='reservation-client'),

    # detail views
    path('movie/<int:pk>', views.FilmMovieDetailView.as_view(), name='movie-details-client'),
    #     path('', views.MoviesListView.as_view(), name='movie-list'),
    # path('', views.RepertuarListView.as_view(), name='client-showtime-list'),
    path('showtime/<int:pk>', views.RezerwacjaNaSeansShowtimeDetailView.as_view(), name='showtime-details-client'),

    # list views
    path('repertuar/', views.RepertuarShowtimeListView.as_view(), name='repertoire-list-client')
]
