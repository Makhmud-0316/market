"""
URL configuration for study_project project.

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
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from market import views
from market.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MarketView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('deals/', views.deals, name='deals'),
    path('services/', views.services, name='services'),
    path('login/', LoginUser.as_view(), name='login'),
    path('signup/', SignUser.as_view(), name='signup'),
    path('logout/', logout_user, name='logout'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
