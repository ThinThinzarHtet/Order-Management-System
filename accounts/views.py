from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from accounts.models import *
from accounts.forms import *
from .filters import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def customers(request, id):
    customer = Customer.objects.get(id = id)
    orders = customer.order_set.all()
    order_count = orders.count()
    filterObj = OrderFilter(request.GET, queryset=orders)
    orders = filterObj.qs
    return render(request, 'accounts/customers.html', {
        'customer' : customer,
        'orders' : orders,
        'order_count' : order_count,
        'filterObj' : filterObj
    })

def products(request):
    # return HttpResponse('contact pafe')
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {
        'products' : products
    })

def dashboard(request):
    # return HttpResponse('dashboard pafe')
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total = orders.count()
    delivered = Order.objects.filter(status="delivered").count()
    pending = Order.objects.filter(status="pending").count()
    return render(request, 'accounts/dashboard.html', {
        'customers' : customers,
        'orders' : orders,
        'total' : total,
        'delivered' : delivered,
        'pending': pending
    })

def orderCreate(request, customerId):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id = customerId)
    formset = OrderFormSet(instance=customer, queryset=Order.objects.none()) #need to add instance = customer to know whose formset is this 
    # form = OrderForm(initial= {'customer': customer})
    if request.method == "POST":

        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', {
        'formset' : formset
    })

def orderUpdate(request, orderId):
    order = Order.objects.get(id = orderId)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order) #should add instance you want to update
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', {
        'form' : form
    })

def orderDelete(request, orderId):
    order = Order.objects.get(id = orderId)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    return render(request, 'accounts/order_delete.html', {
        'order' : order
    })

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'accounts/register.html', {
        'form' : form
    })

'''login function'''
def userLogin(request):
    if request.method == "POST":
        username = request.POST['username'] #[username] ka login.html mhr label htl ka username so tae name
        password = request.POST['password']

        user = authenticate(request, username = username, password = password) #authenticate() ka db htl mhr htae htr tae data twy shi lr sit, shi yin user yaw obj ko pay ml ,ma shi yin none pay ml
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'username and password is incorrect')
            return redirect('/login')
    return render(request, 'accounts/login.html')

'''logout function'''
def userLogout(request):
    logout(request)
    return redirect('/login')