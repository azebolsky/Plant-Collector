from django.urls import path
from . import views

# urlpatterns hold the routes we define in main_app
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('plants/', views.plants_index, name='index'),
    path('plants/<int:plant_id>/', views.plants_detail, name='detail'),
    # new route used to show a form and create a cat
    path('plants/create/', views.PlantCreate.as_view(), name='plants_create'),
    path('plants/<int:pk>/update/', views.PlantUpdate.as_view(), name='plants_update'),
    path('plants/<int:pk>/delete/', views.PlantDelete.as_view(), name='plants_delete'),
    path('plants/<int:plant_id>/add_watering/', views.add_watering, name='add_watering'),
    path('plants/<int:pot_id>/assoc_pot/<int:pot_id>/', views.assoc_pot, name='assoc_pot'),
]