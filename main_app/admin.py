from django.contrib import admin
from .models import Plant, Watering, Photo, Pot
# Register your models here.

admin.site.register(Plant)
admin.site.register(Watering)
admin.site.register(Pot)
admin.site.register(Photo)