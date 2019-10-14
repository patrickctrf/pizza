from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import *

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser


# If user is logged in, redirects to menu.
# Else, returns login page.
def index(request):
    # Reusable output variables
    lists = msg = None

    # If user is not logged in, send him to log in page.
    if not request.user.is_authenticated:
        template = loader.get_template('delivery/login.html')
        
        msg = "Entre com suas credenciais"
        context = {"lists":lists, "msg":msg}
        return HttpResponse(template.render(context, request))

    # If user IS logged in, send him to menu
    context = {"lists":lists, "msg":msg}
    return redirect("/delivery/menu", context,permanent=True)

# Handles login attempts
def login_forms(request):

    # Reusable output variables
    lists = msg = None

    name = request.POST['name']
    password = request.POST['password']
    
    user = authenticate(request, username=name, password=password)
    
    if user is not None:
        login(request, user)
    
        context = {"lists":lists, "msg":msg}
        return redirect("/delivery/menu", context,permanent=True)
    else:
        template = loader.get_template('delivery/login.html')
        
        msg = "Credenciais inválidas!"
        context = {"lists":lists, "msg":msg}
    
    return HttpResponse(template.render(context, request))

# Handles logup requests
def logup(request):
    lists = msg = None
    template = loader.get_template('delivery/logup.html')
    
    msg = "Crie um nome de usuário e uma senha forte."
    
    context = {"lists":lists, "msg":msg}
    return HttpResponse(template.render(context, request))
    
def logup_forms(request):

    # Reusable output variables
    lists = msg = None

    name = request.POST['name']
    password = request.POST['password']
    
    if len(User.objects.filter(username=name)) != 0:
        template = loader.get_template('delivery/logup.html')
    
        msg = "Nome de usuário já existe. Escolha outro."
        
        context = {"lists":lists, "msg":msg}
        return HttpResponse(template.render(context, request))
    
    user = User.objects.create_user(username=name, password=password)
    
    user = authenticate(request, username=name, password=password)
    
    login(request, user)
    
    Cliente.objects.create(name=request.POST["namefull"], user=user)
    
    return redirect("/")

    
# menu is going to be called from login ou logup view and may receive
# context arguments.
def menu(request, **context):
    # Reusable output variables
    lists = msg = None
    template = loader.get_template('delivery/menu.html')
    
    msg = "Bem-vindo ao Menu! Escolha a quantidade e o tamanho dos sabores que desejar."
    
    context = {"lists":lists, "msg":msg}
    return HttpResponse(template.render(context, request))
    
    
# The form going to receive menu choices from client_name
def menu_forms(request):

    # All variables we want to get back from the forms
    amount = ["calabresaqtd", "mussarelaqtd", "frangoqtd", "portuguesaqtd"]
    sizes = ["calabrezasize", "mussarelasize", "frangosize", "portuguesasize"]
    pizzaNames = ["Calabresa", "Mussarela", "Frango", "Portuguesa"]
    
    # Reusable output variables
    lists = msg = None
    
    # Identify the user logged in
    client = Cliente.objects.filter(user__username=request.user.username)[0]
    
    # Iteration over all menu options
    for flavor in amount:
        # If any option is non zero, get it and save as a request.
        if request.POST[flavor] != "0":
            index = amount.index(flavor)
            request_ = Pedido.objects.create(pizza=pizzaNames[index], amount=request.POST[flavor], size=request.POST[sizes[index]], client_name=client.name)
            client.pedidos.add(request_)
            
            

    
    template = loader.get_template('delivery/basket.html')
    
    msg = "Seu carrinho está montado abaixo."
    
    lists = client.pedidos.all()
    
    context = {"lists":lists, "msg":msg}
    return HttpResponse(template.render(context, request)) 

# Shows current request for this client and asks for confirmation.
def basket_forms(request):
    
    msg = lists = None
    
    client = Cliente.objects.filter(user__username=request.user.username)[0]
    
    # If user has confirmed its requests, send him to final view.
    if request.POST["botaoforms"] == "Salvar":
        
        return redirect("/delivery/final")
       
    # If user clicks the "clean" button, clear all requests. 
    else:
        
        client.pedidos.all().delete()
        
        return redirect("/")
   
# Shows final vision about client's basket 
def final(request):
    
    if len(Cliente.objects.filter(user__username=request.user.username)) != 0:
        client = Cliente.objects.filter(user__username=request.user.username)[0]
    else:
        return redirect("/")
    
    msg = "Seus pedidos foram enviados e estão listados abaixo."
    lists = client.pedidos.all()
    
    template = loader.get_template('delivery/final.html')
    context = {"lists":lists, "msg":msg}
    return HttpResponse(template.render(context, request)) 
    
    
# This view only logs user out.
def disconnectlogout(request):
    logout(request)
    
    return redirect("/")
    



