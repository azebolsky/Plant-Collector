from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Plant, Pot, Photo
from .forms import WateringForm

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'catcollectorkitties'

# CBVs
# CBV for creating, updating, deleting plants and viewing form to do so

class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    fields = '__all__'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = '__all__'

class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = '/plants/'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def plants_index(request):
    plants = Plant.objects.filter(user=request.user)
    return render(request, 'plants/index.html', { 'plants': plants })

@login_required
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

@login_required
def add_watering(request, plant_id):
    form = WateringForm(request.POST)
    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()
    return redirect('detail', plant_id=plant_id)

@login_required
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

@login_required
def assoc_pot(request, plant_id, pot_id):
  # Note that you can pass a pot's id instead of the whole object
  Plant.objects.get(id=plant_id).pots.add(pot_id)
  return redirect('detail', plant_id=plant_id)

@login_required
def unassoc_pot(request, plant_id, pot_id):
    Plant.objects.get(id=plant_id).pots.remove(pot_id)
    return redirect('detail', plant_id=plant_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class PotList(LoginRequiredMixin, ListView):
    model = Pot

class PotDetail(LoginRequiredMixin, DetailView):
    model = Pot

class PotCreate(LoginRequiredMixin, CreateView):
    model = Pot
    fields = '__all__'

class PotUpdate(LoginRequiredMixin, UpdateView):
    model = Pot
    fields = '__all__'

class PotDelete(LoginRequiredMixin, DeleteView):
    model = Pot
    success_url = '/pots/'