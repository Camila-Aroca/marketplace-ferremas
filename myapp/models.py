from django.db import models
from django.core.validators import RegexValidator, EmailValidator

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)  # Ensure you have an id field
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=1)
    fecha_nacimiento = models.DateField()
    clave = models.CharField(max_length=100)
    correo = models.EmailField(
        unique=True,
        validators=[EmailValidator(
            message='El correo electrónico debe ser válido y tener una estructura correcta.'
        )]
        )
    es_miembro = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
class TipoTarjeta(models.Model):
    id_tipo = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Tarjeta(models.Model):
    numero_tarjeta = models.CharField(
        max_length=16, 
        primary_key=True, 
        validators=[RegexValidator(
            regex=r'^\d{16}$',  # Asegura que el número tenga exactamente 16 dígitos
            message='El número de tarjeta debe tener 16 dígitos.',
            code='invalid_card_number'
        )]
    )
    cvv = models.CharField(
        max_length=4, 
        validators=[RegexValidator(
            regex=r'^\d{3,4}$',  # Acepta 3 o 4 dígitos para el CVV
            message='El CVV debe tener 3 o 4 dígitos.',
            code='invalid_cvv'
        )]
    )
    tipo = models.ForeignKey(TipoTarjeta, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.numero_tarjeta} - {self.cliente}"