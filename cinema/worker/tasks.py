# # https://stackoverflow.com/questions/46816935/how-to-delete-an-object-after-24hrs-since-creation-of-the-same
# # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#beat-custom-schedulers
#
# from celery.schedules import crontab
# from celery.task import periodic_task
# from django.utils import timezone
# from .models import Reservation
#
#
# # usuwa niepotwierdzone rezerwacje, czyli te, ktore nie maja w bazie ustawionej flagi confirmed jako true
# @periodic_task(run_every=crontab(minute='*/10'))
# def delete_unconfirmed_reservation():
#     all_reservations = Reservation.objects.all()
#
#     for reservation in all_reservations:
#         if reservation.reservation_date < timezone.now() and not reservation.confirmed:
#             reservation.delete()
#     return 'Successfully deleted at {}'.format(timezone.now())
