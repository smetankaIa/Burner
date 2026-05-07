from django.forms import ModelForm
from django import forms
from .models import Product, Nutricion, Workout


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'protein', 'calories','fat','carbs']
        labels = {
            'title' : 'Название продукта',
            'calories' : 'ККАЛ',
            'protein' : 'БЕЛКИ',
            'fat' : 'ЖИРЫ',
            'carbs' : 'УГЛ.'
        }

class NutricionAddForm(ModelForm):
    class Meta:
        model = Nutricion
        fields = ['weight_product']
        labels = {
            'weight' : 'Вес',
            
        }
        
class WorkoutAddForm(ModelForm):       
    class Meta:
        model = Workout
        exclude = ['user']
        labels = {
            'date': 'Дата и время',
            'type': 'Тип тренировки',
            'duration': 'Длительность (минуты)'
        }
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'w-full bg-white/10 border border-white/20 p-3 rounded-2xl outline-none focus:ring-2 focus:ring-white/50 transition text-white [color-scheme:dark]'
            }),
            'type': forms.TextInput(attrs={
                'class': 'w-full bg-white/10 border border-white/20 p-3 rounded-2xl outline-none focus:ring-2 focus:ring-white/50 transition text-white',
                'placeholder': 'Например: Силовая, Кардио...'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'w-full bg-white/10 border border-white/20 p-3 rounded-2xl outline-none focus:ring-2 focus:ring-white/50 transition text-white',
                'placeholder': '45'
            }),
        }
        
