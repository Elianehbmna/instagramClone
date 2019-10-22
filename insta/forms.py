from .models import Image,Profile,Comment
from django import forms

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['profile', 'user_profile' , 'likes']

class UpdateProfile(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['bio','profilepic'] 
        exclude=['user']     
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']
