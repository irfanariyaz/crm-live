from ast import Or
from multiprocessing import context
from tokenize import group
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only
# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST['password']

        user = authenticate(request, username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username and password doesn't match")
            return redirect('login')
        
    context = {}
    return render(request,'accounts/login.html',context)

def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # print('user:::',user)==zaid
            username  = form.cleaned_data.get('username')
           
            messages.success(request,'Account created succesfully:' + username)

            return redirect('login')
    context = {'form':form}
    return render(request,'accounts/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')  

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all() 
    customers = Customer.objects.all()
    total_orders = orders.count()
    orders_delivered =orders.filter(status ='Delivered').count()
    pending = orders.filter(status ='Pending').count() 
    context = {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'orders_delivered':orders_delivered,
        'pending':pending,
    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_delivered =orders.filter(status ='Delivered').count()
    pending = orders.filter(status ='Pending').count() 
    context = {
        'orders':orders,
        'total_orders':total_orders,
        'orders_delivered':orders_delivered,
        'pending':pending,
     }
    
    return render(request, 'accounts/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_setting(request):
    customer = request.user.customer
    form = CustomerForm(instance= customer)
    print(request.user.customer.profile_pic.url)

    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context= {
        'form':form
    }
    return render(request,'accounts/accounts_setting.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customer = Customer.objects.get(id = pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer,'orders':orders,
    'total_orders':total_orders,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        form.save()
        return redirect('/')
       
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request,pk):
    order = Order.objects.get(id =pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        form.save()
        return redirect('/') 
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request,pk):
    order = Order.objects.get(id =pk)
    context = {'order':order}
    if request.method == 'POST':
        order.delete()
        return redirect('/') 

    return render(request,'accounts/delete.html',context)

