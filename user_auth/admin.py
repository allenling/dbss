#coding=utf8
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Permission


from dbss.user_auth.models import MyUser,UserFollow 


class UserCreationForm(forms.ModelForm):
	password1=forms.CharField(label='passwd',widget=forms.PasswordInput)
	password2=forms.CharField(label='passwd comfired',widget=forms.PasswordInput)
	class Meta:
		model=MyUser
	def clean_password(self):
		password1=self.clean_data.get('password1')
		password2=self.clean_data.get('password2')
		if password1 and password2 and password1 is not password2:
			raise forms.ValidationError('Password do not match')
		return password2
	def save(self,commit=True):
		user=super(UserCreationForm,self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user
class UserChangeForm(forms.ModelForm):
	password=ReadOnlyPasswordHashField(help_text=("change password <a href=\"password/\">through</a>"))	
	class Meta:
		model=MyUser
	def clean_password(self):
		return self.initial['password']
class MyUserAdmin(UserAdmin):
	form=UserChangeForm
	add_form=UserCreationForm
	list_display=('username','email','something','last_login','date_join',)
	list_filter=('is_staff','is_superuser',)
	fieldsets=(
				('Personal info',{'fields':('username','email','something','password','score')}),
				('Permissions',{'fields':('is_superuser','is_staff','is_active',)}),
				('Important dates',{'fields':('last_login','date_join')}),
				('Friends',{'fields':('friends',)}),
				('Favlist',{'fields':('favlist',)}),
	)
	add_fieldsets=(
					(None,{'classes':('wide',),'fields':('username','email','something','password1','password2')}),)

	search_fields=('username','email',)
	ordering=('date_join',)
	filter_horizontal=()
	readonly_fields=('date_join',)
admin.site.register(MyUser,MyUserAdmin)
admin.site.register(Permission)
admin.site.register(UserFollow)
