from django.forms import ModelForm
from .models import *
from django import forms
from .models import Profile





class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'plusstatus', 'email']
        labels = {
            'firstname' : 'Имя',
            'lastname' : 'Фамилия',
            # 'email' : 'Почта',
            'male' : 'Пол',
            'goal' : 'Цель',
            'activity': 'Активность',
            'height' : 'Рост',
            'weight' : 'Вес',
            'dete_birth' : 'Дата рождения',
        }
       
       
       

from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # CSS классы, которые мы хотим применить ко всем полям
        css_classes = 'bg-white/10 border border-white/20 p-4 rounded-2xl outline-none focus:ring-4 focus:ring-white/30 transition text-white placeholder-white/30 font-medium'
        
        # Проходимся по всем полям формы и добавляем атрибуты
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': css_classes,
                'placeholder': field.label or '' # Используем label как placeholder
            })
            # Для полей пароля ставим стандартный placeholder
            if isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs['placeholder'] = '••••••••'


       
              