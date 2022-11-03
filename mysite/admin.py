from django.contrib import admin
from .models import Car
from .models import Customer
from .models import Employee
from .models import Order_car

admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Order_car)
