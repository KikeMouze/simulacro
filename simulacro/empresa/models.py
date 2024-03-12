from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

@receiver(post_save, sender=Cliente)
def crear_usuario_cliente(sender, instance, created, **kwargs):
    if created:
        username = instance.cedula  # Utiliza la cédula como nombre de usuario
        password = instance.cedula  # Utiliza la cédula como contraseña inicial
        user = User.objects.create_user(
            username=username,
            email=instance.correo,
            password=password,
            first_name=instance.nombre,
            last_name=instance.apellido,
        )
        # Asigna el usuario al grupo de clientes
        group, created = Group.objects.get_or_create(name='Clientes')
        user.groups.add(group)
        # Asigna el usuario creado al cliente
        instance.usuario = user
        instance.save()



class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

@receiver(post_save, sender=Vendedor)
def crear_usuario_cliente(sender, instance, created, **kwargs):
    if created:
        username = instance.cedula  # Utiliza la cédula como nombre de usuario
        password = instance.cedula  # Utiliza la cédula como contraseña inicial
        user = User.objects.create_user(
            username=username,
            email=instance.correo,
            password=password,
            first_name=instance.nombre,
            last_name=instance.apellido,
        )
        # Asigna el usuario al grupo de clientes
        group, created = Group.objects.get_or_create(name='Vendedor')
        user.groups.add(group)
        # Asigna el usuario creado al cliente
        instance.usuario = user
        instance.save()

class Departamento(models.Model):
    nombre=models.CharField(max_length=100)
    descripcion=models.TextField()
    archivo=models.FileField(upload_to="media/uploads/")
    campo_fecha = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.nombre
class Empleado(models.Model):
    cedula=models.IntegerField(unique=True)
    nombre=models.CharField(max_length=100,blank=True,null=True)
    apellido=models.CharField(max_length=100,blank=True,null=True)
    edad=models.IntegerField()
    fechaIngreso=models.DateField()
    departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE,blank=True)
    def __str__(self):
       return f'El nombre el empleado: {self.nombre}{self.apellido}'    