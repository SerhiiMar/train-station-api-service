from django.contrib.auth import get_user_model
from django.db import models


class TrainType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_number = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        TrainType, on_delete=models.CASCADE, related_name="trains"
    )

    def __str__(self):
        return f"{self.name} (id: {self.id})"


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} (id: {self.id})"


class Route(models.Model):
    source = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_as_source"
    )
    destination = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_as_destination"
    )
    distance = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "destination"], name="unique_source_destination"
            )
        ]

    def __str__(self):
        return f"{self.source} - {self.destination}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "crew member"
        verbose_name_plural = "crew members"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Trip(models.Model):
    name = models.CharField(max_length=255)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="trips")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="trips")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="trip")

    def __str__(self):
        # return f"{self.name} (id: {self.id})"
        return f"{self.route.source} - {self.route.destination} ({self.departure_time})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="orders"
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        ordering = ("seat",)
        constraints = [
            models.UniqueConstraint(
                fields=("cargo", "seat", "trip"), name="unique_cargo_seat_trip"
            ),
        ]

    def __str__(self):
        return f"{self.trip} - (cargo: {self.cargo}, seat: {self.seat})"

    @staticmethod
    def valid_seat(seat, num_seats, error_to_raise):
        if not (1 <= seat <= num_seats):
            raise error_to_raise(
                {"seat": f"seat must be in range [1, {num_seats}], not {seat}"}
            )

    @staticmethod
    def valid_cargo(cargo, cargo_number, error_to_raise):
        if not (1 <= cargo <= cargo_number):
            raise error_to_raise(
                {"cargo": f"cargo must be in range [1, {cargo_number}], not {cargo}"}
            )

    def clean(self):
        self.valid_seat(self.seat, self.trip.train.places_in_cargo, ValueError)
        self.valid_cargo(self.cargo, self.trip.train.cargo_number, ValueError)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Ticket, self).save(*args, **kwargs)
