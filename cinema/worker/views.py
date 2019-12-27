from django.shortcuts import render
from django.db import connection


# Create your views here.
def panel(request):
    return render(request, 'worker/panel.html', context={})
