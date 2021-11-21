from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout as auth_logout , login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
import json
import datetime


def store(request):
    products = Product.objects.all()
    data = {'products': products}
    return render(request, 'store/store.html',data)

@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0,'get_cart_item': 0}
    data = {'items': items,'order':order}
    return render(request, 'store/cart.html',data)

@login_required
def checkout(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except:
            customer = Customer.objects.create(user=request.user)
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0,'get_cart_item': 0}
    data = {'items': items,'order':order}
    return render(request, 'store/checkout.html',data)

def cardItems(request):
    user = request.user
    customer = customer = request.user.customer
    order, created = Order.objects.get_or_create(Customer=customer, complete=False)
    return JsonResponse({'itemsTotal': order.get_cart_item},safe=False)

def updateItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        user = request.user
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)

        orderItem, creaetd = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'minus':
            orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()

        if orderItem.quantity == 0:
            orderItem.delete()
        return JsonResponse({'itemsTotal': order.get_cart_item,'productQty':orderItem.quantity},safe=False)
    else:
        return JsonResponse({"error": "You should not be here"})

def checkoutDeliveryInfor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transactionId = datetime.datetime.now().timestamp()

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(Customer=customer, complete=False)
            order.transaction_Id = transactionId
            order.complete = True 
            order.save()
            DeliveryAddress.objects.create(
                Customer = customer,
                order = order,
                address = data["address"],
                city = data["city"],
                region = data["region"]
            )


        return JsonResponse({"status": 'Okay'},safe=False)
    else:
        return JsonResponse({"error": "You should not be here"})

def login(request):
    if request.method == 'GET':
        return render(request,'store/login.html')
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request,username=username,password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('/')
            else:
                return render(request,'store/login.html',{"error": "Invalid username or password. Please check and try again"})
        except Exception as e:
            print(e)
            return render(request,'store/login.html',{"error": "An error occured make sure all fields are filled and try again"})

def logout(request):
    auth_logout(request)

def register(request):
    if request.method == "GET":
        return render(request,'store/register.html')
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            
            if password != password2:
                return render(request,'store/register.html',{"error": "Password must match"})
            user = User.objects.create_user(username,email,password)
            return redirect('/login')
        except Exception as e:
            print(e)
            return render(request,'store/register.html',{"error": "An error occured make sure all fields are filled and try again"})
