from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url(r'^$',views.welcome,name = 'welcome'),
    url(r'^post/(\d+)',views.posts,name ='post'),  
    url(r'^new/post$', views.post, name='new-post'),
     url(r'^profile/(\d+)',views.profile,name = 'profile')
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)