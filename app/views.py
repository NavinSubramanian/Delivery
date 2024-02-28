from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.

current_user = ''
logged = False
delivered = 0

def home(request):
    return render(request,"home.html")

def inv(request):
    return render(request,"inv.html")

def deli(request):
    global logged
    if(logged==False):
        return redirect('/home')
    items = Item.objects.all()
    itemss = Item.objects.all().values_list() 
    stock = {}
    for i in itemss:
        temp = i[1]
        my_item = Inventory.objects.get(itemname__itemname=temp)
        stock[temp] = my_item.stock
    req = Request.objects.all()
    context = {
        'current_user' : current_user,
        'item' : items,
        'stock' : stock,
        'requests': req,
    }
    return render(request,"del.html",context)

def dashboard(request):
    global logged,delivered
    if(logged==False):
        return render(request,'home.html')
    re = Request.objects.all()
    co = 0
    for i in re:
        if i.username is not None: 
            co = co+1
    items = Item.objects.all()
    itemss = Item.objects.all().values_list() 
    stock = {}
    s = Inventory.objects.all().values_list()
    ss = 0
    for i in s:
        ss = ss+int(i[2])
    price = 0
    for i in itemss:
        temp = i[1]
        my_item = Inventory.objects.get(itemname__itemname=temp)
        stock[temp] = my_item.stock
        price = price + (int(i[2])*int(stock[temp]))
    cat = Category.objects.all().values_list()
    context = {
        'current_user' : current_user,
        'item' : items,
        'stock' : stock,
        'totalstock' : ss,
        'totalprice' : price,
        'categories' : len(cat),
        'delivered' : co,
    }
    return render(request,"dashboard.html",context)

def logout(request):
    global logged,current_user
    logged = False
    current_user = ''
    return redirect('/home')

def reg(request):
    if(request.method == "POST"):
        name = request.POST.get('name')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password2')
        worker = request.POST['work']
        print(worker)
        if(pass1==pass2):
            user = User(username=name,password=pass1,workertype=worker)
            user.save()
            messages.success(request,'User Created succesfully')
            return redirect('/home')

        else:
            messages.error(request,'Error in user creation')
            return redirect('/inv')
        print(name,pass1,pass2)

def log(request):
    if(request.method == "POST"):
        name = request.POST.get('name')
        pass1 = request.POST.get('password')
        if User.objects.filter(username=name).exists():
            l = User.objects.filter(username=name).values_list()
            print(l[0])
            if l[0][2] == pass1:
                global logged,current_user
                logged=True
                current_user = l[0][1]
                if l[0][3] == 'inventory':
                    return redirect('/dashboard')
                else:
                    return redirect('/deli')
            else:
                return redirect('/inv')
        else:
            return redirect('/inv')
        
def req(request):
    return render(request,'request.html')

def increasestock(request):
    if request.method == "POST":
        item = request.POST['name']
        inc = request.POST.get('inc')
        inc = int(inc)

        item_instance = Item.objects.get(itemname=item)
        it = Item.objects.all().values_list()
        item_id = 0
        for i in it:
            if i[1]==item:
                item_id = i[0]
        
        invent = Inventory.objects.all().values_list()
        for i in invent:
            if i[1] == item_id:
                inc = inc + int(i[2])

        inventory = get_object_or_404(Inventory, id=item_id)
        inventory.stock = inc
        inventory.save()
        return redirect('/additem')

def additem(request):

    if request.method == "POST":
        item = request.POST.get('name')
        cost = request.POST.get('cost')
        stock = request.POST.get('stock')
        cat = request.POST['category']
        perish = request.POST.get('perish')
        date = request.POST.get('date2')

        category_instance = Category.objects.get(category=cat)
        print(date)
        new_item = Item(itemname=item, cost=cost, category=category_instance,perish=perish,expiry=date)
        new_item.save()

        item_instance = Item.objects.get(itemname=item)
        new_stock = Inventory(itemname=item_instance,stock=stock)
        new_stock.save()

        return redirect('/additem')

    cat = Category.objects.all()
    item = Item.objects.all()
    context = {
        'category':cat,
        'item':item,
    }
    return render(request,'additem.html',context)

def deliver(request,pk):
    global delivered,current_user
    if request.method == "POST":
        req = Request.objects.filter(id=pk).all().values_list()
        req_amount = 0
        req_item = 0
        for i in req:
            req_amount = int(i[3])
            req_item = i[1]
        item = Inventory.objects.filter(itemname=req_item).all().values_list()
        print(req_item)
        existing = 0
        for i in item:
            existing = int(i[2])
        if(req_amount<=existing):
            inventory = get_object_or_404(Inventory, itemname=req_item)
            inventory.stock = existing-req_amount
            inventory.save()

            reque = get_object_or_404(Request, id=pk)
            user_instance = User.objects.get(username=current_user)
            reque.username = user_instance 
            reque.save()

            delivered = delivered + 1
            messages.success(request,"Order was delivered")
            return redirect('/deli')
        else:
            messages.error(request,"Stock is low")
            return redirect('/deli')
    
    return redirect('/deli')

def profile(request):
    global current_user
    if current_user == '':
        return redirect('/home')
    req = Request.objects.all()
    user = User.objects.all().values_list()
    u_id =0
    for i in user:
        if i[1]==current_user:
            u_id=i[0]

    their = Request.objects.filter(username=u_id).all()
    print(their)


    context = {
        'current_user' : current_user,
        'requests' : their,
    }

    return render(request,'profile.html',context)