import pytest
from django.test import Client
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from Hub.views import *
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from Hub.models import Printer



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
def test_register_view_post_valid_form(client):
    data = {
        'username': 'testuser',
        'password1': 'securepassword',
        'password2': 'securepassword',
    }
    response = client.post(reverse('register'), data)

    assert response.status_code == 302
    assert response.url == reverse('login')

    assert User.objects.filter(username='testuser').exists()


@pytest.mark.django_db
def test_register_view_post_invalid_form2(client):
    data = {}
    response = client.post(reverse('register'), data)
    assert response.status_code == 200
    assert 'register.html' in [template.name for template in response.templates]

    assert not User.objects.filter(username='testuser').exists()