from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url(r'^$',views.welcome,name = 'welcome'),
    url(r'^post',views.post,name ='post'),  
    url(r'^new/post$', views.post, name='new-post'),
    url(r'^profile/(\d+)',views.profile,name = 'profile'),
    url(r'^updateProfile',views.updateProfile,name = 'updateProfile'),
    url(r'^follow/(\d+)',views.follow,name="follow"),
    url(r'^search',views.search_results,name = 'search'),
    url(r'^like/(\d+)',views.likepost,name= 'likePost'),
    url(r'^comment/(\d+)/$',views.new_comment,name='comment')

    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)