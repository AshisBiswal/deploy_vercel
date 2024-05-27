from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User,Permission
from django.shortcuts import get_object_or_404, redirect
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from .forms import registerform,loginform,employeeform
from django.core.exceptions import PermissionDenied


def register(request):
    if request.method == "POST":
        form = registerform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                # Username already taken, display a message
                return render(request, 'registration.html', {'form': form, 'error_message': 'Username already taken'})

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            
            # Assuming you have a Manager model
            manager = Manager.objects.create(user=user)
            
            # Get the permission object with the specific content type
            content_type = ContentType.objects.get_for_model(Manager)  # Replace 'Employee' with the appropriate model
            permission = Permission.objects.get(codename='add_employee', content_type=content_type)
            
            # Assign the permission to the manager's user
            user.user_permissions.add(permission)

            return redirect('login')
            

    else:
        form = registerform()

    return render(request, 'registration.html', {'form': form})


def login_f(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                if Employee.objects.filter(username=username).exists():
                    employee = Employee.objects.get(username=username)
                    return render(request, 'employee.html',{'employee':employee})
                else:
                    manager = Manager.objects.get(user=user)
                    
                    return render(request, 'manager.html', {'manager': manager})
            else:
                error_message = "Invalid username or password."

            
            
            
    else:
        form = loginform()
        error_message = None
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def custom_permission_denied_view(request, exception=None):
    return render(request, 'permission_denied.html', status=403)


@permission_required('system.add_employee',raise_exception=True)
def add_employee(request):
    try:
        if request.method == 'POST':
            form = employeeform(request.POST)
            if form.is_valid():
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    email = form.cleaned_data['email']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']

                # Check if username already exists
                if User.objects.filter(username=username).exists():
                    # Username already taken, display a message
                    manager = Manager.objects.get(user = request.user)
                    employees  = manager.employees.all()
                    return render(request, 'add_employee.html', {'form': form, 'error_message': 'Username already taken','employees':employees})

                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                
                manager = Manager.objects.get(user=request.user)
                employee = Employee.objects.create(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    manager=manager
                )
                
                return redirect('add_employee')
        else:
            form = employeeform()
            manager = Manager.objects.get(user = request.user)
            employees  = manager.employees.all()
        return render(request, 'add_employee.html', {'form': form,'employees':employees})
    except PermissionDenied:
        return custom_permission_denied_view(request)
    
