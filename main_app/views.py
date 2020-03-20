from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3
from .models import Plant, Pot, Watering, Photo
from .forms import WateringForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector'

# CBVs
# CBV for creating, updating, deleting plants and viewing form to do so

class PlantCreate(CreateView):
    model = Plant
    fields = '__all__'

class PlantUpdate(UpdateView):
    model = Plant
    fields = '__all__'

class PlantDelete(DeleteView):
    model = Plant
    success_url = '/plants/'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def plants_index(request):
    plants = Plant.objects.all()
    return render(request, 'plants/index.html', { 'plants': plants })

def plants_detail(request, plant_id):
    # instance of the plant model
    plant = Plant.objects.get(id=plant_id)
    # get the pots the plant doesn't
    pots_plant_doesnt_have = Pot.objects.exclude(id__in = plant.pots.all().values_list('id'))
    watering_form = WateringForm()
    return render(request, 'plants/detail.html', {
        'plant': plant, 'watering_form': watering_form,
        'pots': pots_plant_doesnt_have
    })

def add_watering(request, plant_id):
    form = WateringForm(request.POST)
    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()
    return redirect('detail', plant_id=plant_id)

def add_photo(request, plant_id):
	# photo-file was the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to plant_id or plant (if you have a plant object)
      photo = Photo(url=url, plant_id=plant_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', plant_id=plant_id)

def assoc_pot(request, plant_id, pot_id):
  # Note that you can pass a pot's id instead of the whole object
  Plant.objects.get(id=plant_id).pots.add(pot_id)
  return redirect('detail', plant_id=plant_id)

def unassoc_pot(request, plant_id, pot_id):
    Plant.objects.get(id=plant_id).pots.remove(pot_id)
    return redirect('detail', plant_id=plant_id)

class PotList(ListView):
    model = Pot

class PotDetail(DetailView):
    model = Pot

class PotCreate(CreateView):
    model = Pot
    fields = '__all__'

class PotUpdate(UpdateView):
    model = Pot
    fields = '__all__'

class PotDelete(DeleteView):
    model = Pot
    success_url = '/pots/'