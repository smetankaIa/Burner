"""
URL configuration for a_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from a_main.views import *
from a_profile.views import *
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    path('', home_view, name='home'),
    
    path('nutricion/', RedirectView.as_view(
        url=reverse_lazy('nutricion_by_date', kwargs={'date_str': timezone.localdate().strftime('%Y-%m-%d')})
    ), name='nutricion'),
    path('nutricon/<str:date_str>/', daily_nutricion_view, name='nutricion_by_date'),
    path('nutricon/delete/<pk>', delete_nutricion_view, name='nutricion-delete'),
    
    path('product/search', product_search_view, {'active_tab': 'search'}, name='search-product'),
    path('product/create/', create_product_view, {'active_tab': 'create'}, name='create-product'),
    
    path('workout/', workout_view, name='workout'),
    path('workout/add/', workout_add_view, name='workout-add' ),
    path('workout/edit/<int:pk>', workout_edit_view, name='workout-edit' ),
    path('workout/delete/<int:pk>', workout_delete_view, name='workout-delete' ),
   
    path('profile/', profile_view, name='profile'),
    path('profile/edit', profile_edit_view, name='profile-edit'),
   
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)