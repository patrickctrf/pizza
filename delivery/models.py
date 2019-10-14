from django.db import models
from django.contrib.auth.models import User

# Admin - superuser
# Pizza - Query
# Cliente - Query & field login
# Pedido - Pizzas, suas quantidades e se ele já foi concluído ou não



class Pizza(models.Model):
    flavor = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.flavor    
        
class ClienteBase(): 
    pass

class Pedido(models.Model):
    pizza = models.CharField(max_length=20)# models.ForeignKey(Pizza, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=20)
    client_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.pizza + "_" + str(self.amount) + "_" + self.size
        
        
class Cliente(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    finished = models.BooleanField(default=True)
    pedidos = models.ManyToManyField(Pedido)
    
    def __str__(self):
        return self.name
