from django.urls import path

from myapp import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('',views.HomeView.as_view(), name='home'),
    path('manager/dashboard/', views.TaskListView.as_view(), name='manager.dashboard'),
    path('task/form/', views.AddTaskView.as_view(), name='task.form'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
]