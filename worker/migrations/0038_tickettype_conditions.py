# Generated by Django 3.0.4 on 2020-03-19 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0037_reservation_confirmation_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettype',
            name='conditions',
            field=models.TextField(null=True),
        ),
    ]
