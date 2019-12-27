from django.urls import path
from . import views

# from .views import ClientListView, ClientDetailView, ClientCreateView, MovieListView, ShowtimeListView, \
#     ReservationListView
#
urlpatterns = [
    path('', views.panel),
    # path('clients', ClientListView.as_view(), name='clients-list'),
    # path('movie', MovieListView.as_view(), name='worker-movie-list'),
    # path('client/', ClientListView.as_view(), name='worker-client-list'),
    # path('client/<int:pk>', ClientDetailView.as_view(), name='worker-client-details'),
    # path('client/create', ClientCreateView.as_view(), name='worker-client-create'),
    # path('showtime', ShowtimeListView.as_view(), name='worker-showtime-list'),
    # path('reservation', ReservationListView.as_view(), name='worker-reservation-list'),
]
