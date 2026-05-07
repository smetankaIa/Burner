from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localdate
from django.utils import timezone
import uuid 


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50, null=False)
    
    calories = models.DecimalField(decimal_places=1, max_digits=5, default=0.0)# на 100 грамм
    protein = models.DecimalField(decimal_places=1, max_digits=5, default=0.0)# на 100 грамм
    fat = models.DecimalField(decimal_places=1, max_digits=5, default=0.0)# на 100 грамм
    carbs = models.DecimalField(decimal_places=1, max_digits=5, default=0.0)# на 100 грамм
    
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
            # ordering = ['-created']
            db_table = 'a_main_product'
            verbose_name = 'Продукт'
            verbose_name_plural = 'Продукты'
            
    def __str__(self):
        return str(self.title)  


class Nutricion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight_product = models.DecimalField(max_digits=5, decimal_places=1, default=100.0)
    date_meal = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def total_calories(self):
        return round((self.product.calories * self.weight_product) / 100, 2)
    
    @property
    def total_protein(self):
        return round((self.product.protein * self.weight_product) / 100, 2)
    
    @property
    def total_fat(self):
        return round((self.product.fat * self.weight_product) / 100, 2)
    
    @property
    def total_carbs(self):
        return round((self.product.carbs * self.weight_product) / 100, 2)
    
    
    class Meta:
       ordering = ['-date_meal']
       verbose_name = 'Питание'
       verbose_name_plural = 'Питания'
    
    def __str__(self):
        return f'{self.user.username}: {self.product.title}: {self.weight_product} грамм'   
       
    
    
class Workout(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=50, default='Стандартная')
    # coach
    duration = models.IntegerField(default=0, null=True)
    
    
    
    def __str__(self):
        return f'{self.user.username}: {self.date} {self.type}'