from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import TodoItem
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistroUserForm
from .forms import CustomUserCreationForm
from .forms import ClienteForm, TipoTarjetaForm, TarjetaForm
from django.db import connection
from .models import TodoItem, Cliente, TipoTarjeta, Tarjeta


# Create your views here.
def home(request):
    return render(request, "home.html")

from django.contrib.auth.forms import UserCreationForm

@login_required
def todos(request):

    request.session ["usuario"] = "cpazro"
    usuario=request.session.get("usuario")
    context = {"usuario": usuario}

    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})
    return render(request, "todos.html", context)

def registro_user(request):
    if request.method == 'POST':
        form = RegistroUserForm(request.POST)  # Usa el formulario de registro
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            login(request, user)  # Inicia sesión al usuario
            return redirect('/accounts/login/')  # Redirige a la página de inicio de sesión
    else:
        form = RegistroUserForm()  # Crea una instancia vacía del formulario

    return render(request, 'registro_user.html', {'form': form})

# def registro_user(request):
#     if request.method == "POST":
#         form = RegistroUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return HttpResponse("Usuario creado")
#             messages.success(request, 'Success')

#     else:
#         form = RegistroUserForm()
#         form = CustomUserCreationForm()

#     return render(request, 'registro_user.html', {'form': form})

@login_required
def carrito(request):
    return render(request, "carrito.html")

def inicio(request):
    return render(request, "inicio.html")

def inicio2(request):
    return render(request, "inicio2.html")

def login(request, user):
    return render(request, "login.html")

def login2(request, user):
    return render(request, "login2.html")

def despliegue(request):
    return render(request, "despliegue_producto.html")

def formulario(request):
    return render(request, "formulario_producto.html")

@login_required
def dashboard_cliente(request):

    request.session ["usuario"] = "cpazro"
    usuario=request.session.get("usuario")
    context = {"usuario": usuario}

    return render(request, "dashboard_cliente.html")

#cami
@user_passes_test(lambda u: u.is_superuser)
def lista_clientes(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre, genero, fecha_nacimiento, clave, correo, es_miembro FROM myapp_cliente")
        #clientes = cursor.fetchall()
        clientes = Cliente.objects.all()
    context = {'clientes': clientes}
   #return render(request, 'lista_clientes.html', context)
    return render(request, 'lista_clientes.html', {'clientes': clientes})


def lista_tarjeta(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.numero_tarjeta, t.cvv, tt.descripcion AS tipo_tarjeta, c.nombre AS cliente
            FROM myapp_tarjeta t
            JOIN myapp_tipotarjeta tt ON t.tipo_id = tt.id_tipo
            JOIN myapp_cliente c ON t.cliente_id = c.id
        """)
        tarjetas = Tarjeta.objects.select_related('tipo', 'cliente').all()
        #tarjetas = cursor.fetchall()
    context = {'tarjetas': tarjetas}
    return render(request, 'lista_tarjeta.html', context)

@user_passes_test(lambda u: u.is_superuser)
def lista_tipo_tarjeta(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_tipo, descripcion FROM myapp_tipotarjeta")
        #tipos_tarjeta = cursor.fetchall()
        tipos_tarjeta = TipoTarjeta.objects.all()
    context = {'tipos_tarjeta': tipos_tarjeta}
    return render(request, 'lista_tipo_tarjeta.html', context)

# Vista para añadir Cliente
@login_required
def add_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')  # Redirige a la vista de listar clientes
    else:
        form = ClienteForm()
    return render(request, 'add_cliente.html', {'form': form})

# Vista para añadir TipoTarjeta
@login_required
def add_tipo_tarjeta(request):
    if request.method == 'POST':
        form = TipoTarjetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_tarjeta')  # Redirige a la vista de listar tipo_tarjetas
    else:
        form = TipoTarjetaForm()
    return render(request, 'add_tipo_tarjeta.html', {'form': form})

# Vista para añadir Tarjeta
@login_required
def add_tarjeta(request):
    if request.method == 'POST':
        form = TarjetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tarjeta')  # Redirige a la vista de listar tarjetas
    else:
        form = TarjetaForm()
    return render(request, 'add_tarjeta.html', {'form': form})

# Vista para editar Cliente
@login_required
def edit_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')  # Redirige a la vista de listar clientes
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'edit_cliente.html', {'form': form})

# Vista para editar TipoTarjeta
@login_required
def edit_tipo_tarjeta(request, id_tipo):
    tipo_tarjeta = get_object_or_404(TipoTarjeta, id_tipo=id_tipo)
    if request.method == 'POST':
        form = TipoTarjetaForm(request.POST, instance=tipo_tarjeta)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_tarjeta')  # Redirige a la vista de listar tipo_tarjetas
    else:
        form = TipoTarjetaForm(instance=tipo_tarjeta)
    print(f"Tipo de Tarjeta a Editar: {tipo_tarjeta}")
    return render(request, 'edit_tipo_tarjeta.html', {'form': form})

# Vista para editar Tarjeta
@login_required
def edit_tarjeta(request, numero_tarjeta):
    tarjeta = get_object_or_404(Tarjeta, numero_tarjeta=numero_tarjeta)
    if request.method == 'POST':
        form = TarjetaForm(request.POST, instance=tarjeta)
        if form.is_valid():
            form.save()
            return redirect('lista_tarjeta')  # Redirige a la vista de listar tarjetas
    else:
        form = TarjetaForm(instance=tarjeta)
    return render(request, 'edit_tarjeta.html', {'form': form})

# Vista para eliminar Cliente
@login_required
def delete_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')  # Redirige a la vista de listar clientes
    return render(request, 'delete_cliente.html', {'cliente': cliente})

# Vista para eliminar TipoTarjeta
@login_required
def delete_tipo_tarjeta(request, id_tipo):
    tipo_tarjeta = get_object_or_404(TipoTarjeta, id_tipo=id_tipo)
    if request.method == 'POST':
        tipo_tarjeta.delete()
        return redirect('lista_tipo_tarjeta')  # Redirige a la vista de listar tipo_tarjetas
    return render(request, 'delete_tipo_tarjeta.html', {'tipo_tarjeta': tipo_tarjeta})

# Vista para eliminar Tarjeta
@login_required
def delete_tarjeta(request, numero_tarjeta):
    tarjeta = get_object_or_404(Tarjeta, numero_tarjeta=numero_tarjeta)
    if request.method == 'POST':
        tarjeta.delete()
        return redirect('lista_tarjeta')  # Redirige a la vista de listar tarjetas
    return render(request, 'delete_tarjeta.html', {'tarjeta': tarjeta})