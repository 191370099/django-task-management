from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from .models import User, Task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy, reverse


class HomeView(View):
    def get(self, request):
        return render(request, 'hello.html')


class LoginView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=str(email).lower(), password=password)
        if user is not None:
            login(request, user)
            if user.role == 'manager':
                return redirect('manager.dashboard')
            return redirect('home')
        return render(request, 'Authentication/login.html')

    def get(self, request):
        return render(request, 'Authentication/login.html')


class SignUpView(View):
    def post(self, request):
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password = request.POST.get('password')
        user = User.objects.create(email=email, password=make_password(password), name=name, phone=phone, role=role)
        login(request, user)
        return redirect('manager.dashboard')

    def get(self, request):
        return render(request, 'Authentication/signup.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class ManagerRequiredMixin(LoginRequiredMixin):
    def __init__(self):
        self.request = None

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse('login')))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'manager':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'managers/dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(assigned_by=self.request.user)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class AddTaskView(CreateView):
    model = Task
    template_name = 'managers/task_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('manager.dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['developers'] = User.objects.filter(role='developer')
        return context

    def form_valid(self, form):
        developer = User.objects.get(pk=int(self.request.POST.get('assigned_to')))
        form.instance.assigned_to = developer
        form.instance.assigned_by = self.request.user
        return super().form_valid(form)
