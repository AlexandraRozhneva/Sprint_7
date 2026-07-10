import pytest
import allure
from api.order_api import OrderAPI
from api.helpers import generate_random_string


@allure.feature('Создание заказа')
class TestOrderCreation:
    
    @pytest.fixture
    def order_data(self):
        """Базовые данные для заказа"""
        return {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": "г. Москва, ул. Тестовая, д. 1",
            "metroStation": 1,
            "phone": "+7 999 999 99 99",
            "rentTime": 1,
            "deliveryDate": "2026-07-15",
            "comment": "Тестовый заказ"
        }
    
    @allure.title('Можно указать один из цветов - BLACK')
    @pytest.mark.parametrize('color', [['BLACK']])
    def test_create_order_with_black_color(self, order_data, color):
        response = OrderAPI.create_order(**order_data, color=color)
        
        assert response.status_code == 201
        assert 'track' in response.json()
    
    @allure.title('Можно указать один из цветов - GREY')
    @pytest.mark.parametrize('color', [['GREY']])
    def test_create_order_with_grey_color(self, order_data, color):
        response = OrderAPI.create_order(**order_data, color=color)
        
        assert response.status_code == 201
        assert 'track' in response.json()
    
    @allure.title('Можно указать оба цвета - BLACK и GREY')
    @pytest.mark.parametrize('color', [['BLACK', 'GREY']])
    def test_create_order_with_both_colors(self, order_data, color):
        response = OrderAPI.create_order(**order_data, color=color)
        
        assert response.status_code == 201
        assert 'track' in response.json()
    
    @allure.title('Можно совсем не указывать цвет')
    def test_create_order_without_color(self, order_data):
        response = OrderAPI.create_order(**order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
    
    @allure.title('Тело ответа содержит track')
    def test_create_order_response_has_track(self, order_data):
        response = OrderAPI.create_order(**order_data)
        
        assert response.status_code == 201
        track = response.json().get('track')
        assert track is not None
        assert isinstance(track, int)
    
    @allure.title('Тест с параметризацией цветов')
    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GREY'],
        None
    ])
    def test_create_order_color_parameterization(self, order_data, color):
        response = OrderAPI.create_order(**order_data, color=color)
        
        assert response.status_code == 201
        assert 'track' in response.json()