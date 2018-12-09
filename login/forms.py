#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tian'
__data__ = '2018/11/30 20:23'


from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))  #使用bottsor里面的css样式widget=forms.TextInput(attrs={'class':'form-control'})
    password = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'})) #指定为密文显示密码class form-control指的是bottsor里面的样式名称
    captcha  = CaptchaField(label='验证码')


class RegisterForm(forms.Form):

    gender = (
        ('male','男'),
        ('femald','女'),
    )

    username  = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email     = forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex       = forms.ChoiceField(label='性别',choices=gender)
    captcha   = CaptchaField(label='验证码')

