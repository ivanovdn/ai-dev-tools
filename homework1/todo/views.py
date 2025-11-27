from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

class TodoListView(ListView):
    model = Todo
    template_name = 'todo/home.html'
    context_object_name = 'todos'

class TodoCreateView(CreateView):
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todo_list')

class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todo_list')

class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')

def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')
