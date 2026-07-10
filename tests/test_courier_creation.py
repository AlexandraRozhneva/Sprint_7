import pytest
import allure
import requests
from api.courier_api import CourierAPI
from api.helpers import generate_random_string


@allure.feature('Создание курьера')
class TestCourierCreation:
    
    @allure.title('Курьера можно создать')
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        response = CourierAPI.create_courier(login, password, first_name)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
    
    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        # Первый запрос
        response1 = CourierAPI.create_courier(login, password, first_name)
        assert response1.status_code == 201
        
        # Второй запрос с теми же данными
        response2 = CourierAPI.create_courier(login, password, first_name)
        assert response2.status_code == 409
        assert "Этот логин уже используется" in response2.text
    
    @allure.title('Для создания курьера нужно передать все обязательные поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_field(self, missing_field):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        payload = {"login": login, "password": password}
        if missing_field == 'login':
            payload.pop('login')
        else:
            payload.pop('password')
        
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload
        )
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.text
    
    @allure.title('Запрос возвращает правильный код ответа при успешном создании')
    def test_create_courier_success_status_code(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        response = CourierAPI.create_courier(login, password)
        
        assert response.status_code == 201
    
    @allure.title('Успешный запрос возвращает ok true')
    def test_create_courier_success_response(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        response = CourierAPI.create_courier(login, password)
        
        assert response.json() == {"ok": True}
    
    @allure.title('При отсутствии одного из полей возвращается ошибка')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_field_required(self, missing_field):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        payload = {"login": login, "password": password}
        if missing_field == 'login':
            payload.pop('login')
        else:
            payload.pop('password')
        
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload
        )
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.text
    
    @allure.title('Создание пользователя с уже существующим логином возвращает ошибку')
    def test_create_courier_existing_login(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        # Создаем первого курьера
        response1 = CourierAPI.create_courier(login, password, first_name)
        assert response1.status_code == 201
        
        # Пытаемся создать второго с тем же логином
        response2 = CourierAPI.create_courier(login, generate_random_string(10))
        assert response2.status_code == 409
        assert "Этот логин уже используется" in response2.text