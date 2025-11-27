from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Todo


class TodoModelTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            completed=False
        )

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertFalse(self.todo.completed)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)

    def test_todo_str_method(self):
        self.assertEqual(str(self.todo), "Test Todo")

    def test_todo_ordering(self):
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = Todo.objects.all()
        self.assertEqual(todos[0], todo2)
        self.assertEqual(todos[1], todo1)

    def test_todo_completion_toggle(self):
        self.assertFalse(self.todo.completed)
        self.todo.completed = True
        self.todo.save()
        self.assertTrue(self.todo.completed)

    def test_todo_blank_description(self):
        todo = Todo.objects.create(title="No Description")
        self.assertEqual(todo.description, "")


class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo1 = Todo.objects.create(
            title="Todo 1",
            description="Description 1",
            completed=False
        )
        self.todo2 = Todo.objects.create(
            title="Todo 2",
            description="Description 2",
            completed=True
        )

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/home.html')
        self.assertContains(response, "Todo 1")
        self.assertContains(response, "Todo 2")

    def test_todo_list_view_empty(self):
        Todo.objects.all().delete()
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No todos yet")

    def test_todo_create_view_get(self):
        response = self.client.get(reverse('todo_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_form.html')

    def test_todo_create_view_post(self):
        data = {
            'title': 'New Todo',
            'description': 'New Description',
            'completed': False
        }
        response = self.client.post(reverse('todo_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_todo_update_view_get(self):
        response = self.client.get(reverse('todo_update', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_form.html')
        self.assertContains(response, "Todo 1")

    def test_todo_update_view_post(self):
        data = {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'completed': True
        }
        response = self.client.post(reverse('todo_update', args=[self.todo1.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'Updated Todo')
        self.assertEqual(self.todo1.description, 'Updated Description')
        self.assertTrue(self.todo1.completed)

    def test_todo_delete_view_get(self):
        response = self.client.get(reverse('todo_delete', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_confirm_delete.html')
        self.assertContains(response, "Todo 1")

    def test_todo_delete_view_post(self):
        response = self.client.post(reverse('todo_delete', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=self.todo1.pk).exists())

    def test_todo_toggle_view(self):
        self.assertFalse(self.todo1.completed)
        response = self.client.get(reverse('todo_toggle', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.completed)

        response = self.client.get(reverse('todo_toggle', args=[self.todo1.pk]))
        self.todo1.refresh_from_db()
        self.assertFalse(self.todo1.completed)


class TodoURLTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description"
        )

    def test_todo_list_url(self):
        url = reverse('todo_list')
        self.assertEqual(url, '/')

    def test_todo_create_url(self):
        url = reverse('todo_create')
        self.assertEqual(url, '/create/')

    def test_todo_update_url(self):
        url = reverse('todo_update', args=[self.todo.pk])
        self.assertEqual(url, f'/update/{self.todo.pk}/')

    def test_todo_delete_url(self):
        url = reverse('todo_delete', args=[self.todo.pk])
        self.assertEqual(url, f'/delete/{self.todo.pk}/')

    def test_todo_toggle_url(self):
        url = reverse('todo_toggle', args=[self.todo.pk])
        self.assertEqual(url, f'/toggle/{self.todo.pk}/')
