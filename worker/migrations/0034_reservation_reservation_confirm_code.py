# Generated by Django 3.0.1 on 2020-03-08 20:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0033_auto_20200308_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservation_confirm_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]