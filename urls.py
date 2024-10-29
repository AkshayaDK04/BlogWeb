# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('content/<str:content_type>/', views.content_list, name='content_list'),
    path('post/', views.post_content, name='post_content'),
    path('like/<int:content_id>/', views.like_content, name='like'),
    path('add_comment/<int:content_id>/', views.add_comment, name='add_comment'),
    path('signin/', views.signin, name='signin'),
    path('upload-calligraphy/', views.upload_calligraphy, name='upload_calligraphy'),
    path('signup/', views.signup, name='signup'),
]
