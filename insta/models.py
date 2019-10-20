from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime as dt
from tinymce.models import HTMLField

class Profile(models.Model):
    bio=models.CharField(max_length=100,blank=True,default="bio please...")
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
    imageCaption= models.CharField(max_length =30)
    profile= models.ForeignKey(User)
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

    def total_likes(self):
         self.likes.count()

    def __str__(self):
        return self.imageName
 
class Follow(models.Model):
    following=models.ForeignKey(User,related_name='rel_from_set')
    follower=models.ForeignKey(User,related_name='rel_to_set')

    def __str__(self):
        return '{} follows {}'.format(self.user_to)


User.add_to_class('following',models.ManyToManyField('self',through=Follow,related_name='followers',symmetrical=False))
    

    