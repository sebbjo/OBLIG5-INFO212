from rest_framework import serializers
from .models import Car
# from .models import Customer

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = car
        fields = ['id', 'make', 'carmodel', 'year', 'location', 'status']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = car
        fields = ['name', 'address', 'age']
        
class EmployeeSerializer(serializers.ModelSerializer): 
    class Meta:
        model = employee
        fields = ['name', 'age', 'branch']
        
# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['id', 'name', 'age', 'address']
