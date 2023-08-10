import pytest
from django.test import Client
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from Hub.views import *
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from Hub.models import Printer, PrintingQue, Filament, Project, Parts
from django.contrib.auth import get_user_model
from Hub.forms import FilamentForm, PartsForm
from django.contrib.auth.models import User

User = get_user_model()

@pytest.mark.django_db
def test_register_view():
    client = Client()
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_login_view(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_printer_list_view(client):
    response = client.get(reverse('printer_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_printer_view(client):
    response = client.get(reverse('add_printer'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_printer_view(client, printer):
    response = client.post(reverse('delete_printer', args=[printer.id]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_printer_detail_view_status_code():
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('printer_detail', args=[printer.id])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_printer_detail_view_context():
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('printer_detail', args=[printer.id])
    response = client.get(url)
    assert 'printer' in response.context
    assert response.context['printer'] == printer


@pytest.mark.django_db
def test_printer_detail_view_template_used():
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('printer_detail', args=[printer.id])
    response = client.get(url)
    assert 'printer_detail.html' in [template.name for template in response.templates]



@pytest.mark.django_db
def test_register_view_post_valid_form_status_code(client):
    data = {
        'username': 'testuser',
        'password1': 'securepassword',
        'password2': 'securepassword',
    }
    response = client.post(reverse('register'), data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_register_view_post_valid_form_redirect(client):
    data = {
        'username': 'testuser',
        'password1': 'securepassword',
        'password2': 'securepassword',
    }
    response = client.post(reverse('register'), data)
    assert response.url == reverse('login')

@pytest.mark.django_db
def test_register_view_post_valid_form_user_created(client):
    data = {
        'username': 'testuser',
        'password1': 'securepassword',
        'password2': 'securepassword',
    }
    client.post(reverse('register'), data)
    assert User.objects.filter(username='testuser').exists()


@pytest.mark.django_db
def test_register_view_post_invalid_form_status_code(client):
    data = {}
    response = client.post(reverse('register'), data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_register_view_post_invalid_form_template(client):
    data = {}
    response = client.post(reverse('register'), data)
    assert 'register.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_register_view_post_invalid_form_user_not_created(client):
    data = {}
    client.post(reverse('register'), data)
    assert not User.objects.filter(username='testuser').exists()


@pytest.mark.django_db
def test_edit_printer_view_get_status_code(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_edit_printer_view_get_template(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    response = client.get(url)
    assert 'edit_printer.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_edit_printer_view_get_form_context(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    response = client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], PrinterForm)

@pytest.mark.django_db
def test_edit_printer_view_get_printer_context(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    response = client.get(url)
    assert 'printer' in response.context
    assert response.context['printer'] == printer


@pytest.mark.django_db
def test_edit_printer_view_post_valid_form_status_code(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    form_data = {
        'name': 'Edited Printer',
        'head': 2,
        'max_temperature': 15,
        'max_speed': 40,
    }
    response = client.post(url, form_data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_edit_printer_view_post_valid_form_redirect(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    form_data = {
        'name': 'Edited Printer',
        'head': 2,
        'max_temperature': 15,
        'max_speed': 40,
    }
    response = client.post(url, form_data)
    assert response.url == reverse('printer_list')

@pytest.mark.django_db
def test_edit_printer_view_post_valid_form_updated_printer_name(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    form_data = {
        'name': 'Edited Printer',
        'head': 2,
        'max_temperature': 15,
        'max_speed': 40,
    }
    client.post(url, form_data)
    updated_printer = Printer.objects.get(id=printer.id)
    assert updated_printer.name == form_data['name']

@pytest.mark.django_db
def test_edit_printer_view_post_valid_form_updated_printer_head(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    form_data = {
        'name': 'Edited Printer',
        'head': 2,
        'max_temperature': 15,
        'max_speed': 40,
    }
    client.post(url, form_data)
    updated_printer = Printer.objects.get(id=printer.id)
    assert updated_printer.head == form_data['head']

@pytest.mark.django_db
def test_edit_printer_view_post_valid_form_updated_printer_max_temperature(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    form_data = {
        'name': 'Edited Printer',
        'head': 2,
        'max_temperature': 15,
        'max_speed': 40,
    }
    client.post(url, form_data)
    updated_printer = Printer.objects.get(id=printer.id)
    assert updated_printer.max_temperature == form_data['max_temperature']

@pytest.mark.django_db
def test_edit_printer_view_post_valid_form_updated_printer_max_speed(client):
    printer = Printer.objects.create(name='Test Printer', head=1, max_temperature=12, max_speed=34)
    client = Client()
    url = reverse('edit_printer', args=[printer.id])
    form_data = {
        'name': 'Edited Printer',
        'head': 2,
        'max_temperature': 15,
        'max_speed': 40,
    }
    client.post(url, form_data)
    updated_printer = Printer.objects.get(id=printer.id)
    assert updated_printer.max_speed == form_data['max_speed']


@pytest.mark.django_db
def test_project_list_view_get(client):
    client = Client()
    url = reverse('project')
    response = client.get(url)
    assert response.status_code == 200



@pytest.mark.django_db
def test_project_list_view_get_template(client):
    client = Client()
    url = reverse('project')
    response = client.get(url)
    assert 'project_list.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_add_project_view_get(client):
    client = Client()
    url = reverse('add_project')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_project_view_get_redirect(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    project = Project.objects.create(name='Test Project', user=user)
    client = Client()
    url = reverse('delete_project', args=[project.id])
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_project_view_get_deleted(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    project = Project.objects.create(name='Test Project', user=user)
    client = Client()
    url = reverse('delete_project', args=[project.id])
    response = client.get(url)
    assert not Project.objects.filter(id=project.id).exists()

@pytest.mark.django_db
def test_delete_project_view_post_status_code(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    project = Project.objects.create(name='Test Project', user=user)
    url = reverse('delete_project', args=[project.id])
    response = client.post(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_delete_project_view_post_project_deleted(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    project = Project.objects.create(name='Test Project', user=user)
    url = reverse('delete_project', args=[project.id])
    response = client.post(url)
    assert not Project.objects.filter(id=project.id).exists()


@pytest.mark.django_db
def test_filament_list_view_without_filters(client):
    Filament.objects.create(name='PLA', producer='XYZ', material='PLA', colour='Red', weight='1', temperature_min=186, temperature_max=210)
    Filament.objects.create(name='ABS', producer='ABC', material='ABS', colour='Black', weight='2', temperature_min=186, temperature_max=210)
    Filament.objects.create(name='PETG', producer='DEF', material='PETG', colour='White', weight='3', temperature_min=186, temperature_max=210)
    client = Client()
    url = reverse('filament')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['filaments']) == 3

@pytest.mark.django_db
def test_filament_list_view_with_filters(client):
    Filament.objects.create(name='PLA', producer='XYZ', material='PLA', colour='Red', weight='1', temperature_min=186, temperature_max=210)
    Filament.objects.create(name='ABS', producer='ABC', material='ABS', colour='Black', weight='2', temperature_min=186, temperature_max=210)
    Filament.objects.create(name='PETG', producer='DEF', material='PETG', colour='White', weight='3', temperature_min=186, temperature_max=210)
    client = Client()
    url = reverse('filament') + f"?search_name=PLA&search_producer=XYZ"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['filaments']) == 1



@pytest.mark.django_db
def test_add_filament_view_get(client):
    client = Client()
    url = reverse('add_filament')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], FilamentForm)


@pytest.mark.django_db
def test_add_filament_view_post_valid_form(client):
    # Utworzenie klienta testowego
    client = Client()

    # Utworzenie ścieżki do widoku AddFilament
    url = reverse('add_filament')

    # Dane do formularza
    form_data = {
        'name': 'PLA',
        'producer': 'XYZ',
        'material': 'PLA',
        'colour': 'Red',
        'weight': 100,
        'temperature_min': 195,
        'temperature_max': 210
    }

    response = client.post(url, form_data)
    assert response.status_code == 302
    assert Filament.objects.filter(name=form_data['name']).exists()

@pytest.mark.django_db
def test_parts_list_view_empty(client):
    client = Client()
    url = reverse('parts')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['parts']) == 0

@pytest.mark.django_db
def test_parts_list_view_with_parts(client):
    Parts.objects.create(name='Part 1', description='Description 1')
    Parts.objects.create(name='Part 2', description='Description 2')
    Parts.objects.create(name='Part 3', description='Description 3')
    client = Client()
    url = reverse('parts')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['parts']) == 3


@pytest.mark.django_db
def test_add_parts_view_ge_status_code(client):
    client = Client()
    url = reverse('add_parts')
    response = client.get(url)
    assert response.status_code == 200



@pytest.mark.django_db
def test_add_parts_view_get_context(client):
    client = Client()
    url = reverse('add_parts')
    response = client.get(url)
    assert isinstance(response.context['form'], PartsForm)
    assert 'printers' in response.context


@pytest.mark.django_db
def test_add_parts_view_post_valid_form_status_code(client):
    client = Client()
    printer1 = Printer.objects.create(name='Printer 1', head=2, max_temperature=300, max_speed=200)
    printer2 = Printer.objects.create(name='Printer 2', head=1, max_temperature=350, max_speed=250)
    url = reverse('add_parts')

    form_data = {
        'name': 'Part 1',
        'description': 'Description 1',
        'printers': [printer1.id, printer2.id]
    }

    response = client.post(url, form_data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_add_parts_view_post_valid_form_part_created(client):
    client = Client()
    printer1 = Printer.objects.create(name='Printer 1', head=2, max_temperature=300, max_speed=200)
    printer2 = Printer.objects.create(name='Printer 2', head=1, max_temperature=350, max_speed=250)
    url = reverse('add_parts')

    form_data = {
        'name': 'Part 1',
        'description': 'Description 1',
        'printers': [printer1.id, printer2.id]
    }

    response = client.post(url, form_data)
    assert Parts.objects.filter(name=form_data['name']).exists()

@pytest.mark.django_db
def test_add_parts_view_post_valid_form_printers_associated(client):
    client = Client()
    printer1 = Printer.objects.create(name='Printer 1', head=2, max_temperature=300, max_speed=200)
    printer2 = Printer.objects.create(name='Printer 2', head=1, max_temperature=350, max_speed=250)
    url = reverse('add_parts')

    form_data = {
        'name': 'Part 1',
        'description': 'Description 1',
        'printers': [printer1.id, printer2.id]
    }

    response = client.post(url, form_data)
    part = Parts.objects.get(name=form_data['name'])
    assert part.printers.count() == 2

@pytest.mark.django_db
def test_delete_part_view_post_code(client):
    client = Client()
    part = Parts.objects.create(name='Test Part', description='Test Description')
    url = reverse('delete_part', args=[part.id])
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_part_view_post(client):
    client = Client()
    part = Parts.objects.create(name='Test Part', description='Test Description')
    url = reverse('delete_part', args=[part.id])
    response = client.post(url)
    assert not Parts.objects.filter(id=part.id).exists()


@pytest.mark.django_db
def test_delete_filament_view_post_code(client):
    client = Client()
    filament = Filament.objects.create(name='Test Filament', producer='Test Producer', temperature_max=300, temperature_min=100, weight=888)
    url = reverse('delete_filament', args=[filament.id])
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_filament_view_post(client):
    client = Client()
    filament = Filament.objects.create(name='Test Filament', producer='Test Producer', temperature_max=300, temperature_min=100, weight=888)
    url = reverse('delete_filament', args=[filament.id])
    response = client.post(url)
    assert not Filament.objects.filter(id=filament.id).exists()


@pytest.mark.django_db
def test_edit_filament_view_get_code(client):
    client = Client()
    filament = Filament.objects.create(name='Test Filament', producer='Test Producer', temperature_max=300, temperature_min=100, weight=888)
    url = reverse('edit_filament', args=[filament.id])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_filament_view_get_template(client):
    client = Client()
    filament = Filament.objects.create(name='Test Filament', producer='Test Producer', temperature_max=300, temperature_min=100, weight=888)
    url = reverse('edit_filament', args=[filament.id])
    response = client.get(url)
    assert isinstance(response.context['form'], FilamentForm)


@pytest.mark.django_db
def test_edit_filament_view_get(client):
    client = Client()
    filament = Filament.objects.create(name='Test Filament', producer='Test Producer', temperature_max=300, temperature_min=100, weight=888)
    url = reverse('edit_filament', args=[filament.id])
    response = client.get(url)
    assert 'filament' in response.context


@pytest.mark.django_db
def test_edit_filament_view_post_valid_form_status_code(client):
    client = Client()
    filament = Filament.objects.create(name='Edited Filament', producer='Edited Producer', temperature_max=300, temperature_min=100, weight=888)
    url = reverse('edit_filament', args=[filament.id])
    form_data = {
        'name': 'Edited Filament',
        'producer': 'Edited Producer'
    }

    response = client.post(url, form_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_edit_filament_view_post_valid_form_updated_data(client):
    client = Client()
    filament = Filament.objects.create(name='Edited Filament', producer='Edited Producer', temperature_max=300, temperature_min=100, weight=888)
    url = reverse('edit_filament', args=[filament.id])
    form_data = {
        'name': 'Edited Filament',
        'producer': 'Edited Producer'
    }

    response = client.post(url, form_data)
    updated_filament = Filament.objects.get(id=filament.id)
    assert updated_filament.name == form_data['name']
    assert updated_filament.producer == form_data['producer']


