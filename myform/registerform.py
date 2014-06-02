#coding=utf8
#from django.contrib.auth.models import User
from dbss.user_auth.models import MyUser as User
from django.forms import ModelForm
from django import forms
from captcha.fields import CaptchaField


class ReUserForm1(ModelForm):
	password=forms.CharField(label='password',widget=forms.PasswordInput)
	passwordcom=forms.CharField(label='passwordcom',widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=('username','email',)
	def clean_passwordcom(self):
		cleaned_data=super(ReUserForm1,self).clean()
		password1_data=cleaned_data.get('password')
		password2_data=cleaned_data.get('passwordcom')
		if password1_data!=password2_data:
			raise forms.ValidationError(u'password is not equal passwordcom')
		return cleaned_data	
'''
	def clean(self):
		cleaned_data=super(ReUserForm1,self).clean()
		email_data=cleaned_data.get('email')
		if User.objects.filter(email=email_data).count() is not 0:
			msg = u'this email is already exists.'
			self._errors['email']=self.error_class([msg])
			#raise forms.ValidationError(u'this email is already exists!')
			del cleaned_data['email']
		return cleaned_data

	def clean_email(self):	
		cleaned_data=super(ReUserForm1,self).clean()
		email_data=cleaned_data.get('email')
		if User.objects.filter(email=email_data).count() is not 0:
		#	self._errors['email']=[u'this email is already exists.']
			raise forms.ValidationError(u'this email is already exist!')
		return cleaned_data
'''
class ReUserForm2(ModelForm):
    birth_day=forms.DateField(required = False)
    phone=forms.CharField(max_length=11, required = False)
    something=forms.CharField(max_length=70, required = False)
    class Meta:
		model=User
		fields=('birth_day', 'phone', 'something')


class ReUserForm3(ModelForm):
    captcha=CaptchaField()
    class Meta:
        model = User
        fields = []
    def clean_captcha(self):
        cleaned_data=super(ReUserForm3, self).clean()
        return cleaned_data
