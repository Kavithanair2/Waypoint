from django.db import models

class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("expert", "Expert"),
    ]

    name = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=6, decimal_places=1)
    elevation_gain = models.IntegerField()
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
    )
    is_open = models.BooleanField(default=True)
    added = models.DateField(auto_now_add=True)

    @property
    def distance(self):
        return self.distance_km

    @property
    def elevation(self):
        return self.elevation_gain

    def __str__(self):
        return self.name