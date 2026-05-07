from django.shortcuts import render
from .models import Specialist

# Create your views here.
def specialist_list(request):
    specialists = Specialist.objects.all()

    print("SPECIALISTS:", specialists)
    print("COUNT:", specialists.count())

    return render(request, 'includes/specialist_list.html', {
        'specialists': specialists
    })