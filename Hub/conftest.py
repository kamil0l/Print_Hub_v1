import pytest
from Hub.views import Printer

@pytest.fixture
def printer():
    printer = Printer.objects.create(name='Test Printer', head='2', max_temperature='23', max_speed='33')
    return printer