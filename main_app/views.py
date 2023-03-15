from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy
from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# cats = [
#     Cat('Lolo', 'Tabby', 'Long Curly Hair', 3),
#     Cat('Sachi', 'Tortoise Shell', 'Cute face', 0),
#     Cat('Raven', 'Black Tripod', '3 legged cat', 4)
# ]

def home(request):
    # res.send in Express
    # return HttpResponse('<h1> Cat Collector </h1>')
    return render(request, 'home.html')

def about(request):
    # return HttpResponse('<h1> About the Cat Collector </h1>')
    return render(request, 'about.html')

@login_required
def cats_index(request):
    # select * from main_app_cat;  
    # cats = Cat.objects.all() # Django's ORM Function
    # only return the user's cats from the DB
    cats = Cat.objects.filter(user = request.user)
    return render(request, 'cats/index.html', {'cats': cats})

@login_required
def cats_detail(request, cat_id):
    # select * from main_app_cat where id = cat_id
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have
    })


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age', 'image']
    # fields = '__all__'
    # success_url = '/cats/'

    def form_valid(self, form):
        # self.request.user is the logged in user
        form.instance.user = self.request.user
        # allows the CreateView form_valid method to do its normal work 
        return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

@login_required
def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail', cat_id=cat_id)


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model= Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

@login_required
def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
# Sign Up View Function:
def signup(request):
    error_message = ''
    if request.method == 'POST':
        # Make a 'user' form object with the data from the browser
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # save user to db
            user = form.save()
            # Log in the user automatically once they sign up
            login(request, user)
            return redirect('index')
        
        else:
            error_message = 'Invalid: Please Try Again!'

    # If there's a bad post or get request:
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
