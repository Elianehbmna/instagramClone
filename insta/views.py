from django.shortcuts import render,redirect
from django.http  import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Image,User,Profile,Follow
from .forms import ImageForm,UpdateProfile
# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    return render(request, 'all-views/index.html')

@login_required(login_url='/accounts/login/')
def posts(request, post_id):
    try:
        post = Image.objects.get(id = post_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-views/post.html", {"posts":post})

@login_required(login_url='/accounts/login/')
def post(request):
    current_user = request.user
    profile = Profile.objects.get(user = request.user.id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user
            image.user_profile = profile
            image.save()
        return redirect('profile',current_user.id)

    else:
        form = ImageForm()
    return render(request, 'new_post.html', {"form": form})

@login_required(login_url='/accounts/login/')
def profile(request,profile_id):
    '''
    Method that fetches a users profile page
    '''
    user=User.objects.get(pk=profile_id)
    images = Image.objects.filter(profile = profile_id)
    title = User.objects.get(pk = profile_id).username
    profile = Profile.objects.filter(user = profile_id)

    if Follow.objects.filter(follower=request.user,following=user).exists():
        is_follow=True
    else:
        is_follow=False

    followers=Follow.objects.filter(follower = user).count()
    followings=Follow.objects.filter(following=user).count()


    return render(request,"all-views/profile.html",{"images":images,"profile":profile,"title":title,"is_follow":is_follow,"followers":followers,"followings":followings})

@login_required(login_url='/accounts/login/')
def updateProfile(request):

    current_user=request.user
    if request.method =='POST':
        if Profile.objects.filter(user_id=current_user).exists():
            form = UpdateProfile(request.POST,request.FILES,instance=Profile.objects.get(user_id = current_user))
        else:
            form=UpdateProfile(request.POST,request.FILES)
        if form.is_valid():
          profile=form.save(commit=False)
          profile.user=current_user
          profile.save()
          return redirect('profile',current_user.id)
    else:

        if Profile.objects.filter(user_id = current_user).exists():
           form=UpdateProfile(instance =Profile.objects.get(user_id=current_user))
        else:
            form=UpdateProfile()

    return render(request,'all-views/update.html',{"form":form})        

def follow(request,follower):

    user=User.objects.get(id=follower)
    is_follow=False
    if Follow.objects.filter(following=request.user,follower=user).exists():
        Follow.objects.filter(following=request.user,follower=user).delete()
        is_follow=False
    else:
        Follow(following=request.user,follower=user).save()
        is_follow=True

    return HttpResponseRedirect(request.meta.get('HTTP_REFERER'))
                   