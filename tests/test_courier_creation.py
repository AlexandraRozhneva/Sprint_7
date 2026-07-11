import pytest
import allure
import requests
from api.courier_api import CourierAPI
from constants.urls import Urls
from constants.messages import ErrorMessages, SuccessMessages
from helpers.data_generators import generate_random_login, generate_random_password, generate_random_first_name


@allure.feature('Создание курьера')
class TestCourierCreation:
    
    @allure.title('Курьера можно создать')
    @pytest.mark.parametrize('has_first_name', [True, False])
    def test_create_courier_success(self, has_first_name):
        login = generate_random_login()
        password = generate_random_password()
        first_name = generate_random_first_name() if has_first_name else None
        
        response = CourierAPI.create_courier(login, password, first_name)
        
        assert response.status_code == 201
        assert response.json() == SuccessMessages.OK_TRUE
    
    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier(self):
        login = generate_random_login()
        password = generate_random_password()
        first_name = generate_random_first_name()
        
        response1 = CourierAPI.create_courier(login, password, first_name)
        assert response1.status_code == 201
        
        response2 = CourierAPI.create_courier(login, password, first_name)
        assert response2.status_code == 409
        assert ErrorMessages.LOGIN_ALREADY_USED in response2.text
    
    @allure.title('При создании курьера обязательны поля login и password')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_fields(self, missing_field):
        login = generate_random_login()
        password = generate_random_password()
        
        payload = {"login": login, "password": password}
        payload.pop(missing_field)
        
        response = requests.post(Urls.get_courier_url(), data=payload)
        
        assert response.status_code == 400
        assert ErrorMessages.NOT_ENOUGH_DATA in response.text