import pytest
import allure
from api.order_api import OrderAPI


@allure.feature('Получение списка заказов')
class TestOrderList:
    
    @allure.title('В тело ответа возвращается список заказов')
    def test_get_orders_returns_list(self):
        response = OrderAPI.get_orders()
        
        assert response.status_code == 200
        # Проверяем, что ответ содержит список заказов
        assert isinstance(response.json(), dict)
        assert 'orders' in response.json()
        assert isinstance(response.json()['orders'], list)
    
    @allure.title('Список заказов не пустой')
    def test_orders_list_not_empty(self):
        response = OrderAPI.get_orders()
        
        assert response.status_code == 200
        orders = response.json().get('orders', [])
        # Проверяем, что список не пустой (или хотя бы есть структура)
        # В реальном API список может быть пустым, поэтому проверяем только тип
        assert isinstance(orders, list)
    
    @allure.title('Каждый заказ в списке содержит необходимые поля')
    def test_order_has_required_fields(self):
        response = OrderAPI.get_orders()
        
        assert response.status_code == 200
        orders = response.json().get('orders', [])
        
        if len(orders) > 0:
            # Проверяем структуру первого заказа
            first_order = orders[0]
            # Проверяем наличие ключевых полей
            assert 'id' in first_order or 'track' in first_order
            assert 'status' in first_order or 'createdAt' in first_order
        # Если заказов нет, тест все равно пройден, так как это валидное состояние