import pytest
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse


@pytest.mark.django_db
def test_empty():
    client = Client() #tworze clienta który bedzie udawał przeglądarke
    response = client.get(reverse("main-menu")) #wchodze na podany adres metodą get
    assert response.status_code == 200 #sprawdzam czy odpowiedz jest 200


@pytest.mark.django_db
def test_empty_post():
    client = Client()
    response = client.post(reverse("main-menu"))
    assert response.status_code == 405