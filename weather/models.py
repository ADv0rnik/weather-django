from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=100)
    temp = models.FloatField(blank=False)
    hum = models.IntegerField(blank=False)
    rain = models.FloatField(blank=False)
    icon = models.CharField(max_length=200)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(
            self.city,
            self.temp,
            self.hum,
            self.rain,
            self.time_create
        )

