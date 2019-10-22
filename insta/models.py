from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime as dt
from tinymce.models import HTMLField

class Profile(models.Model):
    bio=models.TextField(max_length=100,blank=True,default="bio please...")
    profilepic=models.ImageField(upload_to='profile/', blank = True,default='../static/images/bad-profile-pic-2.jpeg')
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

    @classmethod
    def search_by_name(cls,search_term):
        news = cls.objects.filter(user__username__icontains = search_term)
        return news


class Image(models.Model):
    image = models.ImageField(upload_to='post/', blank=True)
    imageName = models.CharField(max_length =30)
    imageCaption= models.TextField(max_length =30)
    profile= models.ForeignKey(User)
    user_profile=models.ForeignKey(Profile)
    likes=models.ManyToManyField(User,related_name = 'likes',blank=True)

    @classmethod
    def save_image(self):
        self.save()
    @classmethod
    def delete_image(self):
        self.delete()
    @classmethod
    def update_caption(cls,id,caption):
        captions=cls.objects.filter(caption_id=id).update(image_caption = caption)
        return captions

    

    @classmethod
    def get_image_by_id(cls,image_id):
        images=cls.objects.get(id=image_id)
        return images

    def __str__(self):
        return self.imageName
 
class Follow(models.Model):
    following=models.ForeignKey(User,related_name='following')
    follower=models.ForeignKey(User,related_name='follower')

    def __str__(self):
        return '{} follows {}'.format(self.following,self.follower)


User.add_to_class('followings',models.ManyToManyField('self',through=Follow,related_name='followers',symmetrical=False))
    

class Comment(models.Model):
    postedby=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    commentImage=models.ForeignKey(Image,on_delete=models.CASCADE,null=True)
    comment=models.CharField(max_length=150,null=True)
    
    def __str__(self):
        return str(self.postedby)