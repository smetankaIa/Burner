from django.shortcuts import render, redirect, get_object_or_404

from datetime import timedelta, datetime

from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import *
from a_specialist.models import Specialist
from .forms import *

import calendar



def home_view(request):
    specialists = Specialist.objects.all()[:3]
    
    return render(request, 'a_main/home.html',{
        'specialists': specialists
    })


@login_required
def daily_nutricion_view(request, date_str):
    
    current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    nutricions = Nutricion.objects.filter(user=request.user, date_meal__date = current_date).order_by('date_meal')
    
    previous_day = current_date - timedelta(days=1)
    next_day = current_date + timedelta(days=1)
    
    contex = {
        'nutricions': nutricions,
        'current_date': current_date,
        'previous_day': previous_day,
        'next_day': next_day,
        'is_today' : current_date == timezone.now().date(),
    }
    
    return render(request, 'a_main/nutricion.html', contex )

@login_required
def delete_nutricion_view(request, pk):
    nutricion = get_object_or_404(Nutricion, id=pk)
    if request.method == "POST":
        nutricion.delete()
        return redirect('nutricion')
    
    return render(request, 'a_main/nutricion_delete.html', {'nutricion': nutricion})


@login_required
def product_search_view(request, active_tab=None):
    products = Product.objects.all()
    
    product_id = request.POST.get('product_id')
    form = NutricionAddForm()
    
    if request.method == 'POST':
        form = NutricionAddForm(request.POST)
        if form.is_valid and product_id:
            new_nutrition_record = form.save(commit=False)
            product = get_object_or_404(Product, id=product_id)
            
            new_nutrition_record.user = request.user
            new_nutrition_record.product = product 
            new_nutrition_record.save()
            return redirect('nutricion')
    else:
         form = NutricionAddForm()   
    context = {
        'form': form,
        'products': products,
        'active_tab': active_tab
    }
    return render(request, 'a_main/search_products.html', context)

@login_required
def create_product_view(request, active_tab='create'):
    
    if request.method == 'POST':
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('search-product') 
        else:
            active_tab = 'create' 
    else:
        form = ProductCreateForm()
    context = {
        'form' : form,
        'active_tab': active_tab
    }
    
    return render(request, 'a_main/product_create.html', context)

@login_required
def workout_view(request):
    import datetime
     # 1. Получаем текущую дату
    current_date = datetime.date.today()
    

    # 2. Смотрим, какой месяц запросил пользователь (через URL: ?year=2026&month=4)
    # Если параметров нет, показываем текущий месяц
    try:
        year = int(request.GET.get('year', current_date.year))
        month = int(request.GET.get('month', current_date.month))
    except ValueError:
        year = current_date.year
        month = current_date.month

    # Защита от дурака (если ввели месяц 13)
    if month < 1 or month > 12:
        month = current_date.month
        year = current_date.year

    # 3. Высчитываем предыдущий и следующий месяц для кнопок "Вперед/Назад"
    prev_month = 12 if month == 1 else month - 1
    prev_year = year - 1 if month == 1 else year

    next_month = 1 if month == 12 else month + 1
    next_year = year + 1 if month == 12 else year

    # 4. Достаем все тренировки юзера за ВЫБРАННЫЙ месяц
    workouts_this_month = Workout.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    )

    
    workouts_by_day = {}
    for workout in workouts_this_month:
        day = workout.date.day
        workouts_by_day[day] = workout 

    # 5. Генерируем сетку календаря (список недель, внутри которых списки дней)
    cal = calendar.Calendar(firstweekday=0) # 0 означает, что неделя начинается с Понедельника
    month_days = cal.monthdayscalendar(year, month)

    # Формируем красивый массив для шаблона
    calendar_grid = []
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0:
                # 0 означает пустую клетку (день из другого месяца)
                week_data.append({'day': 0, 'workout': None, 'is_today': False})
            else:
                is_today = (year == current_date.year and month == current_date.month and day == current_date.day)
                week_data.append({
                    'day': day,
                    'workout': workouts_by_day.get(day), # Достаем тренировку из словаря, если она есть
                    'is_today': is_today
                })
        calendar_grid.append(week_data)

    # 6. Названия месяцев на русском для заголовка
    month_names = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
                   'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    
    # 7. Тренировка для Sidebar (за сегодня)
    today_workout = Workout.objects.filter(user=request.user, date__date=current_date).first()

#    # Обработка формы добавления тренировки
#     if request.method == 'POST':
#         form = WorkoutAddForm(request.POST)
#         if form.is_valid():
#             workout = form.save(commit=False)
#             workout.user = request.user # Привязываем к текущему юзеру!
#             workout.save()
#             return redirect('calendar_view') # Перезагружаем страницу (укажи свой name из urls.py)
#     else:
#         # Если GET запрос, создаем пустую форму. 
#         # Можно передать initial, чтобы дата по умолчанию стояла на сегодня
#         form = WorkoutAddForm(initial={'date': current_date})

    context = {
        'calendar_grid': calendar_grid,
        'current_month_name': f"{month_names[month]} {year}",
        'prev_year': prev_year, 'prev_month': prev_month,
        'next_year': next_year, 'next_month': next_month,
        'today_workout': today_workout,
        
        # Передаем форму в шаблон
        # 'form': form,
    }


    return render(request, 'a_main/workout.html', context)

@login_required
def workout_add_view(request):
    form = WorkoutAddForm()
    if request.method == 'POST':
        form = WorkoutAddForm(request.POST)
        if form.is_valid:
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('workout')
        
    
    return render(request, 'a_main/workout_create.html', {'form': form})

@login_required
def workout_edit_view(request, pk):
    workout = get_object_or_404(Workout, id=pk, user=request.user)
    form = WorkoutAddForm(instance=workout)
    
    if request.method == 'POST':
        form = WorkoutAddForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('workout')
            
    context = {
        'form': form, 
        'edit_mode': True, 
        'workout': workout
        }
 
    return render(request, 'a_main/workout_create.html', context)

@login_required
def workout_delete_view(request, pk):
    workout = get_object_or_404(Workout, id=pk, user=request.user)
    if request.method == 'POST':
        workout.delete()
    return redirect('calendar_view')