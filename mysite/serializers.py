from rest_framework import serializers
from .models import Car, Customer, Employee, Order_car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'carmodel', 'year', 'location', 'status']

        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'age']

        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'age', 'branch']

        
class Order_carSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_car
        fields = ["id", "car", "customer"]
        
