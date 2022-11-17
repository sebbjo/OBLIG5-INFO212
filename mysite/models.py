from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=50)
    carmodel = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.make + ' ' + self.carmodel + ' ' + self.year + ', ' + self.location + ', ' + self.status

class Customer(models.Model):
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=3)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name + ', ' + self.age + ', ' + self.address

class Employee(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)

    def __str__(self):
        return self.name + ', ' + self.address + ', ' + self.branch

class Order_car(models.Model):
    car_id = models.CharField(max_length=8)  # registration number
    customer_id = models.CharField(max_length=10)

    def __str__(self):
        return str(self.car_id) + " " + str(self.customer_id)
    
