from django.db import models

class CovidContent(models.Model):
  headline = models.CharField(max_length=300)
  img = models.URLField(null=True, blank=True)
  url = models.TextField()
  def __str__(self):
    return self.headline

class CovidContentLink(models.Model):
  url = models.TextField()

