from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

TIMES = (
  ('M', 'Morning'),
  ('A', 'Afternoon'),
  ('N', 'Night'),
)

# Create your models here.
class Pot(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('pots_detail', kwargs={'pk': self.id})

class Plant(models.Model):  # Note that parens are optional if not inheriting from another class
  name = models.CharField(max_length=100)
  color = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  pots = models.ManyToManyField(Pot)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
      return self.name

  def get_absolute_url(self):
    return reverse('detail', kwargs={'plant_id': self.id})

  def water_for_today(self):
    return self.watering_set.filter(date=date.today()).count() >= len(TIMES)

class Watering(models.Model):
  date = models.DateField('watering date')
  time = models.CharField(
    max_length=1,
    # add the choices field option
    choices=TIMES,
    # set the default value to morning
    default=TIMES[0][0]
  )
  plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_time_display()} on {self.date}"

  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=200)
  plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for plant_id: {self.plant_id} @{self.url}"