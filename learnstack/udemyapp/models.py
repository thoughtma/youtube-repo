from django.db import models

class UdemyCourse(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField()
    thumbnail = models.URLField()
    def __str__(self):
        return self.title
