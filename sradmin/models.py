from django.db import models


# model: Monitoring intervals
class MonitoringInterval(models.Model):
    type = models.CharField(max_length=30, unique=True)
    interval = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.type
