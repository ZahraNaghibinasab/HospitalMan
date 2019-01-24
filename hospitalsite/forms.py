from django import forms

from .models import User

from .models import DrugStore



class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name','id','tel','Email' )



class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name','tel', 'weight', 'height', 'gender' , 'age' , 'address' , 'postalCode' )


# class EnterForm(forms.ModelForm):
#
#     class Meta:
#         model = User
#         fields = ('id', 'password')