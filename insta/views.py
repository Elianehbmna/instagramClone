from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Image,User,Profile
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
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user
            image.save()
        return redirect('welcome')

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
	
	return render(request,"all-views/profile.html",{"images":images,"profile":profile,"title":title})

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

    
                   