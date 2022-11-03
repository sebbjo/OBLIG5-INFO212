from .models import Car
from .models import Customer
from .models import Employee
from .models import Order_car
from .serializers import CarSerializer
from .serializers import CustomerSerializer
from .serializers import EmployeeSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_cars(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_car(request):
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
@api_view(['PUT'])
def update_car(request, id):
    try:
        theCar = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CarSerializer(theCar, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
def delete_car(request, id):
    try:
        theCar = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    theCar.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_customer(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
@api_view(['PUT'])
def update_customer(request, id):
    try:
        theCustomer = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(theCustomer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
def delete_customer(request, id):
    try:
        theCustomer = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    theCustomer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_employee(request):
    employee = Employee.objects.all()
    serializer = EmployeeSerializer(Employee, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
@api_view(['PUT'])
def update_employee(request, id):
    try:
        theEmployee = Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EmployeeSerializer(theEmployee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
def delete_employee(request, id):
    try:
        theEmployee = Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    theEmployee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(["POST"])
def order_car(request):
    #Place order for a car

    order_serializer = Order_carSerializer(data= request.data)
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
    #Cancel an existing order

    car_id = request.data['car']
    customer_id = request.data['customer']
    cancel_order = Order_car.objects.get(car = car_id, customer = customer_id)
    try:
        if cancel_order.car == car_id and cancel_order.customer == customer_id:
            Car.objects.filter(pk=car_id).update(status='available')
            cancel_order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Order_car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def rent_car(request):
    #Change status from booked to rented
    
    car_id = request.data['car']
    customer_id = request.data['customer']
    the_order = Order_car.objects.get(car = car_id, customer = customer_id)
    if the_order.car == car_id and the_order.customer == customer_id:
        Car.objects.filter(pk=car_id).update(status="rented")
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def return_car(request):
    #return car to dealer

    car_id = request.data['car']
    customer_id = request.data['customer']
    the_order = Order_car.objects.get(car = car_id, customer = customer_id)
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
