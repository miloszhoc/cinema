from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    # strona logowania i wylogowania
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('', views.main, name='main'),
    path('panel/', views.panel, name='panel'),
    path('rezerwacje/', views.ReservationListView.as_view(), name='reservation-worker'),

    # filmy
    path('filmy/', views.MovieListView.as_view(), name='movie-list-worker'),
    path('szczegoly-filmu/<int:pk>', views.MovieDetailView.as_view(), name='movie-details-worker'),
    path('dodaj-film/', views.MovieCreateView.as_view(), name='movie-create-worker'),
    path('<int:pk>/aktualizuj-film/', views.MovieUpdateView.as_view(), name='movie-update-worker'),
    path('<int:pk>/usun-film/', views.MovieDeleteView.as_view(), name='movie-delete-worker'),

    # seanse
    path('seanse/', views.ShowtimeListView.as_view(), name='showtime-list-worker'),
    path('szczegoly-seansu/<int:pk>', views.ShowtimeDetailView.as_view(), name='showtime-details-worker'),
    path('dodaj-seans/', views.ShowtimeCreateView.as_view(), name='showtime-create-worker'),
    path('<int:pk>/aktualizuj-seans/', views.ShowtimeUpdateView.as_view(), name='showtime-update-worker'),
    path('<int:pk>/usun-seans/', views.ShowtimeDeleteView.as_view(), name='showtime-delete-worker'),

    # rezerwacje
    path('dodaj-rezerwacje/', views.ReservationCreateView.as_view(), name='reservations-create-worker')
    # path('reservation', ReservationListView.as_view(), name='worker-reservation-list'),
]
