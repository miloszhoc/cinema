from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    # strona logowania i wylogowania
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('dodaj-uzytkownika', views.add_user, name='adduser-create-worker'),

    path('', views.main, name='main'),
    path('panel/', views.panel, name='panel'),
    path('rezerwacje/', views.ReservationListView.as_view(), name='reservation-worker'),

    # typy biletów
    path('typy-biletow/', views.TicketTypeListView.as_view(), name='tickettype-list-worker'),
    path('szczegoly-typu/<int:pk>', views.TicketTypeDetailView.as_view(), name='tickettype-details-worker'),
    path('dodaj-typ/', views.TicketTypeCreateView.as_view(), name='tickettype-create-worker'),
    path('<int:pk>/aktualizuj-typ/', views.TicketTypeUpdateView.as_view(), name='tickettype-update-worker'),
    path('<int:pk>/usun-typ/', views.TicketTypeDeleteView.as_view(), name='tickettype-delete-worker'),

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
    path('dodaj-rezerwacje/<int:showtime_id>', views.ReservationCreateView.as_view(),
         name='reservations-create-worker'),
    path('szczegoly-rezerwacji/<int:pk>', views.ReservationDetailView.as_view(),
         name='reservation-details-worker'),

    # bliety
    path('dodaj-bilet/<int:reservation_id>/<int:client_id>', views.TicketCreateView.as_view(),
         name='ticket-create-worker')
    # path(''),
]
