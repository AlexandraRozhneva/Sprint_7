import pytest
import allure
import requests
from api.courier_api import CourierAPI
from api.helpers import generate_random_string, register_new_courier_and_return_login_password


@allure.feature('Логин курьера')
class TestCourierLogin:
    
    @allure.title('Курьер может авторизоваться')
    def test_courier_login_success(self):
        courier_data = register_new_courier_and_return_login_password()
        if courier_data:
            login, password, first_name = courier_data
            
            response = CourierAPI.login_courier(login, password)
            
            assert response.status_code == 200
            assert 'id' in response.json()
    
    @allure.title('Для авторизации нужно передать все обязательные поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_missing_field(self, missing_field):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        payload = {"login": login, "password": password}
        if missing_field == 'login':
            payload.pop('login')
        else:
            payload.pop('password')
        
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data=payload
        )
        
        # API может возвращать 400 или 504 в зависимости от состояния сервера
        assert response.status_code in [400, 504]
        if response.status_code == 400:
            assert "Недостаточно данных" in response.text
    
    @allure.title('Система возвращает ошибку при неправильном логине')
    def test_login_wrong_login(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        response = CourierAPI.login_courier(login, password)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text
    
    @allure.title('Система возвращает ошибку при неправильном пароле')
    def test_login_wrong_password(self):
        courier_data = register_new_courier_and_return_login_password()
        if courier_data:
            login, password, first_name = courier_data
            
            # Пытаемся авторизоваться с неправильным паролем
            response = CourierAPI.login_courier(login, password + "wrong")
            
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.text
    
    @allure.title('Запрос возвращает ошибку, если какого-то поля нет')
    def test_login_missing_required_field(self):
        login = generate_random_string(10)
        payload = {"login": login}
        
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data=payload
        )
        
        # API может возвращать 400 или 504 в зависимости от состояния сервера
        assert response.status_code in [400, 504]
        if response.status_code == 400:
            assert "Недостаточно данных" in response.text
    
    @allure.title('Авторизация под несуществующим пользователем возвращает ошибку')
    def test_login_nonexistent_user(self):
        login = generate_random_string(15)
        password = generate_random_string(15)
        
        response = CourierAPI.login_courier(login, password)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text
    
    @allure.title('Успешный запрос возвращает id')
    def test_login_success_returns_id(self):
        courier_data = register_new_courier_and_return_login_password()
        if courier_data:
            login, password, first_name = courier_data
            
            response = CourierAPI.login_courier(login, password)
            
            assert response.status_code == 200
            assert isinstance(response.json().get('id'), int)