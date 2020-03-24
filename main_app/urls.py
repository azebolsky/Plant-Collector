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
    path('plants/<int:plant_id>/assoc_pot/<int:pot_id>/', views.assoc_pot, name='assoc_pot'),
    path('plants/<int:plant_id>/unassoc_pot/<int:pot_id>/', views.unassoc_pot, name='unassoc_pot'),
    path('plants/<int:plant_id>/add_photo/', views.add_photo, name='add_photo'),
    path('pots/', views.PotList.as_view(), name='pots_index'),
    path('pots/<int:pk>/', views.PotDetail.as_view(), name='pots_detail'),
    path('pots/create/', views.PotCreate.as_view(), name='pots_create'),
    path('pots/<int:pk>/update/', views.PotUpdate.as_view(), name='pots_update'),
    path('pots/<int:pk>/delete/', views.PotDelete.as_view(), name='pots_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]