"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.views.generic.base import TemplateView
from .views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("cars/", get_cars),
    path("save_car/", get_cars),
    path("update_car/<int:id>", update_car),
    path("delete_car/<int:id>", delete_car),
    path("customer/", get_customer),
    path("update_customer/", update_customer),
    path("delete_customer/", delete_customer),
    path("save_customer/", save_customer),
    path("employee/", get_employee),
    path("update_employee/", update_employee),
    path("delete_employee/", delete_employee),
    path("save_employee/", save_employee),
    path("order_car/", order_car),
    path("rent_car/", rent_car),
    path("cancel_order/", cancel_ordered_car),
    path("return_car/", return_car),
    path("test/", test)

]
