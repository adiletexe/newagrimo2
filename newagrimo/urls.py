
from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup', views.signupsystem, name='signupsystem'),
    path('login', views.loginsystem, name='loginsystem'),
    path('logout', views.logoutsystem, name='logoutsystem'),
    path('graphs/<str:param>/', views.graphs, name='graphs'),
    path('graphspredict/<str:param>/', views.graphspredict, name='graphspredict'),
    path('graphsai', views.graphsai, name='graphsai'),
    path('geolocation', views.geolocation, name='geolocation'),
    path('shop', views.shop, name='shop'),
    path('specialists', views.specialists, name='specialists'),
    path('profile', views.profile, name='profile'),
    path('education', views.education, name='education'),
    path('add_shape', views.add_shape, name='add_shape'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
