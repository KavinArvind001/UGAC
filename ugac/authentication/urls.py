from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home"),
    path('signup',views.signup, name="signup"),
    path('signin',views.signin, name="signin"),
    path('signout',views.signout, name="signout"),
    path('signined',views.signined, name="signined"),
    path('list_booklets',views.list_booklets, name="list_booklets"),
    path('add_booklet', views.add_booklet, name='add_booklet'),
    path('delete_booklet/<int:booklet_id>/', views.delete_booklet, name='delete_booklet'),
    #path('view_booklet/<int:booklet_id>/', views.view_booklet, name= 'view_booklet'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)