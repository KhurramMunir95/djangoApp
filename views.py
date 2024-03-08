from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Group, Message
from .forms import GroupForm

# Create your views here.

def RegisterUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Error during registration')
    return render(request, 'base/login_register.html', {'form' : form})

def LoginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('Home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Incorrect username or password')    

    return render(request, 'base/login_register.html', {'page' : page})

def LogoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def Home(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''

    groups = Group.objects.filter(Q(name__icontains=search) | Q(description__icontains = search))

    context = { 'groups': groups }
    return render(request, 'base/home.html', context)

def GroupDetail(request, id):
    userInGroup = None
    group = Group.objects.get(id = id)
    user_messages = group.message_set.all().order_by('-created')
    if request.user == group.participants.filter(username=request.user).first():
        userInGroup = True
    else:
        userInGroup = False

    participants = group.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            group = group,
            text = request.POST.get('text')
        )
        return redirect('User', id=group.id)

    context = {'group' : group, 'user_messages': user_messages, 'participants' : participants, 'userInGroup': userInGroup}
    return render(request, 'base/user.html', context)

def createGroup(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')

    context = {'form' : form}
    return render(request, 'base/group_form.html', context)

def updateGroup(request, id):
    group = Group.objects.get(id=id)
    form = GroupForm(instance=group)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context = {'form': form}
    return render(request, 'base/group_form.html', context)

def deleteGroup(request, id):
    obj = Group.objects.get(id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('Home')
    return render(request, 'base/delete_group.html', {'obj': obj})

def deleteMessage(request, id):
    message = Message.objects.get(id=id)
    if request.method == 'POST':
        message.delete()
        return redirect('User', message.group.id)
    return render(request, 'base/delete_group.html', {'message': message})