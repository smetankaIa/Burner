from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
@login_required
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    return render(request, 'a_profile/profile.html', {'profile': profile})

@login_required  
def profile_edit_view(request):
    form = ProfileEditForm(instance=request.user.profile)
    
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        else:
            # ДОБАВЬ ВОТ ЭТУ СТРОКУ:
            print("ОШИБКИ ФОРМЫ:", form.errors) 
    return render(request, 'a_profile/profile_edit.html', {'form' : form})   

def specialist_view(request, pk):
    specialists = get_object_or_404(Specialist, id=pk)
    
    return render(request, 'a_profile/specialist.html', {'specialists' : specialists})