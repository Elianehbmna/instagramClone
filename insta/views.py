from django.shortcuts import render,redirect
from django.http  import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Image,User,Profile,Follow,Comment
from .forms import ImageForm,UpdateProfile,CommentForm
# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    current_user= request.user
    all_images=Image.objects.all()
    profile=Profile.objects.all()
    return render(request, 'all-views/index.html',{"images":all_images})

@login_required(login_url='/accounts/login/')
def posts(request):
    follows=Follow.objects.filter(following=request.user.id)
    images = Image.objects.filter(profile = request.user.followings.follower)
    return render(request, 'all-views/post.html',{"images":images})


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

    if Follow.objects.filter(following=request.user,follower=user).exists():
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

def follow(request,user_to):

    user=User.objects.get(id=user_to)
    is_follow=False
    if Follow.objects.filter(following=request.user,follower=user).exists():
        Follow.objects.filter(following=request.user,follower=user).delete()
        is_follow=False
    else:
        Follow(following=request.user,follower=user).save()
        is_follow=True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def search_results(request):

    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        searched_user = Profile.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'all-views/search.html',{"message":message,"users": searched_user})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-views/search.html',{"message":message})
        
@login_required(login_url='/accounts/login/')
def likepost(request,image_id):

    images=Image.objects.get(pk=image_id)
    is_liked=False
    if images.likes.filter(id=request.user.id).exists():
            images.likes.remove(request.user)
            is_liked=False
    else:
        images.likes.add(request.user)
        is_liked=True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')     
def new_comment(request,image_id):
    current_user=request.user
    
    image = Image.get_image_by_id(image_id)
    print(current_user)
   
    # profile=Profile.objects.get(user_id=current_user.id)
    # print(f' hey profile {profile}')
    # print(profile)
    if request.method=='POST':
        form=CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.postedby=current_user
            comment.commentImage=image
            comment.save()
            return redirect('welcome')
    else:
        form=CommentForm()
    
    return render(request,'all-views/comment.html',{"form":form,"image":image})

