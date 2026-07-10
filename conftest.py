import pytest
import random
from api.helpers import register_new_courier_and_return_login_password, login_courier, delete_courier


@pytest.fixture
def create_and_delete_courier():
    """Фикстура для создания и удаления курьера"""
    courier_data = register_new_courier_and_return_login_password()
    if courier_data:
        login, password, first_name = courier_data
        courier_id = login_courier(login, password)
        yield login, password, first_name, courier_id
        if courier_id:
            delete_courier(courier_id)
    else:
        yield None, None, None, None


@pytest.fixture
def courier_data():
    """Фикстура с данными курьера"""
    login = "test_courier_" + str(hash(str(random.random())))
    password = "test_pass_" + str(hash(str(random.random())))
    return login, password