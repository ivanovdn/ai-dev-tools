from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo_list'),
    path('create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('update/<int:pk>/', views.TodoUpdateView.as_view(), name='todo_update'),
    path('delete/<int:pk>/', views.TodoDeleteView.as_view(), name='todo_delete'),
    path('toggle/<int:pk>/', views.toggle_todo, name='todo_toggle'),
]
