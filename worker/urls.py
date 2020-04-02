from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    # strona logowania i wylogowania
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('', views.main, name='main'),
    path('panel/', views.panel, name='panel'),

    # typy biletów
    path('typy-biletow/', views.TicketTypeListView.as_view(), name='tickettype-list-worker'),
    path('typy-biletow/usuniete/', views.TicketTypeArchiveListView.as_view(), name='tickettype-deleted-list-worker'),
    path('szczegoly-typu/<int:pk>', views.TicketTypeDetailView.as_view(), name='tickettype-details-worker'),
    path('dodaj-typ/', views.TicketTypeCreateView.as_view(), name='tickettype-create-worker'),
    path('<int:pk>/aktualizuj-typ/', views.TicketTypeUpdateView.as_view(), name='tickettype-update-worker'),
    path('<int:pk>/usun-typ/', views.TicketTypeDeleteView.as_view(), name='tickettype-delete-worker'),

    # filmy
    path('filmy/', views.MovieListView.as_view(), name='movie-list-worker'),
    path('filmy/usuniete/', views.MovieDeletedListView.as_view(), name='movie-deleted-list-worker'),
    path('szczegoly-filmu/<int:pk>', views.MovieDetailView.as_view(), name='movie-details-worker'),
    path('dodaj-film/', views.MovieCreateView.as_view(), name='movie-create-worker'),
    path('<int:pk>/aktualizuj-film/', views.MovieUpdateView.as_view(), name='movie-update-worker'),
    path('<int:pk>/usun-film/', views.MovieDeleteView.as_view(), name='movie-delete-worker'),

    # seanse
    path('seanse/', views.ShowtimeListView.as_view(), name='showtime-list-worker'),
    path('seanse/archiwalne/', views.ShowtimeArchiveListView.as_view(), name='showtime-archive-list-worker'),
    path('szczegoly-seansu/<int:pk>', views.ShowtimeDetailView.as_view(), name='showtime-details-worker'),
    path('dodaj-seans/', views.ShowtimeCreateView.as_view(), name='showtime-create-worker'),
    path('<int:pk>/aktualizuj-seans/', views.ShowtimeUpdateView.as_view(), name='showtime-update-worker'),
    path('<int:pk>/usun-seans/', views.ShowtimeDeleteView.as_view(), name='showtime-delete-worker'),

    # rezerwacje
    path('usun-rezerwacje/<int:reservation_id>', views.reservation_delete, name='reservation-delete-worker'),
    path('dodaj-rezerwacje/<int:showtime_id>', views.reservation_form, name='reservation-form-worker'),
    path('edytuj-rezerwacje/<int:reservation_id>', views.reservation_update, name='reservation-update-worker'),
    path('potwierdz/<int:pk>', views.ReservationConfirmPay.as_view(), name='reservation-confirm-pay-worker'),
    path('bilety/', views.ticket_types_worker, name='reservation-tickets-worker'),
    path('podsumowanie/', views.summary, name='summary-worker'),
    path('cron/usun-rezerwacje', views.delete_unconfirmed_reservation, name='delete-reservations-worker'),
]
