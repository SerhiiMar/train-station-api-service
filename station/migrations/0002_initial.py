# Generated by Django 5.0.6 on 2024-06-11 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("station", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="route",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="routes_as_destination",
                to="station.station",
            ),
        ),
        migrations.AddField(
            model_name="route",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="routes_as_source",
                to="station.station",
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="station.order",
            ),
        ),
        migrations.AddField(
            model_name="train",
            name="train_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trains",
                to="station.traintype",
            ),
        ),
        migrations.AddField(
            model_name="trip",
            name="crew",
            field=models.ManyToManyField(related_name="trip", to="station.crew"),
        ),
        migrations.AddField(
            model_name="trip",
            name="route",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trips",
                to="station.route",
            ),
        ),
        migrations.AddField(
            model_name="trip",
            name="train",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trips",
                to="station.train",
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="trip",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="station.trip",
            ),
        ),
        migrations.AddConstraint(
            model_name="route",
            constraint=models.UniqueConstraint(
                fields=("source", "destination"), name="unique_source_destination"
            ),
        ),
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                fields=("cargo", "seat", "trip"), name="unique_cargo_seat_trip"
            ),
        ),
    ]
