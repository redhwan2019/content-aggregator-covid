from django.db import models

class CovidContent(models.Model):
  headline = models.CharField(max_length=300)
  img = models.URLField(null=True, blank=True)
  url = models.TextField()
  date = models.TextField(null=True, blank=True)
  def __str__(self):
    return self.headline

class CovidContentLink(models.Model):
  id= models.TextField(primary_key=True)
  url = models.TextField()

