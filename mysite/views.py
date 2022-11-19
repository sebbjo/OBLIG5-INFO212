from .models import Car, Customer, Order, Employee
from rest_framework.response import Response
from .serializers import CarSerializer, CustomerSerializer, OrderSerializer, EmployeeSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json


@api_view(["GET"])
def get_cars(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_customers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def save_car(request):
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def save_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def save_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_car(request, id):
    try:
        the_car = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CarSerializer(the_car, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_employee(request, id):
    try:
        the_employee = Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EmployeeSerializer(the_employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_customer(request, id):
    try:
        the_customer = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(the_customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_car(request, id):
    try:
        the_car = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    the_car.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["DELETE"])
def delete_customer(request, id):
    try:
        the_customer = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    the_customer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["DELETE"])
def delete_employee(request, id):
    try:
        the_employee = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    the_employee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def order_car(request):
    """Creates order with key for Customer and Car.
    Edits customer order status and car availability"""

    order_serializer = OrderSerializer(data=request.data)
    car_id = request.data['car']
    customer_id = request.data['customer']
    
    if order_serializer.is_valid():
        try:
            the_car = Car.objects.get(pk=car_id)
            the_customer = Customer.objects.get(pk=customer_id)

        except Car.DoesNotExist or Customer.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if the_car.status != "booked":
            Car.objects.filter(pk=car_id).update(status="booked")
            if the_customer.active_order == False:
                Customer.objects.filter(pk=customer_id).update(active_order=True)
                order_serializer.save()
                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    "Customer has booking registered", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("Car already booked", status=status.HTTP_403_FORBIDDEN)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def cancel_ordered_car(request):
    """Implement an endpoint ‘cancel-order-car’ where a customer-id, car-id is passed as parameters.
    The system must check that the customer with customer-id has booked for the car.
    If the customer has booked the car, the car becomes available"""

    car_id = request.data['car']
    customer_id = request.data['customer']
    cancel_order = Order.objects.get(car = car_id, customer = customer_id)
    try:
    
        Car.objects.filter(pk=car_id).update(status='available')
        cancel_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def rent_car(request):
    """ Implement an endpoint 'rent-car' where a #customer-id, #car-id is passed as parameters. The
    system must check that the customer with customer-id has a booking for the car. The car's
    status is changed from 'booked' to 'rented'.  """

    car_id = request.data['car']
    customer_id = request.data['customer']
    the_order = Order.objects.get(car = car_id, customer = customer_id)
    if the_order.car == car_id and the_order.customer == customer_id:
        Car.objects.filter(pk=car_id).update(status="rented")
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

    


@api_view(["DELETE"])
def return_car(request):
    """- Implement an endpoint 'return-car' where a customer-id, car-id is passed as parameters.
    Car's status (e.g., ok or damaged) during the return will also be passed. The system must
    check that the customer with customer-id has rented the car. The car's status is changed
    from 'booked' to 'available' or 'damaged' """
    car_id = request.data['car']
    customer_id = request.data['customer']
    the_order = Order.objects.get(car = car_id, customer = customer_id)
    the_status = "available"
    try:
        if request.data['status'] in ["damaged", "broken", "crashed"]:
            the_status = request.data['status']
    except:
        pass


    if the_order.car == car_id and the_order.customer == customer_id:
        Car.objects.filter(pk=car_id).update(status=the_status)
        Customer.objects.filter(pk=customer_id).update(active_order = False)
        the_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
